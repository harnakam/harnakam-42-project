*This project has been created as part of the 42 curriculum by harnakam.*

# get_next_line

## Description

`get_next_line` は、ファイルディスクリプタからテキストを1行ずつ読み取るC言語の関数です。
同じファイルディスクリプタに対して繰り返し呼び出すと、読み取り位置を保ちながら次の1行を返します。

この課題の主な目的は、次の仕組みを理解することです。

- `read(2)` を使ったファイルディスクリプタからの入力
- 関数呼び出し後も値を保持する静的変数
- 必要なデータだけを残す動的メモリ管理
- 読み取り単位と行単位の違いを吸収するバッファ処理

関数のプロトタイプは次のとおりです。

```c
char *get_next_line(int fd);
```

### 戻り値

- 読み取りに成功した場合: 読み取った1行を格納した文字列
- ファイル終端に達した場合: `NULL`
- 読み取りエラーまたはメモリ確保失敗の場合: `NULL`

返される文字列には、行末に存在する場合は改行文字 `\n` が含まれます。ファイルの最終行が `\n` で終わっていない場合は、その最終行をそのまま返します。返された文字列は呼び出し側が `free` する必要があります。

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `get_next_line.c` | 読み取り、1行の切り出し、未使用部分の保存 |
| `get_next_line_utils.c` | 文字列長、文字検索、文字列結合の補助関数 |
| `get_next_line.h` | 関数プロトタイプ、必要なヘッダ、`BUFFER_SIZE` の既定値 |

## Instructions

### コンパイル

このリポジトリには実行用の `main` 関数は含まれていません。任意のテスト用 `main.c` と一緒にコンパイルしてください。

```sh
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
  get_next_line.c get_next_line_utils.c main.c -o gnl_demo
```

`BUFFER_SIZE` は、1回の `read` で読み込む最大バイト数です。コンパイル時に指定しない場合は、ヘッダで定義された既定値 `42` が使われます。

```sh
cc -Wall -Wextra -Werror \
  get_next_line.c get_next_line_utils.c main.c -o gnl_demo
```

### 使用例

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    int     fd;
    char    *line;

    if (argc != 2)
        return (1);
    fd = open(argv[1], O_RDONLY);
    if (fd < 0)
        return (1);
    line = get_next_line(fd);
    while (line != NULL)
    {
        printf("%s", line);
        free(line);
        line = get_next_line(fd);
    }
    close(fd);
    return (0);
}
```

実行例:

```sh
./gnl_demo sample.txt
```

標準入力を読む場合は、ファイルディスクリプタに `STDIN_FILENO` を渡します。

```c
line = get_next_line(STDIN_FILENO);
```

## アルゴリズム

### 基本方針

この実装では、`get_next_line` 内の静的変数 `stash` に「読み取ったが、まだ返していない文字列」を保存します。`read` が返すデータは必ずしも1行単位ではないため、読み取り結果をいったん `stash` に蓄積し、改行位置を基準に1行と残りへ分割します。

処理は次の順序で進みます。

1. `read_to_stash` が、`stash` に改行が現れるかEOFへ到達するまで読み取る
2. `extract_line` が、`stash` の先頭から最初の `\n` までを新しい文字列として確保する
3. `keep_rest` が、返した行より後ろの文字列を次回呼び出し用に保存する
4. 呼び出し側へ1行を返す

たとえば、`stash` が次の状態になった場合:

```text
first line\nsecond
```

今回返す文字列は `first line\n`、次回へ残す文字列は `second` です。

### この方式を選んだ理由

`BUFFER_SIZE` と実際の行の長さは一致しません。1行が複数回の `read` に分かれる場合も、1回の `read` に複数行が含まれる場合もあります。静的変数へ未処理部分を保存する方式なら、どちらの場合にも同じ処理で対応できます。

また、改行を見つけた時点で読み取りを止めるため、毎回ファイル全体を読み込む必要がありません。課題要件である「1回の呼び出しで必要以上に読み取らないこと」に沿った構成です。

### 各関数の役割

- `get_next_line`: 引数の検証と処理全体の制御を行う
- `read_to_stash`: `read` の結果を `stash` へ連結する
- `extract_line`: 返却する1行を確保してコピーする
- `keep_rest`: 返却後に残った文字列を次回用に確保する
- `ft_strjoin_free`: 文字列を連結し、古い `stash` を解放する
- `ft_strlen` / `ft_strchr`: 必要最小限の文字列操作を提供する

### メモリ管理

`stash` は結合や分割のたびに新しい領域へ置き換え、不要になった古い領域を解放します。EOF、読み取りエラー、または処理対象がなくなった場合も、保持中の領域を解放して `NULL` に戻します。

呼び出し側へ返した `line` の所有権は呼び出し側へ移るため、使用後に必ず `free(line)` を実行してください。

## 制約と注意点

- 使用する外部関数は `read`、`malloc`、`free` です。
- `libft` および `lseek` は使用していません。
- `BUFFER_SIZE` が `0` 以下の場合は `NULL` を返します。
- バイナリファイルの読み取りは未定義動作です。
- 読み取り途中で対象ファイルが変更された場合の動作は未定義です。
- この必須パートの実装は静的な `stash` を1つだけ使うため、複数のファイルディスクリプタを交互に読み取る用途には対応していません。


## Resources

= chat.openai.com
- 42 Get Next Line subject Version 14.2 — 課題仕様、禁止事項、README要件の確認

### AIの利用について

AIは、このREADMEの構成作成、日本語での説明整理、既存コードと課題PDFの要件照合に使用しました。特に、アルゴリズムの流れ、各関数の役割、コンパイル例、テスト観点を文書化するために利用しています。実装コードの生成や変更には使用していません。
