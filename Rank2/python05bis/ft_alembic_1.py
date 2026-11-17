import alchemy

# import inspect


def main() -> None:
    print("=== Alembic 1 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")

    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    try:
        # The subject requires this missing attribute to raise AttributeError.
        earth = alchemy.create_earth()  # type: ignore[attr-defined]
        print(f"Testing the hidden create_earth: {earth}")
    except AttributeError as Error:
        print(f"AttributeError: {Error}")

    # [DEBUG]
    # print("\n=== DEBUG ===")

    # # create_air
    # print("Function: alchemy.create_air")
    # path = inspect.getfile(alchemy.create_air)
    # print("Defined in: " + "/".join(path.split("/")[-2:]))

    # # create_earth
    # print("\nFunction: alchemy.create_earth")
    # try:
    #     path = inspect.getfile(
    #         alchemy.create_earth  # type: ignore[attr-defined]
    #     )
    #     print("Defined in: " + "/".join(path.split("/")[-2:]))
    # except AttributeError:
    #     print("Not accessible through the alchemy package interface")
    #     print("Did you mean: 'alchemy.elements.create_earth'?")


if __name__ == "__main__":
    main()
