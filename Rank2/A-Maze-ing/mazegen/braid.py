#!/usr/bin/env python3

"""完全迷路に閉路を足し、完全でない迷路 (PERFECT=False) にする。"""

import logging
from collections import deque
from random import Random

from .grid import MIN_LOOPS, Grid
from .maze import Coordinate
from .wall import Wall

logger = logging.getLogger(__name__)


def break_deadend(grid: Grid, pos: Coordinate, rng: Random) -> bool:
    """pos が行き止まりなら、壁をもう1枚開けて行き止まりでなくす。

    開ける壁は、迷路の内側にあり「42」に面していない閉じた壁から
    ランダムに選ぶ。

    Args:
        grid: 対象のグリッド。その場で書き換える。
        pos: 調べるセル。
        rng: 開ける壁の選択に使う乱数生成器。

    Returns:
        壁を開けたら True。pos が行き止まりでないか、開けられる壁が
        なければ False。
    """
    if not grid.is_deadend(pos):
        return False
    candidates = [
        direction for direction, _ in grid.neighbors(pos)
        if grid.has_wall(pos, direction)
    ]
    if not candidates:
        return False
    rng.shuffle(candidates)
    grid.open_wall(pos, candidates[0])
    return True


def close_open_areas(grid: Grid, rng: Random) -> None:
    """3x3 の広場をすべて探し、それぞれの中央のセルの壁を1枚閉じる。

    Args:
        grid: 対象のグリッド。その場で書き換える。
        rng: 閉じる壁の選択に使う乱数生成器。
    """
    for pos in grid.positions():
        if grid.is_open_area(pos):
            directions = list(Wall)
            rng.shuffle(directions)
            grid.close_wall(
                Coordinate(pos.x + 1, pos.y + 1), directions[0]
            )


def add_loops(grid: Grid, rng: Random) -> None:
    """閉路が MIN_LOOPS 個に満たなければ、閉じた壁をランダムに開けて足す。

    すでに足りていれば何もしない (乱数も使わない)。

    Args:
        grid: 対象のグリッド。その場で書き換える。
        rng: 開ける壁の選択に使う乱数生成器。
    """
    # 迷路は連結しているので、閉じた壁を1枚開けるごとに閉路はちょうど1つ増える。
    # 足りないときだけ乱数を使うので、足りている迷路の seed の結果は変わらない
    loops = grid.count_loops()
    shortage = MIN_LOOPS - loops
    logger.debug(
        "loops after breaking dead ends: %d (opening %d more)",
        loops, max(0, shortage),
    )
    if shortage <= 0:
        return
    # 各壁を1回だけ数えるため、東と南の壁だけを候補にする
    candidates = [
        (pos, direction)
        for pos in grid.positions()
        for direction, _ in grid.neighbors(pos)
        if direction in (Wall.EAST, Wall.SOUTH)
        and grid.has_wall(pos, direction)
    ]
    rng.shuffle(candidates)
    for pos, direction in candidates[:shortage]:
        grid.open_wall(pos, direction)


def make_imperfect(grid: Grid, entry: Coordinate, rng: Random) -> None:
    """完全迷路を、閉路を持つ完全でない迷路に作り変える。

    入口から到達できる行き止まりを壊し、閉路が MIN_LOOPS 個に満たなければ
    足し、最後にできた 3x3 の広場を閉じる。結果が要件を満たすかどうかは
    ここでは確かめず、validate.find_problems() で調べる。

    Args:
        grid: 完全迷路を掘ったグリッド。その場で書き換える。
        entry: 入口のセル。ここから幅優先探索で行き止まりを探す。
        rng: 壁の選択に使う乱数生成器。
    """
    no_need_to_visit: set[Coordinate] = {entry}
    queue: deque[Coordinate] = deque([entry])
    while queue:
        pos = queue.popleft()
        break_deadend(grid, pos, rng)
        for _, adjacent_cell in grid.open_neighbors(pos):
            if adjacent_cell not in no_need_to_visit:
                no_need_to_visit.add(adjacent_cell)
                queue.append(adjacent_cell)
    # 行き止まりを壊すだけでは閉路が1つしかできないことがある
    # (例: 一筆書きの迷路の両端がつながるだけのとき)。
    # close_open_areas() より前に足しておけば十分: 3x3 の広場は内側に閉路を
    # 4つ持ち、中央の壁を1枚閉じても3つ残るので、閉じたあとも MIN_LOOPS を下回らない
    add_loops(grid, rng)
    close_open_areas(grid, rng)
