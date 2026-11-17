*This project has been created as part of the 42 curriculum by smukai, harnakam.*

# A-Maze-ing

## Description

設定ファイルを読み込んで迷路を生成し、決められた形式のファイルに書き出したうえで、端末（ASCII）または MiniLibX（MLX）のウィンドウに表示するプログラムです。

- 迷路のサイズ、入口、出口、完全迷路にするかどうかなどを、設定ファイルで指定します。設定ファイルの例を config.txt として同梱しており、Makefile の `make run` も既定でこれを読みます。
- 迷路の中央には、閉じたセルで「42」の模様を描きます。
- 生成した迷路と、入口から出口への最短経路を出力ファイルに書き出します。
- 迷路を生成する部分は、独立したモジュール `mazegen` として切り出してあります。pip でインストールすれば、ほかのプロジェクトからも再利用できます（「再利用できる部分」を参照）。

## Instructions

### 必須要件

- Python 3.10 以上
pyproject.tomlでもこれを要求しています。

### インストール

```bash
make install
```

`.env/` に仮想環境を作り、`requirements.txt` のパッケージをインストールします。MLX の Python ラッパー（`mlx-2.2-py3-none-any.whl`）が同じディレクトリにある前提です。

### 実行

```bash
make run                      # .env の Python で config.txt を読んで実行する
make run CONFIG=config2.txt   # 別のtxtファイルを参照することも可能
.env/bin/python a_maze_ing.py config.txt   # make を使わずに実行する場合
```

`python3 a_maze_ing.py config.txt` のように直接実行する場合は、`make install` で作った仮想環境（`.env`）を有効にしておく必要があります（python-dotenv が見つからないと、メッセージを出して終了します）。

実行すると迷路が生成され、設定ファイルの `DISPLAY` に従って表示されます。既定は端末への ASCII 表示で、`DISPLAY=mlx` なら MiniLibX のウィンドウ、`DISPLAY=auto` なら MLX を試して使えなければ ASCII に切り替えます。キー操作は次のとおりです。

| キー | 操作 |
|---|---|
| `c` | 壁の色を切り替える |
| `q`| 終了する（MLX では Esc も同じ） |
| `r` | 迷路を作り直し、出力ファイルも上書きする |
| `p` | 最短経路の表示を切り替える |
| 矢印キー | （ASCII のみ）迷路が端末に収まらないとき、見える範囲をスクロールする |

なお、MLX表示においては迷路生成時にアニメーションが表示されます。

### そのほかの Makefile のルール

| コマンド | 内容 |
|---|---|
| `make debug` | pdb で実行する |
| `make lint` | flake8 と mypy（課題が指定するフラグ）でチェックする |
| `make lint-strict` | flake8 と `mypy --strict` でチェックする |
| `make build` | `mazegen` パッケージをビルドし、wheel を `submit/` 直下に置く |
| `make clean` | `__pycache__` などのキャッシュを削除する |

## ディレクトリ構成

