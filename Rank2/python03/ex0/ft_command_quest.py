import sys


def main() -> None:
    print("=== Command Quest ===")
    FileName = sys.argv[0]
    print(f"Program name: {FileName.split("/")[-1]}")
    if len(sys.argv[1:]) > 0:
        print(f"Arguments received: {len(sys.argv[1:])}")
        i = 1
        for arg in sys.argv[1:]:
            print(f"Argument {i}: {arg}")
            i += 1
    else:
        print("No arguments provided!")
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
