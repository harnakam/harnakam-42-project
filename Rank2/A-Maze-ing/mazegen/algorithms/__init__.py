#!/usr/bin/env python3

"""迷路を掘るアルゴリズムの一覧。

どのアルゴリズムも CarveFunction の形 (Grid と乱数生成器を受け取り、
Grid の壁を開けて完全迷路にする関数) をしており、ALGORITHMS に名前で登録する。
"""

from collections.abc import Callable
from random import Random

from ..grid import Grid
from . import growing_tree, kruskal, recursive_backtracker

CarveFunction = Callable[[Grid, Random], None]

ALGORITHMS: dict[str, CarveFunction] = {
    "backtracker": recursive_backtracker.carve,
    "kruskal": kruskal.carve,
    "growing_tree": growing_tree.carve,
}

DEFAULT_ALGORITHM = "backtracker"

# the names users can pass as algorithm=; a tuple so that it cannot be changed
AVAILABLE_ALGORITHMS: tuple[str, ...] = tuple(sorted(ALGORITHMS))


__all__ = [
    "ALGORITHMS", "AVAILABLE_ALGORITHMS", "CarveFunction", "DEFAULT_ALGORITHM"
]
