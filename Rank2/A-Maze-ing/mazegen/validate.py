#!/usr/bin/env python3

"""生成した迷路が要件を満たしているかを調べる。"""

import logging

from .grid import MIN_LOOPS, Grid, cycle_rank
from .maze import Coordinate, Maze
from .wall import ALL_WALLS, Wall

logger = logging.getLogger(__name__)


class InvalidMazeError(RuntimeError):
    """生成した迷路が要件を満たしていないことを表す例外。

    利用者の入力の誤り (ValueError) ではなく、生成の処理の不具合を表すので
    RuntimeError の子にしている。except ValueError で入力の誤りを受ける
    コードが、この例外まで一緒に受けてしまわないようにするため。
    単なる例外にとどめず、だめだった迷路をself.mazeとして持つので、デバッグに便利。
    なお、外部には公開しておらず、mazegen内部でもself.mazeは参照していない。

    Attributes:
        maze: 要件を満たしていない迷路。出口に到達できなければ path は ""。
        problems: 満たしていない要件の説明の一覧。
    """

    def __init__(self, maze: Maze, problems: list[str]) -> None:
        """例外を作る。メッセージは problems をつなげたものになる。

        Args:
            maze: 要件を満たしていない迷路。
            problems: 満たしていない要件の説明の一覧。
        """
        super().__init__("Invalid Maze: " + "; ".join(problems))
        self.maze = maze
        self.problems = problems


def _wall_problems(grid: Grid) -> list[str]:
    """壁の状態が正しくないセルを探す。

    隣り合うセルで壁の有無が食い違っていないか、外周の壁が閉じているか、
    「42」のセルの壁がすべて閉じているかを調べる。

    Args:
        grid: 調べるグリッド。

    Returns:
        見つかった問題の説明の一覧。問題がなければ空のリスト。
    """
    # 隣り合うセルで壁の有無が食い違っていないか、外周が閉じているか、
    # 「42」のセルがすべて閉じているかを見る
    problems: list[str] = []
    for y in range(grid.height):
        for x in range(grid.width):
            pos = Coordinate(x, y)
            if grid.is_blocked(pos) and grid.cells[y][x] != ALL_WALLS:
                problems.append(f"42 cell {tuple(pos)} is not closed")
            for direction in Wall:
                dx, dy = direction.delta
                other = Coordinate(x + dx, y + dy)
                if not grid.in_bounds(other):
                    if not grid.has_wall(pos, direction):
                        problems.append(
                            f"border {direction.name} of {tuple(pos)} is open"
                        )
                elif (grid.has_wall(pos, direction)
                      != grid.has_wall(other, direction.opposite)):
                    problems.append(
                        f"{direction.name} wall of {tuple(pos)} "
                        f"does not match its neighbour"
                    )
    return problems


def find_problems(grid: Grid, is_perfect: bool) -> list[str]:
    """迷路が満たしていない要件をエラーメッセージのlistとしてすべて返す。

    壁の整合性、連結性、3x3 の広場がないこと、閉路の数を調べる。
    is_perfect が False なら、Pac-Man の盤面として使えるかも調べる。

    Args:
        grid: 調べるグリッド。
        is_perfect: True なら完全迷路 (閉路なし) として、False なら
            完全でない迷路 (閉路が MIN_LOOPS 個以上) として調べる。

    Returns:
        満たしていない要件の説明の一覧。迷路が有効なら空のリスト。
    """
    problems = _wall_problems(grid)
    # 連結性: 「42」以外のすべてのセルが1つにつながっている
    # 連結成分数と閉路の数は同じグラフから求まるので、計算は一度だけにする
    vertices, edges, components = grid.connectivity_parameters()
    loops = cycle_rank(vertices, edges, components)
    logger.debug(
        "v, e, c: %d, %d, %d / loops: %d", vertices, edges, components, loops
    )
    if components != 1:
        problems.append(f"not connected: {components} components")
    # 3x3 の広場がない
    problems.extend(
        f"3x3 open area at {tuple(pos)}"
        for pos in grid.positions() if grid.is_open_area(pos)
    )
    # 閉路の数: 完全迷路なら0、そうでなければ2以上
    if is_perfect and loops != 0:
        problems.append(f"perfect maze has {loops} loops")
    if not is_perfect and loops < MIN_LOOPS:
        problems.append(f"imperfect maze has only {loops} loops")
    if not is_perfect:
        problems.extend(_board_problems(grid))
    return problems


def _board_problems(grid: Grid) -> list[str]:
    """完全でない迷路が Pac-Man の盤面として使えない理由を返す。

    四隅と中央が「42」で塞がれていないか、壊せるのに残っている
    行き止まりがないかを調べる。

    Args:
        grid: 調べるグリッド。

    Returns:
        見つかった問題の説明の一覧。問題がなければ空のリスト。
    """
    # PERFECT=False の迷路は Pac-Man の盤面として使える必要がある:
    # 四隅と中央が通路 (「42」で塞がれていない) で、行き止まりが1つもない
    # 壁はセルの間の線でセルはすべて通路なので、「通路である」とは
    # 「42」で塞がれていないことを指す。「42」の置き方 (maze_generator の
    # _fortytwo_gap) から中央・四隅が塞がれることはないが、念のため確かめる
    # ただし、閉じた壁の先がすべて「42」か外周である行き止まりは
    # 壊しようがないので数えない (maze_analyzer.py の "enclosed" と同じ扱い)
    problems: list[str] = []
    problems.extend(
        f"corner {tuple(pos)} is on the 42"
        for pos in sorted(grid.corners)
        if grid.is_blocked(pos)
    )
    centre = grid.centre
    if all(grid.is_blocked(pos) for pos in centre):
        problems.append(f"centre {sorted(map(tuple, centre))} is on the 42")
    problems.extend(
        f"dead end at {tuple(pos)}"
        for pos in grid.positions()
        if grid.is_deadend(pos) and len(list(grid.neighbors(pos))) > 1
    )
    return problems
