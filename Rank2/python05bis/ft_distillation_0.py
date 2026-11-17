from alchemy.potions import healing_potion, strength_potion

# import inspect


def main() -> None:
    print("=== Distillation 0 ===")
    print("Direct access to alchemy/potions.py")
    print(f"Testing strength_potion: {strength_potion()}")
    print(f"Testing healing_potion: {healing_potion()}")

    # [DEBUG]
    # print("\n=== DEBUG ===")
    #
    # """strength_potion"""
    # print("Function: alchemy.potions.strength_potion")
    # path = inspect.getfile(strength_potion)
    # print("Defined in: " + "/".join(path.split("/")[-2:]))
    #
    # """healing_potion"""
    # print()
    # print("Function: alchemy.potions.healing_potion")
    # path = inspect.getfile(healing_potion)
    # print("Defined in: " + "/".join(path.split("/")[-2:]))


if __name__ == "__main__":
    main()
