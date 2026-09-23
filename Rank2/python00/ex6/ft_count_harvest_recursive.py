def ft_count_harvest_recursive() -> None:
    days = int(input("Days until harvest: "))

    def count_day(day: int) -> None:
        if day > days:
            return
        print(f"Day {day}")
        count_day(day + 1)

    count_day(1)
    print("Harvest time!")
