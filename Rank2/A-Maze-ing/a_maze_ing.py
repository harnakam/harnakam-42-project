#!/usr/bin/env python3

"""A-Maze-ing のエントリーポイント。

設定ファイルを読み、迷路を生成して出力ファイルに書き込み、画面に表示する。

使い方:
    python3 a_maze_ing.py <config_file_path>
"""

# loggingはログを管理するための標準ライブラリモジュール
# https://docs.python.org/ja/3/library/logging.html
# よく使われるものなので、mazegenモジュールの出力をこれに投げるのも妥当なはず
# このファイルでも logging で出力を制御する
import io
import logging
import sys
import warnings
from os import environ
# @dataclassはデータを格納するクラスを扱うのに便利なデコレータ
# https://docs.python.org/ja/3/library/dataclasses.html
# 型ヒント付きのフィールドから __init__() や __repr__()などのメソッドを自動生成する
# 入力の整形は__init__()内ではなくクラスメソッドでやる
# mypy が __init__() の引数の型をチェックできるのは辞書より嬉しい
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Callable, TypeVar

# python-dotenv: 環境変数まわりを扱うためのライブラリ
# KEY=VALUE形式のファイルをパースするためにも使える
# https://pypi.org/project/python-dotenv/
# make install を済ませずに実行したときに Traceback で落ちないよう、
# import の失敗もメッセージにして終了する
try:
    from dotenv import dotenv_values
    # dotenv_values は解析できない行を警告だけ出して読み飛ばすので、
    # 事前に parse_stream で全行を調べ、壊れた行があればエラーにする
    from dotenv.parser import parse_stream
except ImportError:
    sys.exit("python-dotenv is not installed: run `make install` first")

import display
import mazegen

from maze_file import write_maze_file


def strtobool(value: str) -> bool:
    """文字列を真偽値に変換する。

    Python 3.12以降はdistutils.util.strtobool が使えないので自分で実装。

    Args:
        value: "True", "true", "False", "false" のいずれか。

    Returns:
        変換した真偽値。

    Raises:
        ValueError: value が上記のいずれでもない場合。
    """
    if value == "True" or value == "true":
        return True
    if value == "False" or value == "false":
        return False
    raise ValueError(f"invalid truth value {value!r}")


# デバッグ用のログ。環境変数 LOGLEVEL=DEBUG をつけて実行すると stderr に出力される
# __name__  を渡すと、モジュールと同じ名前の Logger ができる
# どのモジュールが出したログかわかりやすい
# 公式の Logging HOWTO でも推奨されている書き方
logger = logging.getLogger(__name__)


def _setup_logging() -> None:
    """環境変数 LOGLEVEL に従って、ログの出力レベルを設定する。

    LOGLEVEL がなければ WARNING にする。warnings.warn() の警告も
    ログとして同じ形式で stderr に出す。

    Raises:
        SystemExit: LOGLEVEL が不正な場合。
    """
    # mazegenモジュールはログを出すだけで、出すかどうか・どこに出すかはここで決める
    # 環境変数LOGLEVELに出力レベルが入っている (既定は WARNING)
    # 出力先 (filename や stream) を指定していないので stderr に出力される
    level = environ.get("LOGLEVEL", "WARNING").upper()
    try:
        # ログレベルと出力フォーマットを指定
        logging.basicConfig(level=level, format="%(name)s: %(message)s")
    except ValueError:
        # LOGLEVELが不正だったらstderrにメッセージを出力して終了
        sys.exit(f"invalid LOGLEVEL: {level!r}")
    # warnings.warn() の警告も WARNING レベルのログとして扱い、
    # 同じ出力先・形式にそろえる
    logging.captureWarnings(True)
    # 既定の形式はファイル名・行番号・ソース行まで出すので、
    # 利用者向けに "UserWarning: <メッセージ>" だけにする
    warnings.formatwarning = _format_warning


