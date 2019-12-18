import util


def recursive_fuel(mass):
    fuel = max(mass // 3 - 2, 0)
    return [fuel] + recursive_fuel(fuel) if fuel else [0]


# Test cases.
part1_tests = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
part2_tests = [(14, 2), (1969, 966), (100756, 50346)]
for t in part1_tests:
    assert recursive_fuel(t[0])[0] == t[1]
for t in part2_tests:
    assert sum(recursive_fuel(t[0])) == t[1]
print("Tests passed.")

# Part 1
masses = [int(x[0]) for x in util.read_input("input_01.csv")]
fuels = [recursive_fuel(m) for m in masses]
first_fuel_sum = sum(f[0] for f in fuels)

# Part 2
recursive_fuel_sum = sum(sum(f) for f in fuels)

util.print_solutions(part1=first_fuel_sum, part2=recursive_fuel_sum)

# Regression tests
assert first_fuel_sum == 3320816
assert recursive_fuel_sum == 4978360
print("Regression tests passed.")
