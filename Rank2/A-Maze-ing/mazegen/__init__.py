#!/usr/bin/env python3

"""迷路を生成するパッケージ。

MazeGenerator に大きさ・入口・出口などを渡して generate_maze() を呼ぶと、
壁・入口・出口・最短経路をまとめた Maze が返る。

公開している名前:
    MazeGenerator: 迷路の生成の入口となるクラス。
    Maze: 生成された迷路。
    Coordinate: セルの座標 (x, y)。
    Wall: セルの壁を表すビットフラグ。
    WallChange: 生成過程の1手 (壁を1枚開けた・閉じた記録)。
    AVAILABLE_ALGORITHMS: 指定できるアルゴリズム名の一覧。
    DEFAULT_ALGORITHM: 既定のアルゴリズム名。
"""


import logging

from .algorithms import AVAILABLE_ALGORITHMS, DEFAULT_ALGORITHM
from .maze import Coordinate, Maze, WallChange
from .maze_generator import MazeGenerator
from .wall import Wall

# ライブラリの慣習: ログを出すかどうかは利用者(アプリ)の logging の設定に任せる。
# 設定がないときに mazegen のログが勝手に stderr に出ないようにする
logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = [
    "AVAILABLE_ALGORITHMS", "Coordinate", "DEFAULT_ALGORITHM",
    "Maze", "MazeGenerator", "Wall", "WallChange"
]
