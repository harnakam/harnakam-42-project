#!/usr/bin/env python3


"""迷路を出力ファイルの形式で書き込み、読み込む。"""

from pathlib import Path

from mazegen import Coordinate, Maze

# 出力ファイル形式の空行の数。write側・read側の両方がここを参照する
GRID_BLANK_LINES = 1  # マス目のセクションのあとに挟む空行の数
PATH_BLANK_LINES = 0  # entry/exit座標のセクションのあとに挟む空行の数


def _format_maze_output(maze: Maze) -> str:
    """迷路を出力ファイルの形式の文字列にする。

    各セルを16進数1文字で表したマス目、空行、入口と出口の座標、
    最短経路の順に並べる。

    Args:
        maze: 書き出す迷路。

    Returns:
        ファイルにそのまま書き込める文字列。末尾は改行。
    """
    rows: str = "".join(
        # maze.cells(list[list[int]])を大文字の16進数に変換
        # 改行区切りのstrにする
        "".join(format(cell, "X") for cell in row) + "\n"
        for row in maze.cells
    )
    grid_gap = "\n" * GRID_BLANK_LINES
    path_gap = "\n" * PATH_BLANK_LINES
    return (
        f"{rows}{grid_gap}"
        f"{maze.entry.x},{maze.entry.y}\n"
        f"{maze.exit.x},{maze.exit.y}\n"
        f"{path_gap}"
        f"{maze.path}\n"
    )


def write_maze_file(path: Path, maze: Maze) -> None:
    """迷路を出力ファイルの形式で path に書き込む。

    ファイルがすでにあれば上書きする。

    Args:
        path: 書き込むファイルのパス。
        maze: 書き込む迷路。

    Raises:
        OSError: ファイルを書き込めない場合。
    """
    # 具体的なデータ整形は_format_maze_output()でやっている
    # 公開するインターフェースにロジックをベタ書きするとインターフェースの修正でバグが生じやすい
    # ロジックだけ分離することでデバッグがやりやすくなる、というメリットも
    with path.open("w", encoding="utf-8") as f:
        f.write(_format_maze_output(maze))


# 以下はデバッグ用の関数
# 書き出したテキストからMazeを再構成する

def _parse_coordinate(line: str) -> Coordinate:
    """座標の行 ("x,y" の形) を Coordinate にする。

    末尾の "# ..." のコメントと両端の括弧は無視するので、
    "(1, 2)  # comment" のような行も読める。

    Args:
        line: 座標が書かれた1行。

    Returns:
        読み取った座標。

    Raises:
        ValueError: カンマ区切りの整数2つとして読めない場合。
    """
    # "(1, 2)  # comment" を3段階で剥がして "1, 2" にする:
    # split("#", 1)[0] で末尾のコメントを落とす
    # strip()でその前後の空白を除去
    # strip("()") で両端を見て「(」と「)」をすべて除去
    value = line.split("#", 1)[0].strip().strip("()")
    try:
        x, y = (int(part) for part in value.split(","))
    except ValueError:
        # 空文字などもわかりやすく見せてほしいので!rをつけている
        # 新たな例外をraiseするとTracebask表示が2つになるのでfrom Noneをつける
        raise ValueError(f"invalid coordinate: {line!r}") from None
    return Coordinate(x, y)


def _parse_maze(text: str, allow_empty_path: bool = False) -> Maze:
    """出力ファイルの形式の文字列から Maze を作り直す。

    Args:
        text: 出力ファイルの中身。
        allow_empty_path: True なら最短経路が空の迷路 (出口に到達できない、
            デバッグ用に書き出した無効な迷路) も受け付ける。

    Returns:
        読み取った Maze。生成過程 (steps) は空になる。

    Raises:
        ValueError: 形式が正しくない場合。
    """
    lines = [line.strip() for line in text.splitlines()]
    # マス目の直後にある空行の位置。空行がなければマス目が最後まで続く
    grid_end = lines.index("") if "" in lines else len(lines)
    grid_lines = lines[:grid_end]
    if not grid_lines:
        raise ValueError("maze is empty")
    cells: list[list[int]] = []
    for row in grid_lines:
        try:
            # 16進数として読んでいく
            cells.append([int(char, 16) for char in row])
        except ValueError:
            raise ValueError(f"invalid maze row: {row!r}") from None
    if any(len(row) != len(cells[0]) for row in cells):
        raise ValueError("maze rows have different lengths")
    entry_index = grid_end + GRID_BLANK_LINES
    exit_index = entry_index + 1
    path_index = exit_index + 1 + PATH_BLANK_LINES
    try:
        entry = _parse_coordinate(lines[entry_index])
        exit_ = _parse_coordinate(lines[exit_index])
        path = lines[path_index]
    except IndexError:
        raise ValueError("entry, exit or path is missing") from None
    # pathが空の場合もエラー (無効な迷路を読むときだけ許す)
    if not path and not allow_empty_path:
        raise ValueError("path is missing")
    return Maze(cells=cells, entry=entry, exit=exit_, path=path)


def read_maze_file(path: Path, allow_empty_path: bool = False) -> Maze:
    """出力ファイルを読み、書かれている Maze を返す。

    Args:
        path: 読み込むファイルのパス。
        allow_empty_path: True なら最短経路が空の迷路 (出口に到達できない、
            デバッグ用に書き出した無効な迷路) も受け付ける。

    Returns:
        読み取った Maze。生成過程 (steps) は空になる。

    Raises:
        OSError: ファイルを読めない場合。
        ValueError: 形式が正しくない場合。
    """
    return _parse_maze(path.read_text(encoding="utf-8"), allow_empty_path)
