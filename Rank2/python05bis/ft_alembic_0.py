import elements

# import inspect


def main() -> None:
    print("=== Alembic 0 ===")
    print("Using: 'import ...' structure to access elements.py")
    print(f"Testing create_fire: {elements.create_fire()}")

    # [DEBUG]
    # print("\n=== DEBUG ===")

    # print("Function: elements.create_fire")
    # path = inspect.getfile(elements.create_fire)
    # print("Defined in: " + "/".join(path.split("/")[-2:]))

    # print("\nFunction: elements.create_water")
    # path = inspect.getfile(elements.create_water)
    # print("Defined in: " + "/".join(path.split("/")[-2:]))


if __name__ == "__main__":
    main()
