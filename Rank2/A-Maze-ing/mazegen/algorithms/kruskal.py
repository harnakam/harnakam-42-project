#!/usr/bin/env python3

"""クラスカル法で迷路を掘る。"""

from random import Random

from ..grid import Grid
from ..maze import Coordinate
from ..wall import Wall


def _find(parent: dict[Coordinate, Coordinate], pos: Coordinate) -> Coordinate:
    """Union-Find の木をたどり、pos が属する集合の代表 (根) を返す。

    たどる途中で各セルの親を祖父に付け替え、以降の探索を速くする。

    Args:
        parent: 各セルの親を表す辞書。その場で書き換える。
        pos: 代表を調べるセル。

    Returns:
        pos が属する集合の代表のセル。
    """
    while parent[pos] != pos:
        # 探索と同時に木を浅くしていくことで効率化する
        parent[pos] = parent[parent[pos]]
        pos = parent[pos]
    return pos


def carve(grid: Grid, rng: Random) -> None:
    """グリッドの壁を開けて完全迷路にする。

    隣り合うセルの間の壁をすべてランダムな順に並べ、壁の両側のセルが
    まだつながっていなければその壁を開ける (Union-Find で判定する)。

    Args:
        grid: 壁がすべて閉じたグリッド。その場で書き換える。
        rng: 壁の順番をシャッフルする乱数生成器。
    """
    parent: dict[Coordinate, Coordinate] = {
        pos: pos for pos in grid.positions()
    }
    walls_to_break: list[tuple[Coordinate, Wall, Coordinate]] = [
        (pos, direction, adjacent)
        for pos in grid.positions()
        for direction, adjacent in grid.neighbors(pos)
        if direction in (Wall.EAST, Wall.SOUTH)
    ]
    rng.shuffle(walls_to_break)
    for pos, direction, adjacent in walls_to_break:
        root_p, root_a = _find(parent, pos), _find(parent, adjacent)
        if root_p != root_a:
            parent[root_a] = root_p
            grid.open_wall(pos, direction)
