#!/usr/bin/env python3

"""迷路を MiniLibX の窓に表示する。"""

from collections.abc import Iterator
from enum import Enum
from math import ceil
from textwrap import wrap
from time import monotonic

from mazegen import Coordinate, Wall
from mazegen.wall import ALL_WALLS

from .controller import Controller
from .palette import (
    BACKGROUND_COLOR, DEFAULT_WALL_COLOR, ENTRY_COLOR, EXIT_COLOR,
    FORTYTWO_COLOR,
)
from .scene import build_scene
from .display_ascii import cell_display, HORIZONTAL, VERTICAL
from .Minilib import Minilib


CELL_SIZE = 50        # 1マスの幅と高さ
COLOR = DEFAULT_WALL_COLOR  # 壁の標準色：柔らかいアイボリー
S_COLOR = ENTRY_COLOR  # スタート：濃い緑
G_COLOR = EXIT_COLOR  # ゴール：濃い赤
HELP_HEIGHT = 40     # 操作説明用の余白
TEXT_WIDTH = 10      # 操作説明の1文字あたりの余裕


class AnimationKind(Enum):
    """起動時と再生成時に再生するアニメーションの種類。

    Attributes:
        NONE: アニメーションなし。完成した迷路を一度に描く。
        CELLS: 完成した迷路を1マスずつ描く。
        GENERATION: 生成時の壁の開閉を順に再生する。
        PATH: 完成した迷路を描き、経路を表示しているなら入口から順に塗る。
    """

    NONE = "none"
    CELLS = "cells"
    GENERATION = "generation"
    PATH = "path"


ANIMATION_KIND = AnimationKind.GENERATION
ANIMATION_SPEED = 1  # 0: 即時表示、1以上: 更新間隔の倍率
ANIMATION_STEPS_PER_FRAME = 100
FRAME_INTERVAL = 1 / 60
ANIMATION_DURATION = 2.0  # 大きな迷路でも標準倍率で約2秒以内に再生


class DisplayUnavailableError(RuntimeError):
    """MLX の初期化に失敗し、表示を開始できないことを表す。"""


