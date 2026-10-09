def secure_archive(
    filename: str, operation: str = "read", content: str = ""
) -> tuple[bool, str]:
    try:
        if operation == "read":
            with open(filename, "r") as file:
                data = file.read()
            return (True, data)
        elif operation == "write":
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
        # elif operation == "append":
        #     with open(filename, "a") as file:
        #         file.write(content)
    except (OSError, ValueError) as error:
        return (False, str(error))
    return (False, "Invalid operation")


def main() -> None:
    print("=== Cyber Archives Security ===")
    print()

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)

    # Success ..? True / False
    if result[0]:
        print("Using 'secure_archive' to write previous" " content to a new file:")
        print(secure_archive("new_fragment.txt", "write", result[1]))


if __name__ == "__main__":
    try:
        main()
    except BaseException as Error:
        print(f"Unexpected error: {Error}")
