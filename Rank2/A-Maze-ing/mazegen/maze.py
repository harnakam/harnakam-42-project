#!/usr/bin/env python3

"""生成した迷路を表すデータ型。"""

from dataclasses import dataclass, field
from typing import NamedTuple

from .wall import Wall


# NamedTupleとは
#   「名前付きのタプル」を class 文の形で宣言する仕組み。
#   フィールド名と型を並べるだけで、x と y を持つ値の組が作れる。
#
#   dataclass との使い分け: 座標のような小さな値の組は NamedTuple、
#   Maze のように複数の値をまとめてメソッドも持たせたいものは dataclass。

class Coordinate(NamedTuple):
    """セルの位置。

    Attributes:
        x: 列番号。左端が 0。
        y: 行番号。上端が 0。
    """

    x: int
    y: int


class WallChange(NamedTuple):
    """生成過程の1手。壁を1枚開けた、または閉じた記録。

    Attributes:
        pos: 壁を変更したセル。
        direction: pos のどの壁を変更したか。隣のセルの反対側の壁も
            同時に変わる。
        opened: True なら開けた、False なら閉じた。
    """

    pos: Coordinate
    direction: Wall  # the wall of pos; the neighbour's opposite wall too
    opened: bool  # True: the wall was opened, False: it was closed


@dataclass(frozen=True)
class Maze:
    """生成された迷路。

    Attributes:
        cells: 各セルの壁のフラグ (Wall の組み合わせ)。cells[y][x] で
            アクセスする。
        entry: 入口のセル。
        exit: 出口のセル。
        path: 入口から出口までの最短経路。各一歩の方向を N, E, S, W で
            表した文字列。
        steps: 生成過程。すべての壁が閉じた盤面に先頭から順に当てると
            cells になる。ファイルから読み込んだ迷路などでは空。
    """

    cells: list[list[int]]  # Wall flags, cells[y][x]
    entry: Coordinate
    exit: Coordinate
    path: str = ""  # letters N, E, S, W from the entry to the exit
    # 生成過程: すべての壁が閉じた盤面に先頭から順に当てると cells になる
    # (ファイルから読み込んだ迷路などでは空)
    # 迷路そのものではなく作り方の記録なので、== の比較と repr には含めない
    steps: tuple[WallChange, ...] = field(
        default=(), compare=False, repr=False
    )

    @property
    def width(self) -> int:
        """迷路の列数 (横のセル数) を返す。

        Returns:
            列数。cells が空なら 0。
        """
        return len(self.cells[0]) if self.cells else 0

    @property
    def height(self) -> int:
        """迷路の行数 (縦のセル数) を返す。

        Returns:
            行数。
        """
        return len(self.cells)
