"""Growing Tree 法で迷路を掘る。

掘り進める元のセルは、10% の確率で最も新しく加えた活性セルを、
それ以外は活性セルの中からランダムに選ぶ。
"""
from random import Random

from ..grid import Grid
from ..maze import Coordinate


def carve(grid: Grid, rng: Random) -> None:
    """グリッドの壁を開けて完全迷路 (全域木) にする。

    活性セル (未訪問の隣接セルが残っているかもしれないセル) を1つ選び、
    未訪問の隣接セルへの壁を開けて、そのセルを活性セルに加える。
    未訪問の隣接セルがなければ、選んだセルを活性セルから外す。
    壁の変更は Grid.open_wall() を通して Grid.steps に記録される。

    Args:
        grid: 壁がすべて閉じたグリッド。その場で書き換える。
        rng: 活性セルと隣接セルの選択に使う乱数生成器。
    """
    start = next(grid.positions())
    visited: set[Coordinate] = {start}
    cells = [start]
    # Insertion order gives the newest cell; indices allow O(1) removal.
    active = {start: 0}
    while cells:
        pos = (next(reversed(active)) if rng.random() < 0.1
               else cells[rng.randrange(len(cells))])
        candidates = [
            (direction, adjacent)
            for direction, adjacent in grid.neighbors(pos)
            if adjacent not in visited
        ]
        if not candidates:
            index = active.pop(pos)
            last = cells.pop()
            if index < len(cells):
                cells[index] = last
                active[last] = index
            continue
        direction, adjacent = rng.choice(candidates)
        grid.open_wall(pos, direction)
        visited.add(adjacent)
        active[adjacent] = len(cells)
        cells.append(adjacent)
