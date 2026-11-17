#!/usr/bin/env python3

"""迷路を端末に ASCII アートで表示する。"""

# 迷路が端末より大きいときは、端末に収まる範囲 (Viewport) だけを描き、
# 矢印キーでその範囲を動かす。そのまま全部 print すると、端末の幅を
# 超えた行が折り返されて表示が崩れるため。

import shutil
import sys
from typing import NamedTuple

from mazegen import Coordinate, Wall
from mazegen.wall import ALL_WALLS

from .controller import Controller
from .palette import FORTYTWO_COLOR, RGB
from .scene import Scene, build_scene
from .terminal import (
    ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT, ARROW_UP, alternate_screen,
    clear_screen, get_key,
)

CORNER: str = "+"
HORIZONTAL: str = "---"
VERTICAL: str = "|"
LONGSPACE: str = "   "
SPACE: str = " "

ENTRY_MARK: str = " S "
EXIT_MARK: str = " G "
PATH_MARK: str = " # "
FORTYTWO_MARK: str = " @ "

# ANSI エスケープシーケンス(man 4 console_codes):
#   "\033"はESCに対応する(man 7 asciiの通り)
#   ターミナルは ESC で始まる文字列を命令として解釈する
# ECMA-48 Select Graphic Rendition
#    38          256/24-bit foreground color follows
#      ;2;r;g;b  24-bit color, r/g/b components are in the range 0..255
# 色は palette が RGB で持っているので、38;2;r;g;b でそのまま指定する。
# (Linux のコンソールのように 24bit カラーを出せない端末では、近い色に丸められる)
RESET: str = "\033[0m"

# palette の FORTYTWO_COLOR は MLX 向けの 0xAARRGGBB の整数なので、
# 端末で使うために RGB に分解しておく (色の定義は palette の1か所のまま)
FORTYTWO_RGB: RGB = (
    (FORTYTWO_COLOR >> 16) & 0xFF,
    (FORTYTWO_COLOR >> 8) & 0xFF,
    FORTYTWO_COLOR & 0xFF,
)

# 迷路が端末に収まらないとき、矢印キーで見る範囲を1セルずつ動かす。
# 値は (列の増分, 行の増分)。
SCROLL_KEYS: dict[str, tuple[int, int]] = {
    ARROW_UP: (0, -1),
    ARROW_DOWN: (0, 1),
    ARROW_LEFT: (-1, 0),
    ARROW_RIGHT: (1, 0),
}

# 迷路の下に表示する説明の行数 (操作の説明 + スクロールの説明)
HELP_LINES: int = 2


def colorize(text: str, color: RGB | None) -> str:
    """text を 24bit カラーの ANSI エスケープシーケンスで挟んで色を付ける。

    Args:
        text: 色を付ける文字列。
        color: 色の RGB。None なら色を付けない。

    Returns:
        色を付けた文字列。color が None なら text そのもの。
    """
    # 「色を付ける命令 + 文字 + 元に戻す命令」で挟む。
    # RESET で戻さないと、後ろの文字まで全部その色になってしまう。
    if color is None:
        return text
    red, green, blue = color
    return f"\033[38;2;{red};{green};{blue}m{text}{RESET}"


class CellGlyphs(NamedTuple):
    """セルの4辺それぞれに描く文字。

    壁が閉じていれば壁の文字、開いていれば同じ幅の空白になる。

    Attributes:
        north: 北 (上) の辺。HORIZONTAL か LONGSPACE。
        east: 東 (右) の辺。VERTICAL か SPACE。
        south: 南 (下) の辺。HORIZONTAL か LONGSPACE。
        west: 西 (左) の辺。VERTICAL か SPACE。
    """

    north: str
    east: str
    south: str
    west: str


class Viewport(NamedTuple):
    """迷路のうち画面に描くセルの範囲。

    Attributes:
        x: 左端のセルの列。
        y: 上端のセルの行。
        width: 描く列数。
        height: 描く行数。
    """

    x: int
    y: int
    width: int
    height: int


