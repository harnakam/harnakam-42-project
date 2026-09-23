#!/usr/bin/env python3
class Plant:
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self.name = name
        self._height = 0.0
        self._age_days = 0
        self.set_height(height)
        self.set_age(age_days)

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            return False
        self._height = height
        return True

    def set_age(self, age_days: int) -> bool:
        if age_days < 0:
            print(f"{self.name}: Error, age can't be negative")
            return False
        self._age_days = age_days
        return True

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age_days

    def show(self) -> str:
        return f"{self.name}: {self._height:.1f}cm, {self._age_days} days old"


def main() -> None:
    plant = Plant("Rose", 15.0, 10)
    print("=== Garden Security System ===")
    print(f"Plant created: {plant.show()}")
    if plant.set_height(25):
        print("Height updated: 25cm")
    if plant.set_age(30):
        print("Age updated: 30 days")
    if not plant.set_height(-2):
        print("Height update rejected")
    if not plant.set_age(-1):
        print("Age update rejected")
    print(f"Current state: {plant.show()}")


if __name__ == "__main__":
    main()
