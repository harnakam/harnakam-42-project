#!/usr/bin/env python3

"""生成途中の迷路のセルを扱う。"""

from collections import deque
from collections.abc import Iterator

from .maze import Coordinate, WallChange
from .wall import ALL_WALLS, Wall

#   +  +  +  +
#      |  |
#   +--+--+--+
#      |  |
#   +--+--+--+
#      |  |
#   +  +  +  +

INVALID_ROOM: list[list[int]] = [
    [6, 14, 12],
    [7, 15, 13],
    [3, 11, 9]
]


# PERFECT=False の迷路に要求される、独立した閉路の最小数
MIN_LOOPS = 2


def cycle_rank(vertices: int, edges: int, components: int) -> int:
    """グラフの独立した閉路の数 (巡回数) を返す。

    Args:
        vertices: 頂点数。
        edges: 辺数。
        components: 連結成分数。

    Returns:
        辺数 - 頂点数 + 連結成分数。森 (閉路のないグラフ) なら 0。
    """
    return edges - vertices + components


def corner_cells(width: int, height: int) -> set[Coordinate]:
    """迷路の四隅のセルを返す。

    Args:
        width: 迷路の列数。
        height: 迷路の行数。

    Returns:
        四隅のセルの集合。幅か高さが1なら重なるので4つより少なくなる。
    """
    return {
        Coordinate(x, y)
        for x in (0, width - 1)
        for y in (0, height - 1)
    }


