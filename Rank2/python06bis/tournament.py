from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)

from ex4 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    InvalidStrategyError,
)


def tournament(
    opponents: list[tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            creature1, strategy1 = creatures[i]
            creature2, strategy2 = creatures[j]

            print("\n* Battle *")
            print(creature1.describe())
            print(" vs.")
            print(creature2.describe())
            print(" now fight!")

            try:
                strategy1.act(creature1)
                strategy2.act(creature2)
            except InvalidStrategyError as error:
                print(f"Battle error, aborting tournament: {error}")
                return


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    print(" [(Flameling+Normal), (Shiftling+Aggressive)]")

    tournament([
        (flame, normal),
        (transform, aggressive)
    ])

    print("\nTournament 1 (error)")
    print(" [(Shiftling+Aggressive), (Flameling+Aggressive)]")

    tournament([
        (transform, aggressive),
        (flame, aggressive)
    ])


if __name__ == "__main__":
    main()
