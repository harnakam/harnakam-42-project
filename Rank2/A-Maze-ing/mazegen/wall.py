#!/usr/bin/env python3

"""セルの壁を表すビットフラグ。"""

# typingをimportせずに型ヒントを書く
# typingのimportはこれを使う側に任せる
from __future__ import annotations

from enum import IntFlag


class Wall(IntFlag):
    """セルの4方向の壁を表すフラグ。ビットが立っていれば壁が閉じている。

    セルの値はこれらの論理和で、0 (すべて開いている) から ALL_WALLS
    (すべて閉じている) までの整数になる。

    Attributes:
        NORTH: 北 (上) の壁。ビット0。
        EAST: 東 (右) の壁。ビット1。
        SOUTH: 南 (下) の壁。ビット2。
        WEST: 西 (左) の壁。ビット3。
    """

    NORTH = 0b0001  # bit 0
    EAST = 0b0010  # bit 1
    SOUTH = 0b0100  # bit 2
    WEST = 0b1000  # bit 3

    @staticmethod
    def add_wall(cell: int, wall: Wall) -> int:
        """cell の指定した壁を閉じた値を返す。

        Args:
            cell: セルの壁のフラグ。
            wall: 閉じる壁。

        Returns:
            wall のビットを立てた cell の値。
        """
        return cell | wall

    @staticmethod
    def remove_wall(cell: int, wall: Wall) -> int:
        """cell の指定した壁を開けた値を返す。

        Args:
            cell: セルの壁のフラグ。
            wall: 開ける壁。

        Returns:
            wall のビットを下ろした cell の値。
        """
        return cell & ~wall

    @staticmethod
    def has_wall(cell: int, wall: Wall) -> bool:
        """cell の指定した壁が閉じているかを返す。

        Args:
            cell: セルの壁のフラグ。
            wall: 調べる壁。

        Returns:
            閉じていれば True、開いていれば False。
        """
        return bool(cell & wall)

    @property
    def opposite(self) -> Wall:
        """同じ辺を隣のセルから見たときの壁を返す。

        Returns:
            反対方向の壁 (例: NORTH なら SOUTH)。
        """
        return _OPPOSITE[self]

    @property
    def letter(self) -> str:
        """経路の文字列でこの方向を表す文字を返す。

        Returns:
            "N", "E", "S", "W" のいずれか。
        """
        return _LETTER[self]

    @property
    def delta(self) -> tuple[int, int]:
        """この壁の向こうのセルへ進むときの座標の変化量を返す。

        Returns:
            (dx, dy)。dx は列、dy は行の変化量 (例: NORTH なら (0, -1))。
        """
        return _DELTA[self]


ALL_WALLS = 0b1111

_OPPOSITE: dict[Wall, Wall] = {
    Wall.NORTH: Wall.SOUTH,
    Wall.EAST: Wall.WEST,
    Wall.SOUTH: Wall.NORTH,
    Wall.WEST: Wall.EAST,
}

_LETTER: dict[Wall, str] = {
    Wall.NORTH: "N",
    Wall.EAST: "E",
    Wall.SOUTH: "S",
    Wall.WEST: "W",
}

_DELTA: dict[Wall, tuple[int, int]] = {
    Wall.NORTH: (0, -1),
    Wall.EAST: (1, 0),
    Wall.SOUTH: (0, 1),
    Wall.WEST: (-1, 0),
}
