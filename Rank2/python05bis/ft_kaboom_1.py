def main() -> None:
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")

    from alchemy.grimoire.dark_spellbook import dark_spell_record

    print(dark_spell_record("Dark Magic", "bats and frogs"))


if __name__ == "__main__":
    try:
        main()
    except BaseException as Error:
        print(f"Error: {Error}")
