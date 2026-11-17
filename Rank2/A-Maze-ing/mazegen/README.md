# mazegen

迷路を生成する再利用可能な Python モジュールです（A-Maze-ing プロジェクト）。
Python 3.10 以上で動作し、標準ライブラリ以外への依存はありません。

## インストール

標準的な whl ファイルの扱いに準じます。例えば pip を使う場合は以下を実行してください。

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## 公開しているもの

`from mazegen import ...` で以下を利用できます。

```python
class MazeGenerator(
        width: int, height: int,                          # 迷路のサイズ（セル数）
        entry_coordinate: Coordinate | tuple[int, int],   # 入口の座標
        exit_coordinate: Coordinate | tuple[int, int],    # 出口の座標
        is_perfect: bool,                                 # True なら経路がただ1つ
        algorithm: str = DEFAULT_ALGORITHM,               # アルゴリズム名（省略可）
        seed: int | None = None,                          # 乱数のシード値（省略可）
        )
    def generate_maze(self) -> Maze: ...                  # 迷路を生成して返す

@dataclass(frozen=True)
class Maze:                    # 生成結果
    cells: list[list[int]]     # 各セルの壁のビット。cells[y][x]
    entry: Coordinate          # 入口
    exit: Coordinate           # 出口
    path: str                  # 入口から出口への最短経路（"N", "E", "S", "W" の並び）
    steps: tuple[WallChange, ...]  # 生成過程（壁を開けた・閉めた順）
    width: int                 # 列数（プロパティ）
    height: int                # 行数（プロパティ）

class Coordinate(NamedTuple):  # セルの座標
    x: int                     # 列（左端が 0）
    y: int                     # 行（上端が 0）

class WallChange(NamedTuple):  # 生成過程の1手
    pos: Coordinate            # 壁を変えたセル
    direction: Wall            # pos のどの壁か（隣のセルの反対側の壁も同時に変わる）
    opened: bool               # True なら開けた、False なら閉めた

class Wall(IntFlag):           # 壁のビット
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

AVAILABLE_ALGORITHMS = ("backtracker", "growing_tree", "kruskal")  # algorithm= に渡せる名前の一覧
DEFAULT_ALGORITHM = "backtracker"                   # algorithm= を省略したときの名前
```

## パラメータ

- `width`, `height`: 迷路のサイズ（セル数）です。
- `entry_coordinate`, `exit_coordinate`: 入口・出口の座標 `(x, y)` です。
  `Coordinate` でも普通のタプルでも渡せます。迷路の範囲内で、互いに別のセルである必要があります。
- `is_perfect`: `True` なら入口と出口を結ぶ経路がただ1つの迷路（完全迷路）を、
  `False` なら閉路を含む迷路を生成します。
- `algorithm`: 迷路を掘るアルゴリズムの名前です。省略時は `DEFAULT_ALGORITHM` を使います。
  選べる名前は `AVAILABLE_ALGORITHMS` で確認できます。
  `"growing_tree"`（Growing Tree）は、活動中のセルから最新のものかランダムなものを選んで掘り進めます。

  ```python
  import mazegen
  print(mazegen.AVAILABLE_ALGORITHMS)   # ('backtracker', 'growing_tree', 'kruskal')
  ```

- `seed`: 乱数のシード値です。同じ引数（同じ `seed`）で作った `MazeGenerator` は同じ迷路を生成します。
  省略すると実行のたびに異なる迷路になります。

## 基本的な使い方

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, (0, 0), (19, 14), True)
maze = generator.generate_maze()