def _format_warning(
    message: Warning | str, category: type[Warning],
    filename: str, lineno: int, line: str | None = None
) -> str:
    """警告を "<種類>: <メッセージ>" の形の文字列にする。

    warnings.formatwarning の代わりに使う。ファイル名・行番号などは
    表示しないので、それらの引数は使わない。

    Args:
        message: 警告のメッセージ。
        category: 警告の種類。
        filename: 警告が出たファイル名 (使わない)。
        lineno: 警告が出た行番号 (使わない)。
        line: 警告が出た行のソース (使わない)。

    Returns:
        表示する文字列。
    """
    return f"{category.__name__}: {message}"


def parse_config(config_path: Path) -> dict[str, str]:
    """設定ファイルを読み、KEY=VALUE の組を辞書にする。

    空行と # のコメントは読み飛ばし、キーと値の前後の空白は取り除く。
    同じキーが複数あれば後のものが優先される。値の型の変換はしない。

    Args:
        config_path: 設定ファイルのパス。

    Returns:
        キーから値 (文字列) への辞書。

    Raises:
        FileNotFoundError: ファイルがない場合。
        ValueError: 解析できない行や、"=" のない行がある場合。
    """
    if not config_path.is_file():
        raise FileNotFoundError("config file not found")
    # dotenv_valuesは空行・コメント行(#)のスキップ、行末コメント
    # ("KEY=value # comment" の " # comment" 部分)の除去、
    # キーと値の前後の空白除去、"KEY=VALUE"の分割を代わりにやってくれる
    # なお、同じキーが2回ある場合はエラーにならず、後に書いた値で上書きされる
    # 重複があるなら入力テキストの不備を疑いエラーを吐くのが望ましい？
    # 現状はdotenvの仕様を尊重し上書き仕様にしている
    text = config_path.read_text(encoding="utf-8")
    for binding in parse_stream(io.StringIO(text)):
        # 解析できない行と、"=" がない行 (キーだけ読まれて値が None) を拒否する
        no_equals = binding.key is not None and binding.value is None
        if binding.error or no_equals:
            # original.line は前の空行を含めた位置を指すので、
            # 先頭の改行の数だけずらして壊れた行そのものの行番号にする
            original = binding.original.string
            stripped = original.lstrip()
            lineno = binding.original.line + original[
                :len(original) - len(stripped)
            ].count("\n")
            reason = "line is not KEY=VALUE" if no_equals else "syntax error"
            raise ValueError(
                f"Error on parsing: line {lineno}: {reason}: "
                f"{stripped.rstrip()!r}"
            )
    # interpolate=Falseにしないと "${HOME}" のような値を環境変数で
    # 展開してしまうので、値をそのまま使うために無効化する
    raw = dotenv_values(stream=io.StringIO(text), interpolate=False)
    var_dict: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            raise ValueError(
                f"Error on parsing: line is not KEY=VALUE: {key!r}"
            )
        # 小文字の大文字化などは一応していない。するべきだと思ったら適宜やる
        var_dict[key] = value
        logger.debug("parsed: %s, %s", key, value)
    unknown_keys = var_dict.keys() - KNOWN_KEYS
    if unknown_keys:
        logger.debug("unknown keys: %s", ", ".join(sorted(unknown_keys)))
    return var_dict


# convert()は「受け取ったparseに対応した型を返す」という挙動をとる
# 「-> Any」と書くと広すぎて誤って挙動をmypyがチェックできない
# 型変数Tを定義して補っている
# このように型変数で「引数の型と戻り値の型の関係」を表す関数をジェネリック関数と呼ぶ
# https://docs.python.org/ja/3/library/typing.html#typing.TypeVar　も参照のこと
T = TypeVar("T")


def convert(key: str, parse: Callable[[str], T], value: str) -> T:
    """設定値を変換する。失敗したら、メッセージの先頭にキーを付ける。

    Args:
        key: 設定ファイルでのキー。エラーメッセージに使う。
        parse: 値を変換する関数 (int、strtobool など)。
        value: 変換する文字列。

    Returns:
        parse(value) の結果。

    Raises:
        ValueError: parse が ValueError を出した場合。メッセージは
            "<key>: <元のメッセージ>" になる。
    """
    try:
        return parse(value)
    except ValueError as error:
        # どのkeyの変換に失敗したのかは明示する
        raise ValueError(f"{key}: {error}") from None


