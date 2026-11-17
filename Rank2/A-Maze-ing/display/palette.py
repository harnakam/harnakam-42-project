#!/usr/bin/env python3

"""すべてのバックエンドで共通の色の定義。"""

# 色は RGB で1か所にだけ書く。RGB はどのバックエンドにも依存しない色の表し方で、
# 各バックエンドは RGB を自分の形式に変換する
# (端末は 24bit カラーのエスケープシーケンス、MLX はピクセルのバイト列)。
# そのため、色を足すときに直すのはここだけでよい。

RGB = tuple[int, int, int]

# MLX の黒背景。入口・出口は濃い色で、壁と経路はパステル。
BACKGROUND_COLOR = 0xFF000000
DEFAULT_WALL_COLOR = 0xFFD8D3C6
ENTRY_COLOR = 0xFF00994C
EXIT_COLOR = 0xFFCC3344
FORTYTWO_COLOR = 0xFFD8D3C6

# 定義順がそのまま [c] キーで壁の色が切り替わる順になる
# (None はバックエンドの標準の色: 端末なら色なし、MLX なら白)
WALL_COLORS: dict[str, RGB | None] = {
    "default": None,
    "red": (230, 181, 187),
    "green": (179, 214, 190),
    "yellow": (231, 213, 165),
    "blue": (171, 203, 229),
}

# 最初に表示する壁の色 (WALL_COLORS の先頭)
INITIAL_WALL_COLOR: str = next(iter(WALL_COLORS))

# 壁が "default" のときの経路の色
DEFAULT_PATH_COLOR: str = "blue"

# None (標準の色) を除いた、実際に色が決まっているものだけ
_VISIBLE: dict[str, RGB] = {
    name: rgb for name, rgb in WALL_COLORS.items() if rgb is not None
}


def next_color(color: str) -> str:
    """color の次の壁の色を返す。

    順番は WALL_COLORS の定義順で、最後の色の次は先頭に戻る。

    Args:
        color: WALL_COLORS にある色の名前。

    Returns:
        次の色の名前。

    Raises:
        ValueError: color が WALL_COLORS にない場合。
    """
    names = list(WALL_COLORS)
    return names[(names.index(color) + 1) % len(names)]


def path_color_for(wall_color: str) -> RGB:
    """壁の色 wall_color と組み合わせる経路の色を返す。

    実際に色が決まっているものの中で wall_color の次の色にするので、
    壁と同じ色にはならない。"default" (色が決まっていないもの) なら
    DEFAULT_PATH_COLOR にする。

    Args:
        wall_color: WALL_COLORS にある色の名前。

    Returns:
        経路の色の RGB。
    """
    # 壁の色の「次の色」を経路の色にする (blue の次は red に戻る)。
    # 例: 壁 red -> 経路 green, 壁 green -> 経路 yellow
    if wall_color not in _VISIBLE:
        return _VISIBLE[DEFAULT_PATH_COLOR]
    names = list(_VISIBLE)
    return _VISIBLE[names[(names.index(wall_color) + 1) % len(names)]]