```
submit/
├── a_maze_ing.py                    # エントリーポイント。設定の読み込み → 生成 → 書き出し → 表示
├── maze_file.py                     # 迷路を出力ファイルの形式で書き出す（読み込みはデバッグ用）
├── config.txt                       # 設定ファイルの例（make run が既定で読む）
├── Makefile                         # install / run / debug / lint / build / clean
├── requirements.txt                 # 開発・実行に使うパッケージ（make install で入る）
├── mlx-2.2-py3-none-any.whl         # MLX の Python ラッパー（同梱）
├── pyproject.toml                   # mazegen パッケージのビルド設定
├── mazegen-1.0.0-py3-none-any.whl   # ビルドした mazegen パッケージ（make build で更新）
├── LICENSE.md                       # MIT License
├── README.md                        # このファイル
│
├── mazegen/                         # 迷路生成モジュール（再利用できる部分。wheel に入る）
│   ├── __init__.py                  #   公開する名前（MazeGenerator, Maze, Coordinate, Wall など）
│   ├── README.md                    #   モジュールの説明（wheel にも同梱）
│   ├── maze_generator.py            #   MazeGenerator：入力の検証、生成の流れ、最短経路
│   ├── maze.py                      #   Mazeクラス（生成結果）と Coordinateクラス（座標）の定義
│   ├── wall.py                      #   壁のビット（北=0001、東=0010、南=0100、西=1000）の列挙型Wallの定義
│   ├── grid.py                      #   生成途中の迷路に対応するGridクラスの定義　Mazeと異なり内部専用
│   ├── braid.py                     #   PERFECT=False のときの編み込み用アルゴリズム
│   ├── validate.py                  #   生成した迷路の有効性の判定（InvalidMazeError）
│   └── algorithms/                  #   壁を掘るアルゴリズムのディレクトリ
│       ├── __init__.py              #     ALGORITHMS（名前 → 関数の表）
│       ├── recursive_backtracker.py #     backtracker: バックトラック法（デフォルトのアルゴリズム）
│       ├── kruskal.py               #     kruskal: kruskal法
│       └── growing_tree.py          #     growing_tree: Growing Tree 法
│
└── display/                         # 迷路の表示とキー操作
    ├── __init__.py                  #   run()：表示の入口。DISPLAY に従ってバックエンドを選ぶ
    ├── controller.py                #   キー → 操作（再生成、経路、色、終了）
    ├── scene.py                     #   何を描くか（描き方とは独立）
    ├── palette.py                   #   色の定義
    ├── display_ascii.py             #   端末に ASCII で描く（矢印キーでスクロール）
    ├── terminal.py                  #   端末の低レベルな入出力（キー入力、画面の切り替え）
    ├── display_mlx.py               #   MLX のウィンドウに描く（生成過程のアニメーション）
    └── Minilib.py                   #   MLX の呼び出しをまとめたラッパー
```

## 設定ファイル

1行に1つ、`KEY=VALUE` の形で書きます。

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
ALGORITHM=backtracker
```

| キー | 必須 | 値 | 説明 |
|---|---|---|---|
| `WIDTH` | 必須 | 整数（420 以下） | 迷路の幅（セル数） |
| `HEIGHT` | 必須 | 整数（420 以下） | 迷路の高さ（セル数） |
| `ENTRY` | 必須 | `x,y` | 入口の座標。左上が `0,0`、x が列、y が行 |
| `EXIT` | 必須 | `x,y` | 出口の座標。入口とは別のセルにする |
| `OUTPUT_FILE` | 必須 | パス | 迷路の書き出し先。相対パスは実行したディレクトリが基準 |
| `PERFECT` | 必須 | `True` / `False` | `True` なら入口と出口を結ぶ経路がただ1つの迷路（完全迷路）、`False` なら閉路を含む迷路 |
| `SEED` | 任意 | 整数 | 乱数のシード値。同じ値なら同じ迷路になる。省略すると毎回異なる |
| `ALGORITHM` | 任意 | `backtracker` / `kruskal` / `growing_tree` | 迷路を掘るアルゴリズム。省略時は `backtracker` |
| `DISPLAY` | 任意 | `ascii` / `mlx` / `auto` | 表示方法。`ascii` は端末、`mlx` は MiniLibX のウィンドウ、`auto` は MLX を試して使えなければ ASCII。省略時は `ascii` |

- `#` から行末まではコメントとして無視されます（行の途中からでも構いません）。空行も無視されます。
- `=` の前後の空白は無視されます。
- 同じキーを2回書いた場合は、後に書いた値が使われます。
- 知らないキーは無視されます。
- 必須のキーが無い場合や、値が不正な場合は、エラーメッセージを出して終了します。
- `WIDTH` と `HEIGHT` の上限は 420 です。超えた場合は、メモリを使い切って異常終了するのを防ぐため、エラーメッセージを出して終了します。
- 迷路が小さすぎて「42」の模様が入らない場合や、模様で残りのセルが分断されてしまう場合（結果として `WIDTH <= 8` または `HEIGHT <= 5`）は、警告を出し、模様を省いて生成します。模様を置ける大きさでは、模様が四隅や中央を塞ぐことはありません。
- `PERFECT=False` では閉路が2つ以上必要です。幅か高さが 1 の迷路や 2×2 の迷路では閉路を2つ作れないので、エラーメッセージを出して終了します（「42」が無い迷路で作れる閉路は最大 (幅 − 1) × (高さ − 1) 個）。
- 生成した迷路が有効でない場合（後述）も、エラーメッセージを出して終了します。