def run(controller: Controller) -> None:
    """MiniLibX の窓に迷路を描き、終了するまでキー入力を処理する。

    窓を閉じるか q (または Esc) を押すと終わる。ANIMATION_KIND に従い、
    起動時と再生成時にアニメーションを再生する。

    Args:
        controller: 表示する状態を持ち、キーに対応する操作を実行する。

    Raises:
        RuntimeError: X11 の表示先に接続できないなど、窓を開けない場合。
    """
    maze = controller.state.maze

    # +1 は右端と下端の壁を描くための余白
    width = max(
        len(maze.cells[0]) * CELL_SIZE + 1,
        len(controller.help_text()) * TEXT_WIDTH + 20,
    )
    maze_height = len(maze.cells) * CELL_SIZE + 1
    height = maze_height + HELP_HEIGHT

    try:
        minilib = Minilib(width, height, "A-Maze-ing")
    except Exception as error:
        # auto の切り替え対象は初期化失敗だけ。実行中の例外とは区別する。
        raise DisplayUnavailableError(str(error)) from error
    help_lines = wrap(
        controller.help_text(),
        width=max(1, (minilib.width - 20) // TEXT_WIDTH),
    )
    help_height = max(HELP_HEIGHT, len(help_lines) * 20 + 20)
    cell_size = max(1, min(
        CELL_SIZE,
        (minilib.width - 1) // len(maze.cells[0]),
        (minilib.height - help_height - 1) // len(maze.cells),
    ))
    maze_height = len(maze.cells) * cell_size + 1
    playback_kind = ANIMATION_KIND

    def draw_marker(pos: Coordinate, goal: bool = False) -> None:
        """入口 (三角) または出口 (二重枠) の記号をセルに描く。

        Args:
            pos: 記号を描くセル。
            goal: True なら出口、False なら入口の記号を描く。
        """
        x, y = pos.x * cell_size + 1, pos.y * cell_size + 1
        size = cell_size - 1
        color = G_COLOR if goal else S_COLOR
        minilib.fill_rect(x, y, size, size, color)
        if size < 5:
            return
        inset = max(1, size // 5)
        inner = size - 2 * inset
        if goal:
            minilib.fill_rect(x + inset, y + inset, inner, inner,
                              BACKGROUND_COLOR)
            ring = max(1, inner // 4)
            minilib.fill_rect(x + inset + ring, y + inset + ring,
                              inner - 2 * ring, inner - 2 * ring, color)
        else:
            mid = y + size // 2
            radius = max(1, inner // 2)
            for offset in range(-radius, radius + 1):
                width = max(1, inner - abs(offset) * inner // (radius + 1))
                minilib.line(x + inset, mid + offset,
                             x + inset + width - 1, mid + offset,
                             BACKGROUND_COLOR)

    def draw_cells(slow: bool = False,
                   hide_path: bool = False) -> Iterator[None]:
        """現在の状態に合わせて、壁とセルの塗りつぶしを描き直す。

        Args:
            slow: True なら1マス描くごとに yield し、アニメーションにする。
            hide_path: True なら経路を塗らない。

        Yields:
            slow が True のとき、1マス描くごとに None。
        """
        scene = build_scene(controller.state)
        maze = scene.maze

        # 選ばれた RGB を、MLX に渡す色の整数に変換する
        if scene.wall_color is None:
            wall_color = COLOR
        else:
            red, green, blue = scene.wall_color
            wall_color = (
                0xFF000000 | (red << 16) | (green << 8) | blue
            )

        # 前の描画を消す
        minilib.clear()

        for y, row in enumerate(maze.cells):
            for x, cell in enumerate(row):
                glyphs = cell_display(cell)

                # マスの左・上・右・下の座標
                x0 = x * cell_size
                y0 = y * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                # 上の壁
                if glyphs.north == HORIZONTAL:
                    minilib.line(x0, y0, x1, y0, wall_color)

                # 左の壁
                if glyphs.west == VERTICAL:
                    minilib.line(x0, y0, x0, y1, wall_color)

                # 右端の外壁
                if x == len(row) - 1 and glyphs.east == VERTICAL:
                    minilib.line(x1, y0, x1, y1, wall_color)

                # 下端の外壁
                if y == len(maze.cells) - 1 and glyphs.south == HORIZONTAL:
                    minilib.line(x0, y1, x1, y1, wall_color)

                # 壁の1ピクセルを残してセル内を塗る。
                # スタート・ゴールは経路より優先する。
                pos = Coordinate(x, y)
                fill_color = FORTYTWO_COLOR if cell == ALL_WALLS else None
                if pos == maze.entry:
                    fill_color = S_COLOR
                elif pos == maze.exit:
                    fill_color = G_COLOR
                elif not hide_path and pos in scene.path_cells:
                    red, green, blue = scene.path_color
                    fill_color = (
                        0xFF000000 | (red << 16) | (green << 8) | blue
                    )
                if fill_color is not None:
                    minilib.fill_rect(
                        x0 + 1, y0 + 1,
                        cell_size - 1, cell_size - 1, fill_color,
                    )

                if pos == maze.entry or pos == maze.exit:
                    draw_marker(pos, goal=pos == maze.exit)

                if slow:
                    yield  # 1マス描いたら MLX に戻る

        for line_index, help_line in enumerate(help_lines):
            minilib.text(10, maze_height + 20 + line_index * 20,
                         help_line, COLOR)

    def generation_steps() -> Iterator[None]:
        """すべての壁が閉じた盤面から、生成時の壁の開閉を順に再生する。

        生成過程 (maze.steps) がなければ、完成した迷路をそのまま描く。
        再生が終わったら、経路の表示状態に合わせて描き仕上げる。

        Yields:
            壁を1枚変えるごとに None。
        """
        scene = build_scene(controller.state)
        maze = scene.maze
        if not maze.steps:
            yield from draw_cells()
            return
        wall_color = (COLOR if scene.wall_color is None else
                      0xFF000000 | (scene.wall_color[0] << 16)
                      | (scene.wall_color[1] << 8) | scene.wall_color[2])
        minilib.clear()
        for x in range(maze.width + 1):
            minilib.line(x * cell_size, 0, x * cell_size,
                         maze.height * cell_size, wall_color)
        for y in range(maze.height + 1):
            minilib.line(0, y * cell_size, maze.width * cell_size,
                         y * cell_size, wall_color)
        for line_index, help_line in enumerate(help_lines):
            minilib.text(10, maze_height + 20 + line_index * 20,
                         help_line, COLOR)
        for y, row in enumerate(maze.cells):
            for x, cell in enumerate(row):
                if cell == ALL_WALLS:
                    minilib.fill_rect(x * cell_size + 1, y * cell_size + 1,
                                      cell_size - 1, cell_size - 1,
                                      FORTYTWO_COLOR)
        draw_marker(maze.entry)
        draw_marker(maze.exit, goal=True)
        cells = [[ALL_WALLS] * maze.width for _ in range(maze.height)]

        def draw_corner(cx: int, cy: int) -> None:
            """格子点 (cx, cy) の1ピクセルを、接する壁に合わせて塗る。

            接する壁が1枚でも閉じていれば壁の色、すべて開いていれば
            背景色にする。

            Args:
                cx: 格子点の列 (0 から maze.width まで)。
                cy: 格子点の行 (0 から maze.height まで)。
            """
            walls = []
            for x in (cx - 1, cx):
                if 0 <= x < maze.width:
                    row = min(cy, maze.height - 1)
                    side = Wall.NORTH if cy < maze.height else Wall.SOUTH
                    walls.append(cells[row][x] & side)
            for y in (cy - 1, cy):
                if 0 <= y < maze.height:
                    col = min(cx, maze.width - 1)
                    side = Wall.WEST if cx < maze.width else Wall.EAST
                    walls.append(cells[y][col] & side)
            minilib.pixel(cx * cell_size, cy * cell_size,
                          wall_color if any(walls) else BACKGROUND_COLOR)

        yield
        for step in maze.steps:
            x0 = step.pos.x * cell_size
            y0 = step.pos.y * cell_size
            dx, dy = step.direction.delta
            other = Coordinate(step.pos.x + dx, step.pos.y + dy)
            update = Wall.remove_wall if step.opened else Wall.add_wall
            cells[step.pos.y][step.pos.x] = update(
                cells[step.pos.y][step.pos.x], step.direction,
            )
            cells[other.y][other.x] = update(
                cells[other.y][other.x], step.direction.opposite,
            )
            color = BACKGROUND_COLOR if step.opened else wall_color
            if step.direction in (Wall.NORTH, Wall.SOUTH):
                y = y0 + (cell_size if step.direction == Wall.SOUTH else 0)
                if cell_size > 1:
                    minilib.line(x0 + 1, y, x0 + cell_size - 1, y, color)
                draw_corner(step.pos.x, y // cell_size)
                draw_corner(step.pos.x + 1, y // cell_size)
            else:
                x = x0 + (cell_size if step.direction == Wall.EAST else 0)
                if cell_size > 1:
                    minilib.line(x, y0 + 1, x, y0 + cell_size - 1, color)
                draw_corner(x // cell_size, step.pos.y)
                draw_corner(x // cell_size, step.pos.y + 1)
            yield
        if controller.state.show_path:
            yield from path_steps()
        else:
            yield from draw_cells()

    def path_steps() -> Iterator[None]:
        """経路を入口から順に塗る。入口・出口の記号は最後まで残す。

        Yields:
            経路を1マス進むごとに None。
        """
        nonlocal playback_kind
        playback_kind = AnimationKind.PATH
        yield from draw_cells(hide_path=True)
        yield
        scene = build_scene(controller.state)
        maze = scene.maze
        red, green, blue = scene.path_color
        color = 0xFF000000 | (red << 16) | (green << 8) | blue
        directions = {wall.letter: wall.delta for wall in Wall}
        pos = maze.entry
        for letter in maze.path:
            dx, dy = directions[letter]
            pos = Coordinate(pos.x + dx, pos.y + dy)
            if pos != maze.entry and pos != maze.exit:
                minilib.fill_rect(pos.x * cell_size + 1,
                                  pos.y * cell_size + 1,
                                  cell_size - 1, cell_size - 1, color)
            yield

    def make_steps() -> Iterator[None]:
        """ANIMATION_KIND に合わせて、アニメーションのイテレーターを作る。

        Returns:
            next() を呼ぶたびに少しずつ描き進めるイテレーター。
        """
        nonlocal playback_kind
        playback_kind = ANIMATION_KIND
        if ANIMATION_KIND == AnimationKind.PATH:
            return (path_steps() if controller.state.show_path
                    else draw_cells())
        if ANIMATION_KIND == AnimationKind.GENERATION:
            return generation_steps()
        return draw_cells(slow=True)

    def steps_per_frame() -> int:
        """1フレームで描き進める回数を返す。

        アニメーションが約 ANIMATION_DURATION 秒で終わるよう、描き進める
        回数の合計から決める。ANIMATION_STEPS_PER_FRAME より小さくはしない。

        Returns:
            1フレームで next() を呼ぶ回数。
        """
        current = controller.state.maze
        if playback_kind == AnimationKind.PATH:
            total = len(current.path)
        elif playback_kind == AnimationKind.GENERATION:
            total = len(current.steps)
        else:
            total = current.width * current.height
        frames = max(1, int(ANIMATION_DURATION / (FRAME_INTERVAL or 1 / 60)))
        return max(1, ANIMATION_STEPS_PER_FRAME, ceil((total + 2) / frames))

    steps = make_steps()
    next_frame = 0.0
    animating = (ANIMATION_SPEED > 0
                 and ANIMATION_KIND != AnimationKind.NONE)

    def draw() -> None:
        """待たずに最後まで描き、窓に転送する (通常の再描画)。"""
        for _ in draw_cells():
            pass
        minilib.present()

    def animate() -> None:
        """時間が来ていれば、アニメーションを1フレーム進めて窓に転送する。

        ループフックから呼ばれる。最後まで再生したらループフックを外す。
        """
        nonlocal next_frame, animating
        now = monotonic()
        if now < next_frame:
            return
        next_frame = now + FRAME_INTERVAL * max(1, ANIMATION_SPEED)
        try:
            for _ in range(steps_per_frame()):
                next(steps)
        except StopIteration:
            animating = False
            minilib.on_loop(None)
        minilib.present()

    def on_key(key: str) -> None:
        """キーを controller に渡し、結果に合わせて描き直す。

        アニメーション中は q 以外のキーを無視する。r は再生成の
        アニメーションを、経路を表示したときの p は経路のアニメーションを
        始める。

        Args:
            key: 押されたキーの文字。
        """
        nonlocal steps, next_frame, animating
        if animating and key != "q":
            return
        if key == "r":
            # 生成処理を始める前に、前の迷路を全消去して表示する。
            minilib.clear()
            minilib.present()
        if not controller.dispatch(key):
            return
        if not controller.state.running:
            minilib.close()
        elif key == "r":
            steps = make_steps()
            next_frame = 0.0
            animating = (ANIMATION_SPEED > 0
                         and ANIMATION_KIND != AnimationKind.NONE)
            if animating:
                minilib.on_loop(animate)
            else:
                draw()
        elif key == "p" and controller.state.show_path and ANIMATION_SPEED > 0:
            steps = path_steps()
            next_frame = 0.0
            animating = True
            minilib.on_loop(animate)
        else:
            # 非表示・色切替は完成状態を即時表示する。
            animating = False
            if ANIMATION_SPEED > 0:
                minilib.on_loop(None)
            draw()

    def on_expose() -> None:
        """窓の再表示が必要になったら、最後に描いた画像を転送し直す。"""
        if controller.state.running:
            minilib.present()

    if animating:
        minilib.on_loop(animate)
    minilib.on_key(on_key)
    minilib.on_expose(on_expose)

    try:
        # SPEED=0 ならフックを使わず、一度で全体を描く。
        minilib.run(None if animating else draw)
    finally:
        controller.state.running = False
