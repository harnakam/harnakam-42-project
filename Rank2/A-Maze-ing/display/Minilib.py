"""MiniLibX の窓と描画をまとめる。"""

import ctypes
from collections.abc import Callable
# mlx は型情報がなく、検査環境では未インストールの場合もある。
# import は import-untyped / import-not-found の両方を対象にする。
# make lint の --ignore-missing-imports では不要になるため、
# unused-ignore も指定して通常・strict・make lint の検査に対応する。
from mlx import Mlx  # type: ignore[import, unused-ignore]

from .palette import BACKGROUND_COLOR


def _display_available() -> bool:
    """MLX を初期化する前に、X11 の表示先に接続できるかを確かめる。

    Returns:
        接続できれば True。libxcb を読み込めないか、接続に失敗すれば False。
    """
    try:
        xcb = ctypes.CDLL("libxcb.so.1")
    except OSError:
        return False
    xcb.xcb_connect.restype = ctypes.c_void_p
    xcb.xcb_connect.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    xcb.xcb_connection_has_error.argtypes = [ctypes.c_void_p]
    xcb.xcb_disconnect.argtypes = [ctypes.c_void_p]
    connection = xcb.xcb_connect(None, None)
    if not connection:
        return False
    try:
        return bool(xcb.xcb_connection_has_error(connection) == 0)
    finally:
        xcb.xcb_disconnect(connection)


