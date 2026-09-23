#!/usr/bin/env python3
class Plant:
    def __init__(
        self,
        name: str,
        height: float,
        age_days: int,
        daily_growth: float,
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.daily_growth = daily_growth

    def grow(self) -> None:
        self.height = round(self.height + self.daily_growth, 1)

    def age(self) -> None:
        self.age_days += 1

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.age_days} days old")


def main() -> None:
    rose = Plant("Rose", 25.0, 30, 0.8)
    start_height = rose.height
    print("=== Garden Plant Growth ===")
    rose.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()
    growth = round(rose.height - start_height, 1)
    print(f"Growth this week: {growth:.1f}cm")


if __name__ == "__main__":
    main()
