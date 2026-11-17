#!/usr/bin/env python3

"""迷路の生成の入口となる MazeGenerator を定義する。"""

import logging
import warnings
from collections import deque
from random import Random

from . import braid, validate
from .algorithms import ALGORITHMS, AVAILABLE_ALGORITHMS, DEFAULT_ALGORITHM
from .grid import Grid
from .maze import Coordinate, Maze
from .validate import InvalidMazeError

logger = logging.getLogger(__name__)

# 「42」の模様。「4」と「2」を別々に持ち、間の空き列の数を幅の偶奇で変える
_FORTY_CELL_SET: list[str] = [
    "#..",
    "#..",
    "###",
    "..#",
    "..#"
]

_TWO_CELL_SET: list[str] = [
    "###",
    "..#",
    "###",
    "#..",
    "###"
]

# 模様の高さと、「4」「2」それぞれの幅
_FORTYTWO_HEIGHT: int = len(_FORTY_CELL_SET)
_DIGIT_WIDTH: int = len(_FORTY_CELL_SET[0])


def _fortytwo_gap(width: int) -> int:
    """「4」と「2」の間に空ける列数を返す。

    Args:
        width: 迷路の列数。

    Returns:
        width が奇数なら 1、偶数なら 2。
    """
    # 中央の列は、幅が奇数なら1列、偶数なら真ん中の2列 (grid.centre_cells)。
    # 空き列の数をそれに合わせると、模様が左右ちょうど中央に来て、
    # 空き列がそのまま中央の列になる。そのため中央のセルが「42」に
    # 塞がれることがない (Pac-Man の「中央が通路」の条件)。
    return 1 if width % 2 else 2


def _fortytwo_width(width: int) -> int:
    """迷路の幅が width のときの「42」の模様の幅を返す。

    Args:
        width: 迷路の列数。

    Returns:
        「4」と「2」の幅に、間の空き列の数を足したもの (7 か 8)。
    """
    return 2 * _DIGIT_WIDTH + _fortytwo_gap(width)


def _fortytwo_cells(width: int, height: int) -> set[Coordinate]:
    """迷路の中央に「42」を描くセルを返す。

    模様は高さ5マスで、幅は迷路の幅が奇数なら7マス、偶数なら8マス。
    迷路に「42」が入る大きさかどうかは、呼び出し側で確かめる。

    Args:
        width: 迷路の列数。
        height: 迷路の行数。

    Returns:
        「42」を描くセルの集合。
    """
    top = (height - _FORTYTWO_HEIGHT) // 2
    left = (width - _fortytwo_width(width)) // 2
    # 「2」は「4」の右に、空き列の数だけ離して置く
    two_left = left + _DIGIT_WIDTH + _fortytwo_gap(width)
    return {
        Coordinate(digit_left + x, top + y)
        for digit_left, digit in ((left, _FORTY_CELL_SET),
                                  (two_left, _TWO_CELL_SET))
        for y, row in enumerate(digit)
        for x, char in enumerate(row)
        if char == "#"
    }


def _is_connected_without(
    width: int, height: int, blocked: set[Coordinate]
) -> bool:
    """blocked 以外のセルが1つにつながっているかを返す。

    壁は無視し、隣り合うセルはすべてつながっているとみなして調べる。

    Args:
        width: 迷路の列数。
        height: 迷路の行数。
        blocked: 除外するセルの集合。

    Returns:
        1つにつながっていれば True。残るセルがなければ False。
    """
    # 壁を無視して、ブロックされていないセルが1つにつながるかを幅優先探索で見る
    # つながっていれば、どのアルゴリズムでもすべてのセルを覆う迷路を掘れる
    grid = Grid(width, height)
    for cell in blocked:
        grid.block(cell)
    cells = list(grid.positions())
    if not cells:
        return False
    seen: set[Coordinate] = {cells[0]}
    queue: deque[Coordinate] = deque([cells[0]])
    while queue:
        pos = queue.popleft()
        for _, other in grid.neighbors(pos):
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(cells)


def _solve_maze(grid: Grid, entry: Coordinate, exit_: Coordinate) -> str:
    """入口から出口までの最短経路を幅優先探索で求める。

    Args:
        grid: 掘り終えたグリッド。
        entry: 入口のセル。
        exit_: 出口のセル。

    Returns:
        最短経路。各一歩の方向を N, E, S, W で表した文字列。

    Raises:
        ValueError: 入口から出口に到達できない場合。
    """
    # 各セルには直前のセルだけを保存し、経路文字列を最後に一度作る。
    parents: dict[Coordinate, tuple[Coordinate, str] | None] = {entry: None}
    queue: deque[Coordinate] = deque([entry])
    while queue:
        pos = queue.popleft()
        if pos == exit_:
            letters: list[str] = []
            while parents[pos] is not None:
                previous = parents[pos]
                assert previous is not None
                pos, letter = previous
                letters.append(letter)
            return "".join(reversed(letters))
        for direction, other in grid.open_neighbors(pos):
            if other in parents:
                continue
            parents[other] = (pos, direction.letter)
            queue.append(other)
    raise ValueError("No Path from Entry to Exit.")


