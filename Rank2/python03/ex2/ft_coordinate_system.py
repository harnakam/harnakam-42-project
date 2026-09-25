# $> python3 ft_coordinate_system.py
# === Game Coordinate System ===
# Get a first set of coordinates
# Enter new coordinates as floats in format 'x,y,z': hello world
# Invalid syntax
# Enter new coordinates as floats in format 'x,y,z': 1.0 , 2.5, 3.0
# Got a first tuple: (1.0, 2.5, 3.0)
# It includes: X=1.0, Y=2.5, Z=3.0
# Distance to center: 4.0311
# Get a second set of coordinates
# Enter new coordinates as floats in format 'x,y,z': 4,abc,5
# Error on parameter 'abc': could not convert string to float: 'abc'
# Enter new coordinates as floats in format 'x,y,z': 4,5,6
# Distance between the 2 sets of coordinates: 4.9

import math

coord = tuple[float, float, float]


def get_coord() -> coord:
    while True:
        user_input = input("Enter new coordinates as floats in format 'x,y,z': ")
        try:
            parts = user_input.split(",")
            if len(parts) != 3:
                print("Invalid syntax")
                continue
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())

            break
        except Exception as Error:
            print(Error)
    return (x, y, z)


def distance(coord1: coord, coord2: coord) -> float:
    return math.sqrt(
        (coord2[0] - coord1[0]) ** 2
        + (coord2[1] - coord1[1]) ** 2
        + (coord2[2] - coord1[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    initial_coord = (0, 0, 0)
    coord1 = get_coord()
    print(f"Got a first tuple: {coord1}")
    print("It includes: " f"X={coord1[0]}, " f"Y={coord1[1]}, " f"Z={coord1[2]}")
    print(f"Distance to center: {distance(coord1, initial_coord):.4f}")
    print("Get a second set of coordinates")
    coord2 = get_coord()
    print(f"Distance between the 2 sets of coordinates: {distance(coord1, coord2):.4f}")


if __name__ == "__main__":
    main()
