import random

# class Player:
#     players = []

#     def __init__(self, name: str) -> None:
#         self.name = name
#         Player.players.append(self)


#     def __repr__(self) -> str:
#         return self.name


def main() -> None:
    print("=== Game Data Alchemist ===")
    names = [
        "Alice",
        "bob",
        "Charlie",
        "dylan",
        "Emma",
        "Gregory",
        "john",
        "kevin",
        "Liam",
    ]
    display = [name.capitalize() for name in names]
    # for name in names:
    #     display.append(name.capitalize())
    #     Player(name)

    temp = display

    print()
    print(f"Initial list of players: {names}")

    print()
    print(f"New list with all names capitalized: {display}")

    display = [name for name in names if name == name.capitalize()]
    # for name in names:
    #     if name == name.capitalize():
    #         display.append(name)
    print()
    print(f"New list of capitalized names only: {display}")

    scores = {
        name: random.randint(0, 1000)
        for name in temp
        }
    # for name in temp:
    #     scores[name] = random.randint(0, 1000)
    print()
    print(f"Score dict: {scores}")

    # result = 0
    # for name in names:
    #     result += scores[name]
    # average = result / len(names)
    average = sum(scores.values()) / len(scores)

    print(f"Score average is {average:.2f}")

    high_scores = {name: scores[name] for name in scores if scores[name] > average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
