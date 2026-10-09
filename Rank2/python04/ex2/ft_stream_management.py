import sys
from typing import IO


def validate_args() -> bool:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return False
    return True


def title() -> None:
    print("=== Cyber Archives Recovery & Preservation ===")


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

    def writef(self, content: str) -> None:
        if self.file is None:
            raise ValueError("File is not open")
        self.file.write(content)
        self.content = content

    def closef(self) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None


def process(filename: str) -> None:
    title()

    """===ACCESS DATA==="""

    print(f"Accessing file '{filename}'")
    f = Files(filename)

    try:
        f.openf()
        data = str(f)
        print("---\n")
        print(data, end="")
    finally:
        f.closef()

    print("\n---")
    print(f"File '{filename}' closed.\n")

    """===TRANSFORM DATA==="""

    print("Transform data:")
    print("---\n")

    newdata: str = ""
    lines = data.splitlines()

    for line in lines:
        line = line + "#"
        newdata = newdata + line + "\n"
        print(line)

    print("\n---")

    """===SAVE DATA==="""

    print("Enter new file name (or empty): ", end="")
    sys.stdout.flush()

    newfilename = sys.stdin.readline().rstrip("\n")

    if not newfilename:
        print("Not saving data.")
        return

    print(f"Saving data to '{newfilename}'")

    f = Files(newfilename, "w")

    try:
        try:
            f.openf()
            f.writef(newdata)
        finally:
            f.closef()

    except OSError as error:
        sys.stderr.write(f"[STDERR] Error opening file '{newfilename}': {error}\n")
        print("Data not saved.")
        return

    print(f"Data saved in file '{newfilename}'.")


def main() -> None:
    if not validate_args():
        return

    try:
        process(sys.argv[1])

    except UnicodeError as error:
        sys.stderr.write(f"[STDERR] Text decoding error: {error}\n")

    except OSError as error:
        sys.stderr.write(f"[STDERR] Error opening file '{sys.argv[1]}': {error}\n")

    except ValueError as error:
        sys.stderr.write(f"[STDERR] Invalid value: {error}\n")

    except KeyboardInterrupt:
        sys.stderr.write("[STDERR] Operation interrupted.\n")

    except BaseException as error:
        sys.stderr.write(f"[STDERR] Unexpected error: {error}\n")


if __name__ == "__main__":
    main()
