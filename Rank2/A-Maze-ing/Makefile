VENV := .env
PYTHON := $(VENV)/bin/python

# make runの際に「CONFIG=」で読むファイルを指定できる、ない場合のデフォルト値はconfig.txt
CONFIG ?= config.txt

# make install が終わった目印に「.installed」というファイルを作る
# これより requirements.txt や MLX の wheel が新しければmake は install をやり直す
INSTALLED := $(VENV)/.installed

#MLXを使うに際して、必要なファイルがあることを名前で決め打ちしている(のであまりよくない)
MLX_WHEEL := mlx-2.2-py3-none-any.whl

# lint で使う mypy のフラグ (pdf の指定どおり)
#   --warn-return-any        型が Any の値を、Any 以外の戻り値型の関数から返すと警告する
#   --warn-unused-ignores    不要になった `# type: ignore` を警告する
#   --ignore-missing-imports 型情報のないライブラリの import エラーを無視する
#   --disallow-untyped-defs  型注釈のない関数定義をエラーにする
#   --check-untyped-defs     型注釈のない関数の中身も型チェックする
MYPY_FLAGS := --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs
# flake8 が見ないディレクトリ（仮想環境とビルドの生成物）
# --extend-exclude は .git や __pycache__ などの既定の除外に「追加」する
FLAKE8_FLAGS := --extend-exclude $(VENV),build,dist,*.egg-info
MYPY := $(PYTHON) -m mypy

.PHONY: install run debug lint lint-strict clean build

$(PYTHON):
	python3 -m venv $(VENV)

# 最初に書いたこれが「make」で実行される
install: $(INSTALLED)

# | の右は「順序だけの依存」: venv がなければ先に作るが、venv の更新時刻が
# 変わっても install はやり直さない
$(INSTALLED): requirements.txt $(MLX_WHEEL) | $(PYTHON)
# 無難にpipでインストール
# uvは速いが追加インストールが必要
# pipxはプロジェクトの依存ライブラリを入れる用途ではないので不向き（？）
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	touch $@

# install より前に run しても、先に install が走る
# (依存ライブラリがないまま実行して import エラーになるのを防ぐ)
run: $(INSTALLED)
# デフォルトでconfig.txtを読む仕様にする
# "CONFIG=xxx.txt"のように変更も可能
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug: $(INSTALLED)
# pdfの要請通りpdbで動く
#   主なコマンド:
#     n (next)     : 次の行へ (関数の中には入らない)
#     s (step)     : 次の行へ (関数の中に入る)
#     c (continue) : 次のブレークポイントまで実行
#     b 42         : 42行目にブレークポイントを置く (b ファイル名:行番号 も可)
#     p 変数名     : 変数の値を表示        l : 周辺のソースを表示
#     w            : 呼び出し履歴(スタック)を表示   q : 終了
#   コード中に `breakpoint()` と書くと、普通に実行してもそこで pdb が起動する。
#   また例外で落ちた場合は、落ちた地点で止まって中身を調べられる(post-mortem)。
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

lint: $(INSTALLED)
	$(PYTHON) -m flake8 . $(FLAKE8_FLAGS)
	$(MYPY) . $(MYPY_FLAGS)

lint-strict: $(INSTALLED)
	$(PYTHON) -m flake8 . $(FLAKE8_FLAGS)
	$(MYPY) . --strict

# キャッシュを削除
clean:
	find . -path ./$(VENV) -prune -o -type d \
		\( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) \
		-prune -exec rm -rf {} +

# ビルド用のコマンド
# pyproject.tomlに詳細を書いておく、これを見て書き出す
build: $(INSTALLED)
	rm -rf dist
	$(PYTHON) -m build
# バージョンは pyproject.toml で決まるので、ファイル名は決め打ちしない
# (直前に dist/ を消しているので、dist/ にある wheel は今回作った1つだけ)
	cp dist/mazegen-*.whl .
# wheel を submit/ に取り出したら dist/ は不要なので消す
# dist/ には sdist（.tar.gz）も入っているため rmdir ではなく rm -rf を使う
	rm -rf dist mazegen.egg-info