パースにはdotenvを使用しているので、細かい仕様はそちらに準拠しています。

### 出力ファイルの形式
課題の要請通り、「壁の配置の16進数表記」「入口・出口の座標」「最短経路の進み順（`N`、`E`、`S`、`W`）」を順にtxtファイルに書き出しています。
```
D517BB9517
9529044787
AFC2AFFF83
EFD6857FAE
BFFFAFFFC3
C17FAFD516
D2BFEFFFAB
9405391106
C383C6AAC3
D6EC57EC7E

0,0
3,3
EESSES
```

## 迷路生成アルゴリズム

`ALGORITHM` で次の3つから選べます。

- **Recursive Backtracker（深さ優先探索、既定）**: 開始セルから、まだ訪れていない隣のセルをランダムに選んで掘り進め、進めなくなったら戻る方法です。Python の再帰の上限を避けるため、再帰ではなく明示的なスタックで実装しています。
- **Randomized Kruskal's**: すべての壁をランダムな順に見ていき、両側のセルがまだつながっていなければ壊す方法です。つながっているかどうかは Union-Find（素集合データ構造）で判定しています。
- **Growing Tree**: 掘り進める途中のセル（活性セル）の一覧を持ち、そこから1つ選んで、まだ訪れていない隣のセルへ掘り進める方法です。隣がなくなったセルは一覧から外します。どのセルを選ぶかで性質が変わり、この実装では 10% の確率で最も新しく加えたセル、それ以外は一覧からランダムに選びます。

どのアルゴリズムも、`PERFECT=True` のときは完全迷路（閉路のない迷路）を作ります。`PERFECT=False` のときは、加えて行き止まりの壁をすべて壊して閉路を作ります(編み込み/braiding)。課題のBonusではそれでも閉路が2つに満たなければ（例えば一筆書きの迷路の両端がつながっただけのとき）、ランダムな壁を追加で開けます。最後に、3×3 の開けた空間ができた場所は、中央の壁を1枚閉じて潰します（`mazegen/braid.py`）。3×3 の空間は内側に閉路を4つ持つので、壁を1枚閉じても閉路は2つを下回りません。

これらのアルゴリズムを選んだ強い理由はありません。平易なアルゴリズムということで素朴に実装しています。

生成した迷路は、最後に有効かどうかを判定します（`mazegen/validate.py`）。生成の処理と判定の処理は分けてあり、判定する条件は次のとおりです。

- 隣り合うセルの壁が食い違っておらず、外周の壁と「42」のセルの壁がすべて閉じている
- 「42」以外のすべてのセルがつながっている
- 3×3 の開けた空間がない
- `PERFECT=True` なら閉路がない、`PERFECT=False` なら閉路が2つ以上ある
- `PERFECT=False` なら、四隅と中央が「42」で塞がれておらず、行き止まりがない（閉じた壁の先がすべて「42」か外周である袋小路は除く）。幅や高さが偶数のときは、中央を囲むセルのどれかが通路であればよいとします

## 再利用できる部分

迷路を生成する部分は、パッケージ `mazegen`（`mazegen/`）として独立させています。表示や設定ファイルの読み込みには依存しません。

ビルドしたファイル `mazegen-1.0.0-py3-none-any.whl` はリポジトリ直下に置いてあり、pip でインストールできます(詳細は `mazegen/README.md` に記載)。 `make build` を実行すればいつでもリビルドが可能です。

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

