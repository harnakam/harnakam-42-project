import sys


class Inventory:
    def __init__(self) -> None:
        self.item_info = {}

    # def get_position(self, target: str) -> int:
    #     for position, item in enumerate(self.item_info):
    #         if item == target:
    #             return position
    #     return -1

    def add_item(self, name: str, count: int) -> None:
        if name in self.item_info:
            print(f"Redundant item '{name}' - discarding")
        else:
            self.item_info[name] = count

    def max_item(self) -> tuple[str, int]:
        names = list(self.item_info.keys())
        max_name = names[0]
        max_count = self.item_info[max_name]
        for name in names[1:]:
            count = self.item_info[name]
            if count > max_count:
                max_count = count
                max_name = name
        return (max_name, max_count)

    def min_item(self) -> tuple[str, int]:
        min_count = -1
        min_name = ""
        for name in self.item_info.keys():
            count = self.item_info[name]
            if min_count == -1 or count < min_count:
                min_count = count
                min_name = name
        return (min_name, min_count)

    def item_list(self) -> list:
        return list(self.item_info.keys())

    def total_quantity(self) -> int:
        return sum(self.item_info.values())


def main() -> None:
    print("=== Inventory System Analysis ===")
    player = Inventory()
    # add item
    for argument in sys.argv[1:]:
        item = argument.split(":")
        if len(item) != 2:
            print(f"Error - invalid parameter '{argument}'")
            continue
        try:
            player.add_item(item[0], int(item[1]))
        except ValueError as e:
            print(f"Quantity error for '{item[0]}': {e}")

    if len(player.item_info) == 0:
        print("Are you trying to break it ..?")
        return
    print(f"Got inventory: {player.item_info}")
    print(f"Item list: {player.item_list()}")
    print(
        "Total quantity of the "
        f"{len(player.item_info)} "
        f"items: {player.total_quantity()}"
    )

    for name in player.item_info.keys():
        count = player.item_info[name]
        try:
            percentage = count / player.total_quantity() * 100
            print(f"Item {name} represents {percentage:.1f}%")
        except ZeroDivisionError as e:
            print(e)
    max_name, max_count = player.max_item()
    print(f"Item most abundant: {max_name} " f"with quantity {max_count}")
    print(
        f"Item least abundant: {player.min_item()[0]} "
        f"with quantity {player.min_item()[1]}"
    )
    player.item_info.update({"magic_item": 1})
    print(f"Updated inventory: {player.item_info}")


if __name__ == "__main__":
    main()
