import aocd
import math


def parse_movements(data: list[str]) -> list[tuple[int, int]]:
    movements = []
    for line in data:
        direction, distance = line.split()
        distance = int(distance)
        if direction == "forward":
            movements.append((distance, 0))
        elif direction == "down":
            movements.append((0, distance))
        elif direction == "up":
            movements.append((0, -distance))
        else:
            raise ValueError("Invalid movement.")
    return movements


def move(movements: list[tuple[int, int]]):
    x = sum(m[0] for m in movements)
    y = sum(m[1] for m in movements)
    return x, y


def test():
    data = """forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2""".splitlines()
    movements = parse_movements(data)
    final_position = move(movements)
    assert math.prod(final_position) == 150
    print("👍 Test passed!")


def main():
    data = aocd.lines  # type:ignore
    movements = parse_movements(data)
    final_position = move(movements)
    aocd.submit(math.prod(final_position), part="a")


test()
main()