maze.cells[0][0]   # 左上のセルの壁（cells[y][x]）
maze.path          # 入口から出口への最短経路。例: "EESEEN..."
```

### エラーと警告

- 次の場合は `ValueError` を送出します。
  - `width` または `height` が負
  - 入口と出口が同じセル
  - 入口または出口が迷路の範囲外、または「42」の模様の上
  - `algorithm` が `AVAILABLE_ALGORITHMS` に無い
  - `is_perfect=False` で、迷路が小さすぎて閉路を2つ作れない（幅か高さが 1、または 2×2）。
    「42」が無い迷路で作れる閉路は最大 (width − 1) × (height − 1) 個なので、これが2未満になる大きさです
- `generate_maze()` は、生成した迷路が次の条件のどれかを満たさない場合に
  `RuntimeError` を送出します（入力の誤りではなく、生成の処理の不具合を表すため）。
  - 隣り合うセルの壁が食い違っておらず、外周の壁と「42」のセルの壁がすべて閉じている
  - 「42」以外のすべてのセルがつながっている
  - 3×3 の開けた空間がない
  - `is_perfect=True` なら閉路がない、`False` なら閉路が2つ以上ある
  - `is_perfect=False` なら、四隅と中央が「42」で塞がれておらず、行き止まりがない（閉じた壁の先がすべて「42」か外周である袋小路は除く）。
    幅や高さが偶数のときは、中央を囲むセルのどれかが通路であればよいとします。
    この迷路の壁はセルとセルの間の線で、セルはすべて通路なので、「中央が通路」は
    「中央のセルが『42』で塞がれていない」という意味になります

  コンストラクタが `ValueError` を出さなかった入力では、生成アルゴリズムがこれらの条件を満たすように作るので、
  この `RuntimeError` は通常は起きません。万一の不具合に備えた安全装置です。
- 迷路の中央には、閉じたセルで「42」の模様を描きます。模様は「4」と「2」（それぞれ 3×5 セル）を
  横に並べたもので、間は迷路の幅が奇数なら1列、偶数なら2列空けます（模様の幅は 7 か 8 セル）。
  こうすると模様が左右ちょうど中央に来て、間の空き列がそのまま迷路の中央の列になるので、
  中央のセルが「42」で塞がれることはありません。四隅にかかることもありません。
- 迷路が小さく模様が入らない、または模様で残りのセルが分断される場合
  （結果として `width <= 8` または `height <= 5`）は、`UserWarning` を出して模様を省きます。

## 生成結果の読み方

### 壁（`cells`）

各セルは4ビットの整数で、閉じている壁のビットが 1 になります（北=1, 東=2, 南=4, 西=8）。
例えば `0xd`（= 1 + 4 + 8）は、東だけが開いているセルです。「42」の模様のセルは
すべての壁が閉じた `0xf` になります。

```python
from mazegen import Wall

Wall.has_wall(maze.cells[0][0], Wall.NORTH)   # True なら北の壁が閉じている
```

### 解（`path`）

入口から出口への最短経路が、進む方向の文字（`N`, `E`, `S`, `W`）の並びで入っています。
例えば `"NESSW"` は「北→東→南→南→西」と進むことを表します。
各文字に対応する座標の変化は `Wall` から取得できます。

```python
from mazegen import Coordinate, Wall

letter_to_wall = {wall.letter: wall for wall in Wall}   # {"N": Wall.NORTH, ...}

pos = maze.entry
for letter in maze.path:
    dx, dy = letter_to_wall[letter].delta   # 例: N なら (0, -1)
    pos = Coordinate(pos.x + dx, pos.y + dy)
assert pos == maze.exit
```

### 生成過程（`steps`）

迷路を作るときに壁を開けた・閉めた順番が、`WallChange` の並びで入っています。
生成は「すべての壁が閉じた盤面」から始まるので、そこに `steps` を先頭から順に当てると、途中の様子を再現できます。
すべて当て終えると `cells` と一致します。
`PERFECT=False` の迷路では、一度開けた壁を閉め直す手（`opened=False`）も含まれます。

```python
from mazegen import Wall

cells = [[0b1111] * maze.width for _ in range(maze.height)]
for pos, direction, opened in maze.steps:
    dx, dy = direction.delta
    change = Wall.remove_wall if opened else Wall.add_wall
    cells[pos.y][pos.x] = change(cells[pos.y][pos.x], direction)
    cells[pos.y + dy][pos.x + dx] = change(
        cells[pos.y + dy][pos.x + dx], direction.opposite
    )
assert cells == maze.cells
```

ファイルから読み込んだ迷路など、生成過程を持たない `Maze` では `steps` は空です。
