def read_input(filename):
    with open(filename, "r") as f:
        return [line.split(",") for line in f.readlines()]


def print_solutions(part1=None, part2=None):
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    return None