def centre_cells(width: int, height: int) -> set[Coordinate]:
    """迷路の中央のセルを返す。

    幅・高さが奇数ならその方向の中央は1マス、偶数なら真ん中の2マスとする。

    Args:
        width: 迷路の列数。
        height: 迷路の行数。

    Returns:
        中央のセルの集合 (1, 2 または 4 マス)。
    """
    # 奇数なら中央は1マス。偶数なら真ん中の2列(行)のどちらも中央とみなす
    # (maze_analyzer.py と同じ扱い)
    return {
        Coordinate(x, y)
        for x in {(width - 1) // 2, width // 2}
        for y in {(height - 1) // 2, height // 2}
    }


class Grid:
    """生成途中の迷路。セルの壁の状態と、壁の変更の記録を持つ。

    壁は open_wall() と close_wall() でだけ変更し、変更はすべて steps に
    記録する。

    Attributes:
        width: 列数。
        height: 行数。
        cells: 各セルの壁のフラグ。cells[y][x] でアクセスする。
            最初はすべての壁が閉じている。
        steps: 壁の変更の記録。古いものから順に並ぶ。
    """

    def __init__(self, width: int, height: int) -> None:
        """すべての壁が閉じた width x height のグリッドを作る。

        Args:
            width: 列数。
            height: 行数。
        """
        self.width = width
        self.height = height
        # Wall flags, cells[y][x]
        self.cells: list[list[int]] = [
            [ALL_WALLS] * width
            for _ in range(height)
        ]
        self.__blocked: set[Coordinate] = set()
        # 壁の変更の記録。壁は open_wall / close_wall でしか変えないので、
        # ここで記録すればどのアルゴリズムの生成過程も残る
        self.steps: list[WallChange] = []

    # 四隅・中央の求め方は関数 corner_cells / centre_cells にあり、
    # Grid を作らずに幅と高さだけでも使える。ここではそれを呼ぶだけ
    @property
    def corners(self) -> set[Coordinate]:
        """グリッドの四隅のセルを返す。

        Returns:
            四隅のセルの集合 (corner_cells() と同じ)。
        """
        return corner_cells(self.width, self.height)

    @property
    def centre(self) -> set[Coordinate]:
        """グリッドの中央のセルを返す。

        Returns:
            中央のセルの集合 (centre_cells() と同じ)。
        """
        return centre_cells(self.width, self.height)

    def in_bounds(self, pos: Coordinate) -> bool:
        """pos がグリッドの内側にあるかを返す。

        Args:
            pos: 調べる座標。

        Returns:
            内側なら True。
        """
        # つまり境界条件チェック
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def is_blocked(self, pos: Coordinate) -> bool:
        """pos が閉じたままにするセル (「42」のセル) かを返す。

        Args:
            pos: 調べるセル。

        Returns:
            block() で登録されていれば True。
        """
        # 「42」に含まれているかどうか判定
        return pos in self.__blocked

    def block(self, pos: Coordinate) -> None:
        """pos を閉じたままにするセルとして登録する。

        登録したセルの壁は open_wall() でも close_wall() でも変更できず、
        positions() や neighbors() にも現れない。「42」を描くのに使う。

        Args:
            pos: 登録するセル。

        Raises:
            ValueError: pos がグリッドの外にある場合。
        """
        # 「42」を作る際に使う、当該セルをブロックリストに追加
        if not self.in_bounds(pos):
            raise ValueError(f"{tuple(pos)} is outside of the grid")
        self.__blocked.add(pos)

    def positions(self) -> Iterator[Coordinate]:
        """閉じたままにするセル以外のすべてのセルを、左上から行ごとに返す。

        Yields:
            各セルの座標。
        """
        # 「すべてのセルに対して何かを行いたいが、『42』に含まれるものは除外する」に使う
        # 二重forループですべてのセルを見るが、ブロックされているものは除外
        for y in range(self.height):
            for x in range(self.width):
                pos = Coordinate(x, y)
                if not self.is_blocked(pos):
                    yield pos

    def neighbors(self, pos: Coordinate) -> Iterator[tuple[Wall, Coordinate]]:
        """pos とつなげられる隣接セルを、方向と組にして返す。

        グリッドの内側にあり、閉じたままにするセルでないものだけを返す。
        壁の有無は問わない。

        Args:
            pos: 基準のセル。

        Yields:
            (方向, 隣接セル) の組。方向は pos から見た壁。
        """
        # 東西南北すべてをチェックし、迷宮内にある＆ブロックされていないものをyieldで返す
        for direction in Wall:
            dx, dy = direction.delta
            other = Coordinate(pos.x + dx, pos.y + dy)
            if self.in_bounds(other) and not self.is_blocked(other):
                yield direction, other

    def open_neighbors(
        self, pos: Coordinate
    ) -> Iterator[tuple[Wall, Coordinate]]:
        """pos と壁を挟まずにつながっている隣接セルを、方向と組にして返す。

        Args:
            pos: 基準のセル。

        Yields:
            (方向, 隣接セル) の組。方向は pos から見た壁。
        """
        # 上のneighborで得られるもののうち、壁で遮られていないものを返す
        for direction, other in self.neighbors(pos):
            if not self.has_wall(pos, direction):
                yield direction, other

    def has_wall(self, pos: Coordinate, direction: Wall) -> bool:
        """pos の指定した方向の壁が閉じているかを返す。

        Args:
            pos: 調べるセル。
            direction: 調べる壁の方向。

        Returns:
            閉じていれば True。
        """
        return Wall.has_wall(self.cells[pos.y][pos.x], direction)

    def is_deadend(self, pos: Coordinate) -> bool:
        """pos が行き止まり (壁がちょうど3枚閉じている) かを返す。

        Args:
            pos: 調べるセル。

        Returns:
            行き止まりなら True。
        """
        wall_count: int = 0
        for direction in Wall:
            if self.has_wall(pos, direction):
                wall_count += 1
        return wall_count == 3

    def is_open_area(self, pos: Coordinate) -> bool:
        """pos を左上とする 3x3 の範囲が、内側に壁のない広場かを返す。
        INVALID_ROOMとのビットANDで判断。

        Args:
            pos: 3x3 の範囲の左上のセル。

        Returns:
            広場なら True。範囲がグリッドからはみ出す場合は False。
        """
        if pos.y > self.height - 3 or pos.x > self.width - 3:
            return False
        for dy in range(3):
            for dx in range(3):
                cell = self.cells[pos.y + dy][pos.x + dx]
                if INVALID_ROOM[dy][dx] & cell > 0:
                    return False
        return True

    def open_wall(self, pos: Coordinate, direction: Wall) -> None:
        """pos と隣接セルの間の壁を両側から開け、steps に記録する。

        Args:
            pos: 壁を開けるセル。
            direction: 開ける壁の方向。

        Raises:
            ValueError: pos か隣接セルがグリッドの外にあるか、
                閉じたままにするセルの場合。
        """
        dx, dy = direction.delta
        other = Coordinate(pos.x + dx, pos.y + dy)
        if not all(
            self.in_bounds(cell) and not self.is_blocked(cell)
            for cell in (pos, other)
        ):
            raise ValueError(
                f"cannot open the {direction.name} wall of {tuple(pos)}"
            )
        self.cells[pos.y][pos.x] = Wall.remove_wall(
            self.cells[pos.y][pos.x], direction
        )
        self.cells[other.y][other.x] = Wall.remove_wall(
            self.cells[other.y][other.x], direction.opposite
        )
        self.steps.append(WallChange(pos, direction, opened=True))

    def close_wall(self, pos: Coordinate, direction: Wall) -> None:
        """pos と隣接セルの間の壁を両側から閉じ、steps に記録する。

        Args:
            pos: 壁を閉じるセル。
            direction: 閉じる壁の方向。

        Raises:
            ValueError: pos か隣接セルがグリッドの外にあるか、
                閉じたままにするセルの場合。
        """
        dx, dy = direction.delta
        other = Coordinate(pos.x + dx, pos.y + dy)
        if not all(
            self.in_bounds(cell) and not self.is_blocked(cell)
            for cell in (pos, other)
        ):
            raise ValueError(
                f"cannot close the {direction.name} wall of {tuple(pos)}"
            )
        self.cells[pos.y][pos.x] = Wall.add_wall(
            self.cells[pos.y][pos.x], direction
        )
        self.cells[other.y][other.x] = Wall.add_wall(
            self.cells[other.y][other.x], direction.opposite
        )
        self.steps.append(WallChange(pos, direction, opened=False))

    def connectivity_parameters(self) -> tuple[int, int, int]:
        """通路をグラフとみなし、頂点数・辺数・連結成分数を返す。

        閉じたままにするセル以外のセルを頂点、壁のない箇所を辺とする。

        Returns:
            (頂点数, 辺数, 連結成分数) の組。
        """
        # 閉路の数 = 辺の数(つまり壁のない箇所の数) − セル数 + 連結成分数
        # 辺/Edge , 頂点/Vertex, 連結成分/Componentの数をそれぞれ計算する
        cells = list(self.positions())
        v = len(cells)
        # frozensetは順序を持たないので(A, B)と(B,A)を同一として見る
        # よって重複が自然に弾かれる
        edges: set[frozenset[Coordinate]] = {
            frozenset((pos, other))
            for pos in cells
            for _, other in self.open_neighbors(pos)
        }
        e = len(edges)
        seen: set[Coordinate] = set()
        c = 0
        for pos in cells:
            if pos in seen:
                continue
            c += 1
            queue = deque([pos])
            seen.add(pos)
            while queue:
                cur = queue.popleft()
                for _, other in self.open_neighbors(cur):
                    if other not in seen:
                        seen.add(other)
                        queue.append(other)
        return v, e, c

    def count_loops(self) -> int:
        """迷路の独立した閉路の数を返す。

        connectivity_parameters() の結果から cycle_rank() で求める。
        連結成分数も使うなら、connectivity_parameters() を一度だけ呼んで
        cycle_rank() に渡すほうが速い (validate.find_problems() など)。

        Returns:
            独立した閉路の数。完全迷路なら 0。
        """
        return cycle_rank(*self.connectivity_parameters())