def parse_coordinate(str_coordinate: str) -> mazegen.Coordinate:
    """座標の文字列 ("x,y" の形) を Coordinate にする。

    Args:
        str_coordinate: 座標の文字列。例: "0, 0"。数値の前後の空白は許す。

    Returns:
        読み取った座標。

    Raises:
        ValueError: カンマ区切りの整数2つでない場合。
    """
    split_coordinate: list[str] = str_coordinate.split(",")
    if len(split_coordinate) != 2:
        raise ValueError(f"invalid coordinate {str_coordinate!r}")
    return mazegen.Coordinate(
        int(split_coordinate[0]), int(split_coordinate[1])
    )


# WIDTH と HEIGHT の上限。大きすぎる迷路はメモリを使い切り、
# OS に強制終了されてエラーメッセージも出せないので、設定の段階で拒否する
# 値そのものは恣意的なもの。mazegen ではなくアプリ (このファイル) の制限
MAX_SIZE: int = 420


# frozen=Trueで簡単にイミュータブル（変更不能）にできる
# これもdataclassデコレータの恩恵
@dataclass(frozen=True)
class Config:
    """設定ファイルから読み、型を変換した設定値。

    設定ファイルでの各キーは、フィールド名を大文字にしたもの
    (例: width なら WIDTH)。既定値のないフィールドは必須、
    既定値のあるフィールドは省略できる。

    Attributes:
        width: 迷路の列数 (WIDTH)。
        height: 迷路の行数 (HEIGHT)。
        entry: 入口の座標 (ENTRY)。
        exit: 出口の座標 (EXIT)。
        perfect: 完全迷路にするかどうか (PERFECT)。
        output_file: 迷路を書き込むファイルのパス (OUTPUT_FILE)。
        seed: 乱数の種 (SEED)。省略すると実行ごとに異なる迷路になる。
        algorithm: 迷路を掘るアルゴリズムの名前 (ALGORITHM)。
        display: 表示方法 (DISPLAY)。auto, mlx, ascii のいずれか。
    """

    # Mandatory
    width: int
    height: int
    entry: mazegen.Coordinate
    exit: mazegen.Coordinate
    perfect: bool
    output_file: Path
    # Optional(has default value)
    seed: int | None = None
    algorithm: str = mazegen.DEFAULT_ALGORITHM
    display: str = "ascii"

    @classmethod
    def from_dict(cls, raw_data: dict[str, str]) -> "Config":
        """parse_config() が返した辞書から Config を作る。

        Args:
            raw_data: キーから値 (文字列) への辞書。

        Returns:
            型を変換した Config。

        Raises:
            ValueError: 必須のキーがない場合、値を変換できない場合、
                WIDTH か HEIGHT が MAX_SIZE を超える場合、
                または DISPLAY が不正な場合。
        """
        # 必須かどうかと既定値はここで判定
        # 必須のキーはrequired() で読み、任意のキーは書かれていたときだけ上書きする
        def required(key: str) -> str:
            """必須のキーの値を返す。

            Args:
                key: 設定ファイルでのキー。

            Returns:
                key の値。

            Raises:
                ValueError: key が書かれていない場合。
            """
            if key not in raw_data:
                raise ValueError(f"no {key}")
            return raw_data[key]

        config = cls(
            width=convert("WIDTH", int, required("WIDTH")),
            height=convert("HEIGHT", int, required("HEIGHT")),
            entry=convert("ENTRY", parse_coordinate, required("ENTRY")),
            exit=convert("EXIT", parse_coordinate, required("EXIT")),
            perfect=convert("PERFECT", strtobool, required("PERFECT")),
            # パスはPathオブジェクトにすると扱いやすい
            # expanduser() は "~" をホームディレクトリに展開する
            # (相対パスはそのまま。実行時のカレントディレクトリが基準になる)
            output_file=Path(required("OUTPUT_FILE")).expanduser(),
        )
        # 下限 (負の値など) は mazegen が確かめるので、ここでは上限だけを見る
        for key, size in (("WIDTH", config.width), ("HEIGHT", config.height)):
            if size > MAX_SIZE:
                raise ValueError(
                    f"{key}: {size} is too large (max {MAX_SIZE})"
                )
        # replace() の引数は mypy がフィールドの型と照らし合わせてくれる
        # replace()でなくcls(**kwargs) で書くとmypyの型チェックが効かなくなるので注意
        if "SEED" in raw_data:
            config = replace(
                config, seed=convert("SEED", int, raw_data["SEED"])
            )
        if "ALGORITHM" in raw_data:
            config = replace(config, algorithm=raw_data["ALGORITHM"])
        # 「迷路生成が終わってからdisplayを読んだ際エラーが生じる」はやや好ましくない
        # これだけ事前にバリデーションする
        if "DISPLAY" in raw_data:
            if raw_data["DISPLAY"] not in display.BACKENDS:
                raise ValueError(
                    f"invalid DISPLAY {raw_data['DISPLAY']!r}"
                    f" (choose from {', '.join(display.BACKENDS)})"
                )
            config = replace(config, display=raw_data["DISPLAY"])
        return config