def cell_display(cell: int) -> CellGlyphs:
    """セルの4辺それぞれに描く文字を返す。

    Args:
        cell: セルの壁のフラグ。

    Returns:
        各辺の文字。
    """
    # 横の壁は HORIZONTAL "---" (セル幅3文字)、縦の壁は VERTICAL "|" (1文字)。
    # 壁がなければ同じ幅の空白にして、横の位置がずれないようにする。
    north: str = HORIZONTAL if Wall.has_wall(cell, Wall.NORTH) else LONGSPACE
    east: str = VERTICAL if Wall.has_wall(cell, Wall.EAST) else SPACE
    south: str = HORIZONTAL if Wall.has_wall(cell, Wall.SOUTH) else LONGSPACE
    west: str = VERTICAL if Wall.has_wall(cell, Wall.WEST) else SPACE

    return CellGlyphs(north=north, east=east, south=south, west=west)


def _paint(glyph: str, filled: str, color: RGB | None) -> str:
    """glyph が壁の文字なら色を付ける。

    Args:
        glyph: CellGlyphs の各辺の文字。
        filled: 壁が閉じているときの文字。
        color: 色の RGB。None なら色を付けない。

    Returns:
        glyph が filled と同じなら色を付けたもの、そうでなければ glyph。
    """
    # 壁のある部分だけに色を付ける (空白に色を付けても見えないので無駄)
    return colorize(glyph, color) if glyph == filled else glyph


def _cell_fill(pos: Coordinate, scene: Scene) -> str:
    """セルの中に描く3文字の記号を返す。

    Args:
        pos: 描くセル。
        scene: 描いている内容。

    Returns:
        入口なら ENTRY_MARK、出口なら EXIT_MARK、経路上なら色を付けた
        PATH_MARK、「42」のセルなら色を付けた FORTYTWO_MARK、
        それ以外なら空白。
    """
    if pos == scene.maze.entry:
        return ENTRY_MARK
    if pos == scene.maze.exit:
        return EXIT_MARK
    if pos in scene.path_cells:
        return colorize(PATH_MARK, scene.path_color)
    # 「42」のセルは四方の壁がすべて閉じている (MLX と同じ見分け方)
    if scene.maze.cells[pos.y][pos.x] == ALL_WALLS:
        return colorize(FORTYTWO_MARK, FORTYTWO_RGB)
    return LONGSPACE


def render(scene: Scene, view: Viewport | None = None) -> str:
    """scene の迷路のうち、view の範囲を ASCII アートにする。

    Args:
        scene: 描く内容。
        view: 描くセルの範囲。None なら迷路全体。

    Returns:
        迷路の各行を改行でつないだ文字列。末尾に改行は付けない。
    """
    # print せずに文字列を返すので、描画の中身だけをテストできる
    maze = scene.maze
    if view is None:
        view = Viewport(0, 0, maze.width, maze.height)
    wall_color = scene.wall_color
    lines: list[str] = []

    # 色の付いた文字列を後から切り取ると ANSI エスケープシーケンスの
    # 途中で切れてしまうので、描く前にセルの範囲で切り取っておく
    rows = [
        row[view.x:view.x + view.width]
        for row in maze.cells[view.y:view.y + view.height]
    ]

    # 隣り合うセルは壁を共有しているので、描くのは北と西だけでよい。
    # 例外は右端 (東) と最下段 (南) で、これはループの外で別に描く。
    # (範囲の端で切ったときも、端のセルの東・南の壁がそのまま枠になる)
    for y, row in enumerate(rows, start=view.y):
        top: str = ""
        middle: str = ""

        for x, cell in enumerate(row, start=view.x):
            glyphs = cell_display(cell)
            north = _paint(glyphs.north, HORIZONTAL, wall_color)
            west = _paint(glyphs.west, VERTICAL, wall_color)

            top += CORNER + north
            middle += west + _cell_fill(Coordinate(x, y), scene)

        # 行の右端: 角を閉じ、最後のセルの東の壁を足す
        top += CORNER
        middle += _paint(cell_display(row[-1]).east, VERTICAL, wall_color)

        lines.append(top)
        lines.append(middle)

    # 迷路の一番下: 最下段の各セルの南の壁を描く
    bottom: str = ""

    for cell in rows[-1]:
        south = _paint(cell_display(cell).south, HORIZONTAL, wall_color)
        bottom += CORNER + south

    bottom += CORNER
    lines.append(bottom)
    return "\n".join(lines)


