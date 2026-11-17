import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")

    result = alchemy.grimoire.light_spell_record(
        "Fantasy", "Earth, wind and fire"
    )

    print(f"Testing record light spell: {result}")


# def example() -> None:
#     print()
#     print("=== Kaboom 0 TEST ===")
#     result = alchemy.grimoire.light_spell_record(
#         "TEST1", "Earth, wind, fire"
#     )
#     print(f"TEST1: {result}")
#     result = alchemy.grimoire.light_spell_record("TEST2", "Earth")
#     print(f"TEST2: {result}")
#     result = alchemy.grimoire.light_spell_record("TEST3", "NOTHING")
#     print(f"TEST3: {result}")
#     result = alchemy.grimoire.light_spell_record(
#         "TEST4", "Earth, Nothing"
#     )
#     print(f"TEST4: {result}")


if __name__ == "__main__":
    try:
        main()
        # example()
    except BaseException as Error:
        print(f"ERROR: {Error}")
