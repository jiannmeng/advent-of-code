def recursive_fuel(mass):
    fuel = max(mass // 3 - 2, 0)
    return [fuel] + recursive_fuel(fuel) if fuel else [0]


# PART 1.
with open("inputs/input_01.txt") as file:
    masses = [int(x) for x in file.readlines()]
fuels = [recursive_fuel(m) for m in masses]
part1 = sum(f[0] for f in fuels)

# PART 2.
part2 = sum(sum(f) for f in fuels)


if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