def run(controller: Controller) -> None:
    """終了の操作が行われるまで、端末に迷路を表示する。

    キーが押されるたびに controller に渡し、画面を描き直す。

    Args:
        controller: 表示する状態を持ち、キーに対応する操作を実行する。

    Raises:
        termios.error: 標準入力が端末でない場合。
    """
    # 「画面を消す → 描く → キーを1つ待つ → 状態を変える」を繰り返す。
    # 画面を部分的に書き換えるのではなく、毎回まるごと描き直している。
    # どのキーが何をするかは controller が知っていて、ここはキーを渡すだけ。
    #
    # 例外はスクロール (矢印キー) で、これだけはここで処理する。
    # 「どこを見ているか」は端末に描くときだけの事情なので、
    # MLX と共通の controller (ViewState) には持たせない。
    # 代替スクリーンに描くので、表示の前に stderr に出た警告
    # (小さい迷路で「42」を省いたときなど) は、終了後に元の画面で読める
    with alternate_screen():
        left, top = 0, 0
        while controller.state.running:
            maze = controller.state.maze
            view = fit_view(maze.width, maze.height, left, top)
            # 再生成で迷路が小さくなった場合などに備え、丸めた位置を覚えておく
            left, top = view.x, view.y

            clear_screen()
            print(render(build_scene(controller.state), view))
            # 最後の行は改行しない。改行すると、ちょうど画面いっぱいのときに
            # 1行スクロールして迷路の一番上が見えなくなる
            print(controller.help_text(), end="")
            if (view.width, view.height) != (maze.width, maze.height):
                scroll = scroll_text(view, maze.width, maze.height)
                print("\n" + scroll, end="")
            sys.stdout.flush()

            # Enter なしでキーを1つ読む (ここでキー入力を待って止まる)
            key = get_key()
            if key in SCROLL_KEYS:
                dx, dy = SCROLL_KEYS[key]
                left, top = left + dx, top + dy
            else:
                controller.dispatch(key)


def fit_view(
    maze_width: int, maze_height: int, left: int, top: int
) -> Viewport:
    """端末に収まる大きさで、左上が (left, top) の表示範囲を返す。

    Args:
        maze_width: 迷路の列数。
        maze_height: 迷路の行数。
        left: 表示したい左端の列。範囲外なら収まるように丸める。
        top: 表示したい上端の行。範囲外なら収まるように丸める。

    Returns:
        迷路からはみ出さず、端末にも収まる範囲。
    """
    # 端末の大きさは毎回取り直すので、窓の大きさを変えても
    # 次にキーを押したときの描き直しで合わせられる
    columns, lines = shutil.get_terminal_size()

    # 横: 1セル4文字 ("+---" / "|   ") + 右端の1文字 → 4 * width + 1 <= columns
    # 縦: 1セル2行 + 最下段の1行 + 説明の行 → 2 * height + 1 + HELP_LINES <= lines
    # 端末がとても小さくても、最低1セルは描く
    width = min(maze_width, max(1, (columns - 1) // 4))
    height = min(maze_height, max(1, (lines - 1 - HELP_LINES) // 2))

    # 迷路の外を見ないように、左上の位置を 0 〜 (迷路 - 表示範囲) に収める
    left = min(max(left, 0), maze_width - width)
    top = min(max(top, 0), maze_height - height)
    return Viewport(left, top, width, height)


def scroll_text(view: Viewport, maze_width: int, maze_height: int) -> str:
    """スクロールの操作と、いま見ている範囲の説明を返す。

    Args:
        view: いま表示している範囲。
        maze_width: 迷路の列数。
        maze_height: 迷路の行数。

    Returns:
        "[arrows] scroll  x 0-19/50  y 0-9/30" のような文字列。
    """
    return (
        f"[arrows] scroll  "
        f"x {view.x}-{view.x + view.width - 1}/{maze_width}  "
        f"y {view.y}-{view.y + view.height - 1}/{maze_height}"
    )
