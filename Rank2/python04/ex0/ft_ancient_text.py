import sys
from typing import IO


def validate_args() -> bool:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return False
    return True


def title() -> None:
    print("=== Cyber Archives Recovery ===")


class Files:
    def __init__(self, filename: str, scope: str = "r") -> None:
        self.filename = filename
        self.scope = scope
        self.file: IO[str] | None = None
        self.content: str = ""
        self.loaded: bool = False

    def __repr__(self) -> str:
        return f"Files(filename={self.filename!r}, scope={self.scope!r})"

    def __str__(self) -> str:
        if self.file is None:
            raise ValueError("File is not open")
        if not self.loaded:
            self.readf()
        return self.content

    def openf(self) -> None:
        self.file = open(self.filename, self.scope)
        self.content = ""
        self.loaded = False

    def readf(self) -> str:
        if self.file is None:
            raise ValueError("File is not open")
        self.content = self.file.read()
        self.loaded = True
        return self.content

    # def writef(self, content: str) -> None:
    #     if self.file is None:
    #         raise ValueError("File is not open")
    #     self.file.write(content)
    #     self.content = content

    def closef(self) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None


def process(filename: str) -> None:
    title()
    print(f"Accessing file '{filename}'")
    f = Files(filename)
    try:
        f.openf()
        # print(f"{f.openf}")
        # print(f"{f.openf()}")
        print("---" + "\n\n" + f"{f}")
    finally:
        f.closef()
    print("\n" + "---")
    print(f"File '{filename}' closed.")


def main() -> None:
    if not validate_args():
        return
    try:
        process(sys.argv[1])
    except UnicodeError as Error:
        print(f"\nText decoding error: {Error}")
    except OSError as Error:
        print(f"\nError opening file '{sys.argv[1]}': {Error}")
    except ValueError as Error:
        print(f"Invalid value: {Error}")
    except KeyboardInterrupt as Error:
        print(f"{Error}")
    except BaseException as Error:
        print(f"Unexpected error: {Error}")


if __name__ == "__main__":
    main()