使い方:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    20, 15,           # 幅、高さ
    (0, 0), (19, 14), # 入口、出口
    True,             # 完全迷路にするか
    algorithm="kruskal",   # 省略可（既定は "backtracker"）
    seed=42,               # 省略可
)
maze = generator.generate_maze()

maze.cells[y][x]   # セルの壁（北=1、東=2、南=4、西=8 のビット）
maze.path          # 入口から出口への最短経路。例: "EESEN..."
maze.entry, maze.exit
```

## チームとプロジェクト管理
### roles
- smukai: mazegenモジュール、a_maze_ing.py、Makefile、displayモジュールの設計、ASCII表示を担当しました。
- harnakam: growing treeアルゴリズム、mlxのdisplayを担当しました。

### anticipated planning and how it evolved until the end
- smukai: 後学のためコードの凝集度・結合度を意識する&デザインパターンに基づいた実装を試みる方針を設定しました。とはいえ、コードを書きながらアドホックな修正を繰り返すことが多く、事前に緻密に設計するようなコーディングができなかったのが心残りです。
- harnakam: 事前に細かい計画を立てていたわけではなく、Growing TreeアルゴリズムとMLXによる表示を担当し、必要なものから順に実装していきました。実装を進める中で他のメンバーが書いたコードを読む必要がありましたが、想像していた以上に理解することが難しかったです。そのため、実装しながら既存コードの構造を確認し、必要に応じて理解や実装方針を修正していく形になりました。

### What worked well and what could be improved
- smukai: mazegenのFacadeパターンについてはある程度満足行く実装ができたと思います。提出物全体の設計に関しては改善の余地があるかもしれませんし、個々のコードはともかく全体の設計についてはチーム内でじゅうぶん吟味することなく実装を進めてしまったので、反省しています。
- harnakam: Growing TreeアルゴリズムとMLXによる表示について、最終的には既存のコードと組み合わせて動作する形まで実装できた点は良かったと思います。一方で、理解がかなり抽象的なまま進めてしまうことがあり、「なんとなく理解して使える」状態にはなっても、同じ構造を自分で一から再現できるほどには理解できていない部分があります。今後は、コードの動作だけでなく、再現性や構造的な理解を深めたいと思います。

### used any specific tools

- smukai: 進捗の管理に際してGitHubを利用した。また後述の通りClaude Codeを用いている。
- harnakam: バージョン管理やコードの共有にはGitおよびGitHub、ghを使用しました。実装、コードの読解、デバッグや修正の補助、前提知識の検索等にChatGPTおよびCodexも利用しました。

## Resources
### 参考資料
- smukai: 
    - [The Buckblog（Jamis Buck）: Maze Generation シリーズ](https://weblog.jamisbuck.org/under-the-hood/)
    - [Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking.html)
    - [Kruskal's Algorithm](https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm)
    - [Think Labyrinth: Maze Glossary](https://www.astrolog.org/labyrnth/glossary.htm)（braid maze、perfect maze などの用語）
- harnakam: 
    - [A-Maze-ing subject PDF](https://cdn.intra.42.fr/pdf/pdf/228460/en.subject.pdf)
    - [The Buckblog（Jamis Buck）: Growing Tree Algorithm](https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm)

### AI の使い方
- smukai: デザインパターンの実現や知らないモジュールの知識の保管などに際してClaude Code（Anthropic）とかなり相談しました。なお、AIの生成物をそのまま流用するようなことは行っていません。
- harnakam: Growing TreeアルゴリズムやMiniLibXを用いた描画処理について、実装方法の確認や既存コードの読解、デバッグの補助としてChatGPTおよびCodexを使用しました。また、GUIのウィンドウサイズや描画サイズ、色合いなど、視覚的な調整にはVibe Codingを利用しました。AIの出力はそのまま採用するのではなく、実際のコードや動作を確認しながら修正して使用しました。

## License

`mazegen` を含むこのプロジェクトのコードは、MIT License で公開しています。詳しくは `LICENSE.md` を参照してください。