class Minilib:
    """MiniLibX の窓1つと、そこに描く画像1枚をまとめる。

    作成 → 描画・キー登録 → run() の順に使う。描画は画像バッファに対して
    行い、present() で窓に転送する。

    Attributes:
        width: 窓の幅 (ピクセル)。画面に収まるよう縮めた後の値。
        height: 窓の高さ (ピクセル)。画面に収まるよう縮めた後の値。
    """

    def __init__(self, width: int, height: int, title: str = "Minilib"):
        """窓と画像を作る。

        窓が画面に収まらなければ、縦横比を保って縮める。

        Args:
            width: 窓の幅 (ピクセル)。
            height: 窓の高さ (ピクセル)。
            title: 窓のタイトル。

        Raises:
            ValueError: 幅か高さが0以下の場合。
            RuntimeError: X11 の表示先に接続できない場合や、MLX の初期化、
                窓や画像の作成に失敗した場合。
        """
        if width <= 0 or height <= 0:
            raise ValueError("窓の幅と高さは正にしてください")
        if not _display_available():
            raise RuntimeError("X11 の表示先に接続できません")
        self._mlx = Mlx()
        self._ptr = self._mlx.mlx_init()
        if not self._ptr:
            raise RuntimeError("MLX の初期化に失敗しました")
        _, screen_width, screen_height = (
            self._mlx.mlx_get_screen_size(self._ptr)
        )
        scale = min(1.0, max(1, screen_width - 400) / width,
                    max(1, screen_height - 100) / height)
        self.width = max(1, int(width * scale))
        self.height = max(1, int(height * scale))
        self._window = self._mlx.mlx_new_window(
            self._ptr, self.width, self.height, title,
        )
        if not self._window:
            self._mlx.mlx_release(self._ptr)
            raise RuntimeError("窓を作れませんでした")
        self._image = self._mlx.mlx_new_image(
            self._ptr, self.width, self.height,
        )
        if not self._image:
            self._mlx.mlx_destroy_window(self._ptr, self._window)
            self._mlx.mlx_release(self._ptr)
            raise RuntimeError("画像を作れませんでした")
        self._data, bits, self._stride, self._format = (
            self._mlx.mlx_get_data_addr(self._image)
        )
        if bits != 32:
            self._mlx.mlx_destroy_image(self._ptr, self._image)
            self._mlx.mlx_destroy_window(self._ptr, self._window)
            self._mlx.mlx_release(self._ptr)
            raise RuntimeError("32ビット画像が必要です")
        self._buffer = bytearray(self.height * self._stride)
        self._texts: list[tuple[int, int, str, int]] = []
        self._finished = False
        self._callback_error: BaseException | None = None
        self._key_callback: Callable[[int, object], int] | None = None
        self._key_handler: Callable[[str], None] | None = None
        self._loop_callback: Callable[[], None] | None = None
        self._loop_hook_installed = False
        self._pending_keys: dict[str, None] = {}
        self._expose_callback: Callable[[object], int] | None = None
        self._mlx.mlx_hook(self._window, 33, 0, self._on_close, None)

    def pixel(self, x: int, y: int, color: int) -> None:
        """1点を描く。窓の外は無視する。

        Args:
            x: 点の x 座標 (ピクセル)。
            y: 点の y 座標 (ピクセル)。
            color: 色 (0xRRGGBB。それより上位のビットは無視する)。
        """
        self.fill_rect(x, y, 1, 1, color)

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """横線・縦線を描く。始点と終点の両方を含む。

        Args:
            x0: 始点の x 座標 (ピクセル)。
            y0: 始点の y 座標 (ピクセル)。
            x1: 終点の x 座標 (ピクセル)。
            y1: 終点の y 座標 (ピクセル)。
            color: 色 (0xRRGGBB。それより上位のビットは無視する)。

        Raises:
            ValueError: 斜めの線を指定した場合。
        """
        if y0 == y1:
            self.fill_rect(min(x0, x1), y0, abs(x1 - x0) + 1, 1, color)
        elif x0 == x1:
            self.fill_rect(x0, min(y0, y1), 1, abs(y1 - y0) + 1, color)
        else:
            raise ValueError("line は横線・縦線に対応しています")

    def fill_rect(self, x: int, y: int, width: int, height: int,
                  color: int) -> None:
        """左上が (x, y) の四角を、行単位で画像バッファに塗る。

        窓からはみ出す部分は無視する。

        Args:
            x: 左上の x 座標 (ピクセル)。
            y: 左上の y 座標 (ピクセル)。
            width: 幅 (ピクセル)。
            height: 高さ (ピクセル)。
            color: 色 (0xRRGGBB。それより上位のビットは無視する)。
        """
        x0, x1 = max(0, x), min(self.width, x + width)
        y0, y1 = max(0, y), min(self.height, y + height)
        if x0 >= x1 or y0 >= y1:
            return
        red, green, blue = (color >> 16) & 255, (color >> 8) & 255, color & 255
        pixel = (bytes((blue, green, red, 255)) if self._format == 0
                 else bytes((red, green, blue, 255)))
        row = pixel * (x1 - x0)
        for py in range(y0, y1):
            start = py * self._stride + x0 * 4
            self._buffer[start:start + len(row)] = row

    def text(self, x: int, y: int, text: str, color: int) -> None:
        """画像を転送した後に描く文字を登録する。

        文字は画像ではなく窓に直接描くので、present() のたびに描き直す。
        clear() を呼ぶと消える。

        Args:
            x: 文字の x 座標 (ピクセル)。
            y: 文字の y 座標 (ピクセル)。
            text: 描く文字列。
            color: 色 (0xAARRGGBB)。
        """
        self._texts.append((x, y, text, color))

    def present(self) -> None:
        """描き終えた画像を窓に一度で転送し、登録した文字を描く。"""
        self._mlx.mlx_sync(
            self._ptr, self._mlx.SYNC_IMAGE_WRITABLE, self._image,
        )
        self._data[:] = self._buffer
        self._mlx.mlx_put_image_to_window(
            self._ptr, self._window, self._image, 0, 0,
        )
        for x, y, text, color in self._texts:
            self._mlx.mlx_string_put(
                self._ptr, self._window, x, y, color, text,
            )

    def _save_callback_error(self, error: BaseException) -> None:
        """フックの最初の例外を保存し、Python 側へ戻るためループを止める。

        Args:
            error: C へ返す前に捕捉した例外。
        """
        if self._callback_error is None:
            self._callback_error = error
            self._pending_keys.clear()
            self._loop_callback = None
            self.close()

    def _ensure_loop_hook(self) -> None:
        """入力をまとめて処理するフックを一度だけ登録する。"""
        if self._loop_hook_installed:
            return

        def handle_loop(param: object) -> int:
            """MLX のループから呼ばれ、溜まったキーと更新関数を処理する。

            q が溜まっていれば他のキーは捨てて q だけを処理し、
            更新関数も呼ばない。

            Args:
                param: MLX から渡される値 (使わない)。

            Returns:
                MLX に返す値。常に 0。
            """
            if self._callback_error is not None or self._finished:
                return 0
            try:
                pending = tuple(self._pending_keys)
                self._pending_keys.clear()
                if "q" in pending:
                    pending = ("q",)
                for key in pending:
                    if self._key_handler is not None:
                        self._key_handler(key)
                if "q" not in pending and self._loop_callback is not None:
                    self._loop_callback()
            except BaseException as error:
                # ctypes の境界では例外を送出せず、run() で送出し直す。
                # KeyboardInterrupt / SystemExit も同じ経路で処理する。
                self._save_callback_error(error)
            return 0

        self._native_loop_callback = handle_loop
        self._mlx.mlx_loop_hook(self._ptr, handle_loop, None)
        self._loop_hook_installed = True

    def on_loop(self, callback: Callable[[], None] | None) -> None:
        """ループのたびに呼ぶ更新関数を切り替える。

        None にしても、キー入力の処理は続ける。

        Args:
            callback: 引数なしで呼ぶ更新関数。None なら何も呼ばない。
        """
        self._loop_callback = callback
        self._ensure_loop_hook()

    def clear(self) -> None:
        """画像を背景色で塗りつぶし、登録した文字も消す。"""
        self.fill_rect(0, 0, self.width, self.height, BACKGROUND_COLOR)
        self._texts.clear()

    def on_key(self, callback: Callable[[str], None]) -> None:
        """キー入力で呼ぶ関数を登録する。

        キーはすぐには処理せず、次のループでまとめて処理する。同じキーの
        連打は1回にまとめる。Esc は q として扱う。更新関数が登録されている
        間は、q 以外のキーを無視する。

        Args:
            callback: 押されたキーの文字を受け取る関数。
        """
        self._key_handler = callback
        self._ensure_loop_hook()

        def handle_key(keycode: int, param: object) -> int:
            """MLX のキーフックから呼ばれ、キーを処理待ちに加える。

            Args:
                keycode: 押されたキーの X11 の keysym。
                param: MLX から渡される値 (使わない)。

            Returns:
                MLX に返す値。常に 0。
            """
            if self._callback_error is not None or self._finished:
                return 0
            try:
                if keycode == 65307:
                    self._pending_keys["q"] = None
                elif 32 <= keycode < 127:
                    key = chr(keycode)
                    if key == "q" or self._loop_callback is None:
                        self._pending_keys[key] = None
            except BaseException as error:
                self._save_callback_error(error)
            return 0

        self._key_callback = handle_key
        self._mlx.mlx_key_hook(self._window, handle_key, None)

    def on_expose(self, callback: Callable[[], None]) -> None:
        """窓の再表示が必要になったときに呼ぶ関数を登録する。

        Args:
            callback: 引数なしで呼ぶ関数。
        """
        def handle_expose(param: object) -> int:
            """MLX の expose フックから呼ばれ、callback を呼ぶ。

            Args:
                param: MLX から渡される値 (使わない)。

            Returns:
                MLX に返す値。常に 0。
            """
            if self._callback_error is not None or self._finished:
                return 0
            try:
                callback()
            except BaseException as error:
                self._save_callback_error(error)
            return 0

        self._expose_callback = handle_expose
        self._mlx.mlx_expose_hook(self._window, handle_expose, None)

    def close(self) -> None:
        """イベント待ちを終了する。後片付けは run() が行う。"""
        if not self._finished:
            self._mlx.mlx_loop_exit(self._ptr)

    def _on_close(self, param: object) -> int:
        """窓が閉じられたときに MLX から呼ばれ、イベント待ちを終了する。

        Args:
            param: MLX から渡される値 (使わない)。

        Returns:
            MLX に返す値。常に 0。
        """
        self.close()
        return 0

    def run(self, draw: Callable[[], None] | None = None) -> None:
        """イベントを待ち、終了後に窓と MLX の資源を解放する。

        Args:
            draw: イベント待ちの前に一度呼ぶ描画関数。None なら呼ばない。

        Raises:
            RuntimeError: 一度終了した窓で再び呼んだ場合。
            BaseException: フック内で発生した例外。資源を解放して送出する。
        """
        if self._finished:
            raise RuntimeError("終了した窓は再利用できません")
        try:
            if draw is not None:
                draw()
            self._mlx.mlx_loop(self._ptr)
            if self._callback_error is not None:
                raise self._callback_error
        finally:
            try:
                try:
                    self._mlx.mlx_destroy_image(self._ptr, self._image)
                finally:
                    self._mlx.mlx_destroy_window(self._ptr, self._window)
            finally:
                self._mlx.mlx_release(self._ptr)
                self._finished = True