class MazeGenerator:
    """迷路の生成の入口となるクラス (Facade)。

    パラメータの確認と「42」の配置は作成時に済ませ、generate_maze() を
    呼ぶたびに新しい迷路を作る。同じ seed なら、同じ順に同じ迷路が作られる。

    Example:
        >>> gen = MazeGenerator(20, 15, (0, 0), (19, 14), True, seed=42)
        >>> maze = gen.generate_maze()
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry_coordinate: Coordinate | tuple[int, int],
        exit_coordinate: Coordinate | tuple[int, int],
        is_perfect: bool,
        algorithm: str = DEFAULT_ALGORITHM,
        seed: int | None = None
    ) -> None:
        """パラメータを確かめ、「42」を置く位置を決める。

        「42」が入らない大きさや、「42」で残りのセルが分断される大きさでは、
        「42」を省いて警告を出す。

        Args:
            width: 迷路の列数。
            height: 迷路の行数。
            entry_coordinate: 入口のセル。(x, y) のタプルでもよい。
            exit_coordinate: 出口のセル。(x, y) のタプルでもよい。
            is_perfect: True なら完全迷路 (入口から出口への道がちょうど
                1つ)、False なら閉路を持つ迷路を作る。
            algorithm: 迷路を掘るアルゴリズムの名前。
                AVAILABLE_ALGORITHMS のいずれか。
            seed: 乱数の種。None なら実行ごとに異なる迷路になる。

        Raises:
            ValueError: 幅か高さが負の場合、閉路を2つ作れない大きさで
                is_perfect が False の場合、入口と出口が同じ・迷路の外・
                「42」の上にある場合、またはアルゴリズム名が不明な場合。

        Warns:
            UserWarning: 「42」を省いた場合。
        """
        # plain (x, y) tuples are accepted too
        entry = Coordinate(*entry_coordinate)
        exit_ = Coordinate(*exit_coordinate)
        # negative value
        if width < 0 or height < 0:
            raise ValueError("Invalid Parameter for Maze: less than zero.")
        # PERFECT=False には閉路が2つ以上要る
        # 42 がない迷路で作れる閉路は最大 (width - 1) * (height - 1) 個
        # 幅か高さが1、または 2x2では原理的に作れない
        if not is_perfect and (
            width < 2 or height < 2 or (width, height) == (2, 2)
        ):
            raise ValueError(
                "Maze cannot have two loops."
            )
        fortytwo: set[Coordinate] = set()
        if height >= _FORTYTWO_HEIGHT and width >= _fortytwo_width(width):
            fortytwo = _fortytwo_cells(width, height)
        # in case the maze size does not allow "42":
        # 42 が入らないか、42 で残りのセルが分断される
        # (模様の幅・高さちょうどの迷路。結果として幅 8 以下か高さ 5 以下)
        # 分断されない大きさでは、42 は四隅にも中央にもかからない
        if not fortytwo or not _is_connected_without(width, height, fortytwo):
            # stacklevel=2: 警告の発生場所として MazeGenerator(...) を呼んだ行を示す
            warnings.warn(
                "Not Enough Space for Maze: 42 is left out.", stacklevel=2
            )
            fortytwo = set()
        # 入口と出口が一致してるならエラー処理
        if entry == exit_:
            raise ValueError("Entry and Exit Must Be Different.")
        # 入口or出口が迷宮からはみだしていればエラー処理
        if any(
            not (0 <= point.x < width and 0 <= point.y < height)
            for point in (entry, exit_)
        ):
            raise ValueError("Invalid Parameter for Maze.")
        # 入口or出口が「42」と重複していたら
        if entry in fortytwo or exit_ in fortytwo:
            raise ValueError("Entry and Exit Must Not Be on the 42.")
        # アルゴリズムのエラー処理
        if algorithm not in ALGORITHMS:
            raise ValueError(
                f"Unknown Algorithm {algorithm!r}: "
                f"choose from {', '.join(AVAILABLE_ALGORITHMS)}"
            )
        self.__width = width
        self.__height = height
        self.__entry = entry
        self.__exit = exit_
        self.__is_perfect = is_perfect
        self.__fortytwo = fortytwo
        self.__algorithm = algorithm
        self.__carve = ALGORITHMS[algorithm]
        self.__rng = Random(seed)

    def _carve_grid(self) -> Grid:
        """新しいグリッドを作り、アルゴリズムで迷路を掘る。

        is_perfect が False なら、続けて閉路を足す。要件を満たすかどうかは
        ここでは確かめない。

        Returns:
            掘り終えたグリッド。
        """
        grid = Grid(self.__width, self.__height)
        for cell in self.__fortytwo:
            grid.block(cell)
        logger.debug("carve with %s", self.__algorithm)
        self.__carve(grid, self.__rng)
        if not self.__is_perfect:
            braid.make_imperfect(grid, self.__entry, self.__rng)
        return grid

    def generate_maze(self) -> Maze:
        """新しい迷路を生成して返す。

        乱数を用いており、呼ぶたびに異なる迷路になる。

        Returns:
            壁・入口・出口・最短経路・生成過程をまとめた Maze。

        Raises:
            InvalidMazeError: 生成した迷路が要件を満たしていない場合。
                例外の maze 属性で、その迷路を調べられる。
        """
        grid = self._carve_grid()
        # 生成後に有効性を判定
        problems = validate.find_problems(grid, self.__is_perfect)
        if problems:
            # 無効な迷路も例外に持たせ、呼び出し側で調べられるようにする
            try:
                path = _solve_maze(grid, self.__entry, self.__exit)
            except ValueError:
                # 無効な迷路は経路が空
                path = ""
            raise InvalidMazeError(
                Maze(
                    cells=[row[:] for row in grid.cells],
                    entry=self.__entry,
                    exit=self.__exit,
                    path=path,
                    steps=tuple(grid.steps)
                ),
                problems
            )
        return Maze(
            cells=[row[:] for row in grid.cells],
            entry=self.__entry,
            exit=self.__exit,
            path=_solve_maze(grid, self.__entry, self.__exit),
            steps=tuple(grid.steps)
        )
