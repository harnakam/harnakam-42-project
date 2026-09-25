class Player:
    players = []
    all_achievements = set()

    def __init__(self, name: str) -> None:
        self.name = name
        self.achievements = set()
        Player.players.append(self)

    def __repr__(self) -> str:
        return self.name.lower()

    def add_achievements(self, achievement: str) -> None:
        self.achievements.add(achievement)
        Player.all_achievements.add(achievement)

    def show_achievements(self) -> set:
        return self.achievements

    @staticmethod
    def show_all_achievements() -> set:
        return Player.all_achievements

    # from __future__ import annotations
    @staticmethod
    def common_achievements(*other: "Player") -> set:
        if not other:
            return set()
        result = other[0].achievements.copy()
        for player in other[1:]:
            result = result.intersection(player.achievements)
        return result

    def unique_achievements(self, *other: "Player") -> set:
        result = self.achievements.copy()

        for player in other:
            result = result.difference(player.achievements)
        return result

    def missing_achievements(self) -> set:
        return Player.all_achievements.difference(self.achievements)

    @staticmethod
    def all_distinct(*other: "Player") -> set:
        result = set()
        for player in other:
            result = result.union(player.achievements)
        return result


def main() -> None:
    print("=== Achievement Tracker System ===")
    print()
    alice = Player("Alice")
    bob = Player("Bob")
    steve = Player("Steve")
    alex = Player("Alex")

    # show all player
    # print("=== Player list ===")
    # print(Player.players)
    # add player achievements
    alice.add_achievements("Taking Inventory")
    alice.add_achievements("Getting Wood")
    bob.add_achievements("Taking Inventory")
    bob.add_achievements("Getting Wood")
    bob.add_achievements("Benchmaking")
    bob.add_achievements("Time to Mine!")
    steve.add_achievements("Taking Inventory")
    steve.add_achievements("Getting Wood")
    steve.add_achievements("DIAMONDS!")
    steve.add_achievements("Diamonds to you!")
    steve.add_achievements("Acquire Hardware")
    steve.add_achievements("Time to Strike!")
    alex.add_achievements("Taking Inventory")
    alex.add_achievements("Getting Wood")
    alex.add_achievements("DIAMONDS!")
    alex.add_achievements("Super Fuel")
    alex.add_achievements("Time to Farm!")
    alex.add_achievements("Have a Shearful Day")
    alex.add_achievements("Rainbow Collection")
    alex.add_achievements("Sound of Music")

    # show all achievements
    # print()
    # print("=== ALL ACHIEVEMENTS ===")
    # print(Player.all_achievements)

    # show player achievements
    print()
    print("=== Player Achievements ===")
    print(f"Player {alice.name}: {alice.show_achievements()}")
    print(f"Player {bob.name}: {bob.show_achievements()}")
    print(f"Player {steve.name}: {steve.show_achievements()}")
    print(f"Player {alex.name}: {alex.show_achievements()}")

    # All distinct
    print()
    print("=== All distinct ===")

    print(
        "All distinct achievements: " f"{Player.all_distinct(alice, bob, steve, alex)}"
    )

    # Common Achievements
    print()
    print("=== Common Achievements ===")
    print(
        "Common achievements: " f"{Player.common_achievements(alice, bob, steve, alex)}"
    )

    # Only Player has:
    print()
    print("=== Only has ===")
    print(f"Only {alice.name} has: " f"{alice.unique_achievements(bob, steve, alex)}")
    print(f"Only {bob.name} has: " f"{bob.unique_achievements(alice, steve, alex)}")
    print(f"Only {steve.name} has: " f"{steve.unique_achievements(alice, bob, alex)}")
    print(f"Only {alex.name} has: " f"{alex.unique_achievements(alice, bob, steve)}")

    # Player is missing
    print()
    print("=== Missing Achievements ===")
    print(f"{alice.name} is missing: " f"{alice.missing_achievements()}")
    print(f"{bob.name} is missing: " f"{bob.missing_achievements()}")
    print(f"{steve.name} is missing: " f"{steve.missing_achievements()}")
    print(f"{alex.name} is missing: " f"{alex.missing_achievements()}")


if __name__ == "__main__":
    main()