# Configクラスで前提しているデータの名前の集合を作っている
# これに入っていないものは上のparse_config()内でunknown_keysとしている
# デバッグ用のものであり本筋には関連しない、そういう意味では削ってもいい
KNOWN_KEYS: frozenset[str] = frozenset(
    field.name.upper() for field in fields(Config)
)


def main() -> None:
    """設定を読み、迷路を生成してファイルに書き込み、表示する。

    設定ファイルのパスをコマンドライン引数で1つ受け取る。
    エラーが起きたら、メッセージを表示して終了する。

    Raises:
        SystemExit: 引数の数が違う場合や、エラーが起きた場合。
    """
    _setup_logging()
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 a_maze_ing.py <config_file_path>")
    # expanduser() 自体が失敗しうるので、except で使う値は try の外で確定させる
    raw_path: str = sys.argv[1]
    try:
        config_path: Path = Path(raw_path).expanduser()
        var_dict: dict[str, str] = parse_config(config_path)
    except Exception as e:
        # ファイルがない・読めない・書式誤りなどすべてのエラーを一括処理
        # 原因は e のメッセージに任せ、どのファイルの問題かだけを添える
        sys.exit(f"{raw_path}: {e}")

    try:
        config = Config.from_dict(var_dict)
    except Exception as e:
        sys.exit(str(e))
    logger.debug("config: %s", config)

    try:
        maze_generator = mazegen.MazeGenerator(
            config.width, config.height,
            config.entry, config.exit,
            config.perfect, config.algorithm, config.seed
        )
        maze = maze_generator.generate_maze()
        output_path: Path = config.output_file
        write_maze_file(output_path, maze)

        # displayモジュールでは迷路の再生成も行う
        # あちらに生成用のすべてのパラメータを渡すのは煩雑
        # よってregenerate()という関数として渡してやる
        def regenerate() -> mazegen.Maze:
            """新しい迷路を生成し、OUTPUT_FILE を上書きする。

            Returns:
                新しく生成した迷路。
            """
            new_maze = maze_generator.generate_maze()
            # maze_file.pyの出力関数に投げる
            write_maze_file(output_path, new_maze)
            return new_maze

        display.run(maze, regenerate=regenerate, backend=config.display)
    except Exception as e:

        sys.exit(str(e))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # KeyboardInterruptにおいては終了コード130で終えるのが慣例らしい
        # Ctrl+C などの割り込みシグナル（SIGINT）を受け取ったことに対応
        # ユーザーの操作により中断・終了したことを意味する
        # 実行直後に「echo $?」を実行すると終了コードを参照できる
        sys.exit(130)
