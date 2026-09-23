*This project has been created as part of the 42 curriculum by harnakam.*

# ft_printf

## Description

`ft_printf` は、C 標準ライブラリの `printf` の基本機能を再実装するプロジェクトです。
可変長引数を順番に読み取り、フォーマット文字列に含まれる変換指定子に応じて値を標準出力へ表示します。

この実装は、次の変換指定子に対応しています。

| 指定子 | 内容 | 受け取る型 |
| --- | --- | --- |
| `%c` | 1 文字 | `int` |
| `%s` | 文字列 | `char *` |
| `%p` | ポインタアドレス（16 進数） | `void *` |
| `%d` / `%i` | 符号付き 10 進整数 | `int` |
| `%u` | 符号なし 10 進整数 | `unsigned int` |
| `%x` | 小文字の符号なし 16 進整数 | `unsigned int` |
| `%X` | 大文字の符号なし 16 進整数 | `unsigned int` |
| `%%` | `%` 記号 | 引数なし |

また、学習用の独自指定子 `%a` は `my awsome 42` を出力します。
未対応の指定子は、`%` とその文字をそのまま出力します。

通常は出力した文字数を返し、`write` に失敗した場合や `format` が `NULL` の場合は `-1` を返します。

## Instructions

### ビルド

```sh
make
```

実行すると、静的ライブラリ `libftprintf.a` が生成されます。

### 使用例

```c
#include "ft_printf.h"

int	main(void)
{
	int	count;

	count = ft_printf("name: %s, score: %d, hex: %X\n", "42", 100, 100);
	ft_printf("printed: %d characters\n", count);
	return (0);
}
```

次のようにコンパイルします。

```sh
cc -Wall -Wextra -Werror main.c -L. -lftprintf -o example
./example
```

### Makefile のルール

| コマンド | 動作 |
| --- | --- |
| `make` / `make all` | `libftprintf.a` を作成する |
| `make clean` | オブジェクトファイルを削除する |
| `make fclean` | オブジェクトファイルとライブラリを削除する |
| `make re` | すべて削除してから再ビルドする |

## Algorithm

### 全体の流れ

1. `ft_printf` が `va_start` で可変長引数の読み取りを開始する。
2. フォーマット文字列を先頭から 1 文字ずつ調べる。
3. 通常の文字なら `ft_print_char` でそのまま出力する。
4. `%` を見つけたら次の文字を変換指定子として `ft_print_format` に渡す。
5. `va_arg` で指定子に対応する型の値を取り出し、専用関数で出力する。
6. 各関数が返した文字数を合計する。
7. 最後に `va_end` を呼び、合計文字数を返す。

フォーマット文字列の末尾が単独の `%` だった場合、その `%` は出力せず処理を終了します。

### 整数の出力

数値は再帰を使って上位桁から出力します。例えば `123` の場合は、次のように処理します。

```text
123
├── 12
│   ├── 1  を出力
│   └── 2  を出力
└── 3  を出力
```

`ft_print_nbr` は負数のとき最初に `-` を出力します。`INT_MIN` も安全に扱えるよう、計算前に `long` へ変換しています。

### 基数変換

`ft_putbase` は、数値、基数字列、基数を受け取る共通関数です。

```c
ft_putbase(n, "0123456789abcdef", 16);
```

数値を基数で割った商を再帰処理し、余りを基数字列の添字として使います。これにより、同じ処理を 16 進数とポインタ表示の両方で再利用しています。

### エラー処理

最小の出力関数 `ft_print_char` が `write` の戻り値を確認します。失敗時の `-1` は呼び出し元へ順番に伝播されるため、途中までの文字数を正常終了として返しません。

### 再実装する順番

初めから `ft_printf` 全体を書くより、次の順番で小さな機能を完成させると理解しやすくなります。

1. `ft_print_char` で 1 文字を出力する。
2. `ft_print_str` で文字列を出力する。
3. `ft_print_nbr` と `ft_print_unsigned` で 10 進数を出力する。
4. `ft_putbase` で任意の基数による出力を作る。
5. `ft_print_hex` と `ft_print_ptr` を作る。
6. `ft_print_format` で指定子と出力関数を対応させる。
7. `ft_printf` で文字列走査、文字数集計、エラー処理をまとめる。

各段階で `0`、最大値、最小値、`NULL` などの境界値を確認してから次へ進むと、問題の切り分けが容易になります。

## Data structure

このプロジェクトでは、複雑な構造体や動的メモリ確保を使用しません。中心となるデータは次の 3 つです。

- `const char *format`: 出力内容と変換指定子を保持するフォーマット文字列
- `va_list args`: `...` で渡された可変長引数を順番に読むための型
- `int total`: 正常に出力できた文字数の合計

### ファイル構成

| ファイル | 役割 |
| --- | --- |
| `ft_printf.c` | フォーマット解析、引数の振り分け、文字数集計 |
| `ft_print_char.c` | 1 文字の出力 |
| `ft_print_str.c` | 文字列の出力と `NULL` の処理 |
| `ft_print_nbr.c` | 符号付き 10 進整数の出力 |
| `ft_print_unsigned.c` | 符号なし 10 進整数の出力 |
| `ft_putbase.c` | 共通の基数変換と出力 |
| `ft_print_hex.c` | 小文字・大文字の 16 進数出力 |
| `ft_print_ptr.c` | ポインタの出力 |
| `ft_printf.h` | 関数宣言と必要なヘッダー |
| `Makefile` | 静的ライブラリのビルド規則 |

## Resources

- `man 3 printf`
- `man 3 stdarg`
- `man 2 write`
- [cppreference: Variadic arguments](https://en.cppreference.com/w/c/variadic)
- [cppreference: printf family](https://en.cppreference.com/w/c/io/fprintf)

## AI usage

AI は README の構成整理、日本語表現の改善、および実装内容と説明の整合性確認に使用しました。
