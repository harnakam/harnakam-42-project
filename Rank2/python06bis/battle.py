from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")

    base = factory.create_base()
    evolved = factory.create_evolved()

    print(base.describe())
    print(base.attack())

    print(evolved.describe())
    print(evolved.attack())


def test_battle(
    factory1: CreatureFactory,
    factory2: CreatureFactory
) -> None:
    print("Testing battle")

    creature1 = factory1.create_base()
    creature2 = factory2.create_base()

    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(" fight!")

    print(creature1.attack())
    print(creature2.attack())


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()

    test_factory(flame)
    print()

    test_factory(transform)
    print()

    test_battle(flame, transform)


if __name__ == "__main__":
    main()
