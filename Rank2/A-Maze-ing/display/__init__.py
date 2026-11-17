#!/usr/bin/env python3

"""迷路を表示し、利用者の操作を受け付ける。

使い方（利用者が知っておくのは run() だけ）::

    import display

    display.run(maze, regenerate=callback, backend="ascii")

構成
    palette        色の名前と順番（バックエンド非依存）
    controller     ViewState と Command 群、キー -> Command の表（Controller）
    scene          ViewState -> Scene（何を描くか）
    terminal       端末の低レベル I/O（Unix 専用）
    display_ascii  Scene を ASCII で描き、端末でキーを読むバックエンド
    display_mlx    Scene を MiniLibX の窓に描き、キーフックで受けるバックエンド

バックエンドはどれも run(controller) を持つ。どれを使うかはここで選ぶ
（Simple Factory）。選ばれた側だけを import するので、MLX が入っていない
環境でも ASCII 表示は使える。
"""

import logging
from collections.abc import Callable

from mazegen import Maze

from .controller import make_controller

logger = logging.getLogger(__name__)

# "auto": MLX を試し、使えなければ ASCII に切り替える
BACKENDS: tuple[str, ...] = ("auto", "mlx", "ascii")


def run(
    maze: Maze,
    regenerate: Callable[[], Maze],
    backend: str = "ascii",
) -> None:
    """利用者が終了するまで、指定したバックエンドで迷路を表示する。

    キー操作: r で再生成 (regenerate を呼ぶ)、p で最短経路の表示切り替え、
    c で壁の色の切り替え、q で終了。

    Args:
        maze: 最初に表示する迷路。
        regenerate: r が押されたときに引数なしで呼ぶ関数。新しい迷路を返す。
        backend: "ascii" なら端末、"mlx" なら MiniLibX の窓に表示する。
            "auto" なら MLX を試し、使えなければ ASCII に切り替える。

    Raises:
        ValueError: backend が BACKENDS のいずれでもない場合。
        ImportError: backend が "mlx" で、mlx が入っていない場合。
        RuntimeError: backend が "mlx" で、窓を開けない場合
            (X11 の表示先に接続できないなど)。
    """
    if backend not in BACKENDS:
        raise ValueError(f"unknown display backend: {backend!r}")
    controller = make_controller(maze, regenerate)

    if backend in ("auto", "mlx"):
        try:
            from .display_mlx import DisplayUnavailableError, run as run_mlx
        except ImportError as error:
            # MLX を指定されたときは、使えないことをそのままエラーにする
            if backend == "mlx":
                raise
            logger.warning("%s; falling back to ASCII", error)
        else:
            try:
                run_mlx(controller)
                return
            except DisplayUnavailableError as error:
                if backend == "mlx":
                    raise
                logger.warning("%s; falling back to ASCII", error)

    from .display_ascii import run as run_ascii
    run_ascii(controller)


__all__ = ["BACKENDS", "run"]
