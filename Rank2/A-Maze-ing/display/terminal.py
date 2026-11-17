#!/usr/bin/env python3

"""端末の低レベルな入出力 (Unix 専用)。"""

import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager

ESC: str = "\033"

# 矢印キーを押したときに端末から届くエスケープシーケンス
ARROW_UP: str = ESC + "[A"
ARROW_DOWN: str = ESC + "[B"
ARROW_RIGHT: str = ESC + "[C"
ARROW_LEFT: str = ESC + "[D"

# 1回の os.read で読む最大バイト数。エスケープシーケンスが収まれば十分
_READ_SIZE: int = 8


@contextmanager
def alternate_screen() -> Iterator[None]:
    """with の中だけ、端末を代替スクリーンに切り替える。

    with を抜けると元の画面に戻り、切り替える前の表示がそのまま残る。
    """
    # 端末には「通常の画面」と「代替スクリーン」の2枚の画面がある。
    # less や vim は代替スクリーンに描くので、終わるとシェルの画面が元に戻る。
    #   "\033[?1049h": 代替スクリーンに切り替える (h = set)
    #   "\033[?1049l": 通常の画面に戻る (l = reset)
    # 迷路は代替スクリーンの側で消したり描いたりするので、
    # 表示の前に stderr に出た警告は通常の画面に残り、終了後に読める。
    # (ただし、表示中に出力したものは代替スクリーンと一緒に消える)
    print("\033[?1049h", end="", flush=True)
    try:
        yield
    finally:
        # Ctrl+C や例外で抜けたときも必ず戻す。
        # 戻さないと、シェルが代替スクリーンのまま残ってしまう。
        print("\033[?1049l", end="", flush=True)


def clear_screen() -> None:
    """端末の画面を消し、カーソルを左上に移す。"""
    # "\033[H": カーソルを左上 (1行目1列目) に移動する命令
    # "\033[J": カーソル位置から画面の最後までを消去する命令
    # 2つ合わせて「画面を消して左上から書き直す」になる。
    # end="" は print が最後に付ける改行を付けないため。
    print("\033[H\033[J", end="")


def get_key() -> str:
    """Enter を待たずに、押されたキーを1つ読む。

    読む間だけ端末を cbreak モードにし、読み終わったら元の設定に戻す。

    Returns:
        読んだキー。普通のキーなら1文字、矢印キーなら "\\033[A" のような
        エスケープシーケンス (ARROW_UP などの定数と比べられる)。
        入力が終わっていれば ""。

    Raises:
        termios.error: 標準入力が端末でない場合。
    """
    # --- 前提: ターミナルの「行バッファリング」---
    # ターミナルは普段「カノニカルモード」で動いている。
    # このモードでは、打った文字はターミナル（正確には OS の端末ドライバ）が
    # ため込み、Enter が押されて初めてプログラムに1行分まとめて渡す。
    # Backspace で文字を消せるのは、この段階でドライバが編集しているから。
    # そのため普通の input() や sys.stdin.read(1) は Enter まで待たされる。
    #
    # キーを押した瞬間に反応したいので、一時的にこのモードを切り、
    # 読み終わったら必ず元に戻す、というのがこの関数の流れ。
    #
    # termios: 端末ドライバの設定を読み書きする低レベルなモジュール
    # tty:     termios を使ったよくある設定をまとめた便利モジュール
    # どちらも Unix (Linux/macOS) 専用。Windows にはないので、
    # ファイルの先頭ではなくここで import している
    # (この関数が呼ばれない限り、import エラーにならない)。
    import termios
    import tty

    fd = sys.stdin.fileno()
    # 現在の端末設定をまるごと保存しておく (後で元に戻すため)
    old_settings = termios.tcgetattr(fd)
    try:
        # cbreak モードに切り替える:
        #   - Enter を待たず、1文字打つごとにすぐプログラムに渡す
        #   - 打った文字を画面に表示しない (エコーしない)
        #   - Ctrl+C は引き続き有効 (似た raw モードでは無効になる)
        tty.setcbreak(fd)
        # 矢印キーは1文字ではなく、ESC [ A のような3バイトで届く。
        # sys.stdin.read(1) だと最初の ESC しか読めず、残りの "[A" が
        # 次の2回のキー入力として扱われてしまう。
        # そこで os.read で「いま届いているバイト」をまとめて読む。
        # 1回のキー押下で送られるバイトはふつう一度に届くので、
        # 矢印キーなら3バイト、普通のキーなら1バイトが返ってくる。
        # (sys.stdin は内部にバッファを持つので、os.read と混ぜて使わない)
        # キーが押されるまでここで止まる。
        data = os.read(fd, _READ_SIZE)
        key = data.decode(errors="replace")
        # ESC で始まらないのに複数文字ある (貼り付けなど) ときは、
        # 今までどおり先頭の1文字だけを返す
        return key if key.startswith(ESC) else key[:1]
    finally:
        # return の後でも、例外 (Ctrl+C など) が起きても、finally は必ず走る。
        # ここで元の設定に戻さないと、プログラム終了後もシェルが
        # 「打った文字が見えない」「Enter が効かない」ような壊れた状態になる。
        # (もしそうなったら、見えないまま `reset` と打って Enter で直る)
        # TCSADRAIN: 出力待ちの文字を全部出し切ってから設定を変える、の意味
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
