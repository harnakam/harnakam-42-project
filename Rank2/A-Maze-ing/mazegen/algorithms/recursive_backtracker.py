"""再帰的バックトラック法 (スタックを使う深さ優先探索) で迷路を掘る。"""

from collections import deque
from random import Random

from ..grid import Grid
from ..maze import Coordinate


def carve(grid: Grid, rng: Random) -> None:
    """グリッドの壁を開けて完全迷路にする。

    左上から見て最初のセルを起点に深さ優先探索を行い、未訪問の隣接セルを
    ランダムに選んでその間の壁を開ける。行き詰まったら1つ前のセルに戻る。

    Args:
        grid: 壁がすべて閉じたグリッド。その場で書き換える。
        rng: 隣接セルの選択に使う乱数生成器。
    """
    start = next(grid.positions())
    visited: set[Coordinate] = {start}
    stack: deque[Coordinate] = deque([start])

    while stack:
        pos = stack.pop()
        candidates = [
            (direction, adjacent)
            for direction, adjacent in grid.neighbors(pos)
            if adjacent not in visited
        ]
        if not candidates:
            continue
        direction, adjacent = rng.choice(candidates)
        grid.open_wall(pos, direction)
        visited.add(adjacent)
        stack.append(pos)
        stack.append(adjacent)
