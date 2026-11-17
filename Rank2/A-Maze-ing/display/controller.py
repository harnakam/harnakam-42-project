#!/usr/bin/env python3

"""利用者の操作を Command オブジェクトとして表す (全バックエンドで共通)。"""

# Command パターン:
#   Receiver  ViewState      操作によって書き換わる表示の状態
#   Command   Regenerate など 1つの操作を1つのオブジェクトにしたもの
#   Invoker   各バックエンド  キーを読み、Controller.dispatch() に渡す
# 端末のループ (display_ascii) と MLX のキーフック (display_mlx) という
# 2つの Invoker が、同じ操作を同じ形で呼べるようにするために使う。
# バックエンドは具体的な Command を知らず、キーの文字を渡すだけでよい。

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from mazegen import Maze

from .palette import INITIAL_WALL_COLOR, next_color


@dataclass
class ViewState:
    """いま表示している内容。Command によって書き換わる。

    Attributes:
        maze: 表示している迷路。
        show_path: 最短経路を表示しているかどうか。
        wall_color: 壁の色の名前 (palette.WALL_COLORS のキー)。
        running: 表示を続けているかどうか。終了すると False になる。
    """

    maze: Maze
    show_path: bool = False
    wall_color: str = INITIAL_WALL_COLOR  # a name in palette.WALL_COLORS
    running: bool = True


class Command(Protocol):
    """利用者の1つの操作。

    Attributes:
        label: キー操作の説明に表示する短い名前。
    """

    label: str

    def execute(self, state: ViewState) -> None:
        """操作を実行し、state を書き換える。

        Args:
            state: 書き換える表示の状態。
        """


class Regenerate:
    """迷路を新しく生成したものに置き換える操作。"""

    label = "regenerate"

    def __init__(self, regenerate: Callable[[], Maze]) -> None:
        """迷路を生成する関数を受け取る。

        Args:
            regenerate: 引数なしで呼ぶと新しい迷路を返す関数。
        """
        # 迷路の作り方は知らず、呼び出し元 (a_maze_ing.py) から受け取った
        # コールバックを呼ぶだけ
        self._regenerate = regenerate

    def execute(self, state: ViewState) -> None:
        """新しい迷路を生成し、state.maze を置き換える。

        Args:
            state: 書き換える表示の状態。
        """
        state.maze = self._regenerate()


class TogglePath:
    """最短経路の表示・非表示を切り替える操作。"""

    label = "toggle path"

    def execute(self, state: ViewState) -> None:
        """state.show_path を反転する。

        Args:
            state: 書き換える表示の状態。
        """
        state.show_path = not state.show_path


class CycleWallColor:
    """壁の色を次の色に切り替える操作。"""

    label = "wall colour"

    def execute(self, state: ViewState) -> None:
        """state.wall_color を次の色にする。

        Args:
            state: 書き換える表示の状態。
        """
        state.wall_color = next_color(state.wall_color)


class Quit:
    """表示を終了する操作。"""

    label = "quit"

    def execute(self, state: ViewState) -> None:
        """state.running を False にする。バックエンドはそれを見て終了する。

        Args:
            state: 書き換える表示の状態。
        """
        state.running = False


class Controller:
    """キーと Command を対応づけ、押されたキーの Command を実行する。

    Attributes:
        state: Command が書き換える表示の状態。
    """

    def __init__(self, state: ViewState, bindings: dict[str, Command]) -> None:
        """表示の状態とキーの割り当てを受け取る。

        Args:
            state: Command が書き換える表示の状態。
            bindings: キーから Command への辞書。この順に help_text() に並ぶ。
        """
        self.state = state
        self._bindings = bindings

    def dispatch(self, key: str) -> bool:
        """key に割り当てた Command を実行する。

        Args:
            key: 押されたキーの文字。

        Returns:
            Command を実行したら True。key に何も割り当てていなければ False。
        """
        command = self._bindings.get(key)
        if command is None:
            return False
        command.execute(self.state)
        return True

    def help_text(self) -> str:
        """キー操作の説明を返す。

        Returns:
            "[r] regenerate  [q] quit" のように、割り当てごとの
            "[キー] 名前" を空白2つで区切った文字列。
        """
        # 表示する説明を bindings から作るので、キーを足したときに
        # 説明の文字列を別に書き換える必要がない
        return "  ".join(
            f"[{key}] {command.label}"
            for key, command in self._bindings.items()
        )


def make_controller(
    maze: Maze, regenerate: Callable[[], Maze]
) -> Controller:
    """既定のキー割り当ての Controller を作る。

    キーは r (再生成)、p (経路の表示切り替え)、c (壁の色)、q (終了)。

    Args:
        maze: 最初に表示する迷路。
        regenerate: r が押されたときに引数なしで呼ぶ関数。新しい迷路を返す。

    Returns:
        maze を表示する状態を持つ Controller。
    """
    # 定義順がそのまま help_text() に並ぶ順になる
    bindings: dict[str, Command] = {
        "r": Regenerate(regenerate),
        "p": TogglePath(),
        "c": CycleWallColor(),
        "q": Quit(),
    }
    return Controller(ViewState(maze), bindings)
