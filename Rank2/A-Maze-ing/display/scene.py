#!/usr/bin/env python3

"""何を描くかを、描き方 (バックエンド) と切り離して表す。"""

# ViewState (操作の結果) を、描画に必要な値だけの Scene に変換する。
# 色もここで名前から RGB に変えるので、バックエンドは色の名前を知らない。
# 各バックエンドの render() は Scene だけを受け取るので、
# show_path のような「処理を切り替えるフラグ」を知らなくて済む
# (経路を出さないときは path_cells が空になるだけ)。

from dataclasses import dataclass

from mazegen import Coordinate, Maze, Wall

from .controller import ViewState
from .palette import RGB, WALL_COLORS, path_color_for

# 経路の文字 "N"/"E"/"S"/"W" から Wall を引く逆引き表
# e.g. : {"N": Wall.NORTH, "E": Wall.EAST, ...}
_LETTER_TO_WALL: dict[str, Wall] = {wall.letter: wall for wall in Wall}


@dataclass(frozen=True)
class Scene:
    """バックエンドが1フレームを描くのに必要なものすべて。

    Attributes:
        maze: 描く迷路。
        path_cells: 最短経路上のセル。経路を表示しないときは空。
        wall_color: 壁の色の RGB。None ならバックエンドの標準の色。
        path_color: 経路の色の RGB。
    """

    maze: Maze
    path_cells: frozenset[Coordinate]  # empty when the path is hidden
    wall_color: RGB | None  # None: the backend's default colour
    path_color: RGB


def path_cells(maze: Maze) -> frozenset[Coordinate]:
    """maze.path をたどり、経路上のすべてのセルを返す。

    Args:
        maze: 経路をたどる迷路。

    Returns:
        経路上のセルの集合。入口と出口も含む。
    """
    pos = maze.entry
    cells = {pos}
    for letter in maze.path:
        dx, dy = _LETTER_TO_WALL[letter].delta
        pos = Coordinate(pos.x + dx, pos.y + dy)
        cells.add(pos)
    return frozenset(cells)


def build_scene(state: ViewState) -> Scene:
    """現在の表示の状態から、描く内容 (Scene) を作る。

    Args:
        state: 現在の表示の状態。

    Returns:
        色の名前を RGB に変換した Scene。
    """
    return Scene(
        maze=state.maze,
        path_cells=path_cells(state.maze) if state.show_path else frozenset(),
        wall_color=WALL_COLORS[state.wall_color],
        path_color=path_color_for(state.wall_color),
    )
