import csv
from math import floor


def recursive_fuel(mass):
    fuel = max(floor(mass / 3) - 2, 0)
    if fuel:
        return [fuel] + recursive_fuel(fuel)
    else:
        return [0]


with open("input_01.csv", "r") as f:
    reader = csv.reader(f)
    masses = list(reader)
    masses = [int(m[0]) for m in masses]
fuels = [recursive_fuel(m) for m in masses]

# Part 1
first_fuel_sum = sum(f[0] for f in fuels)
print(f"Simple fuel requirement is {first_fuel_sum}.")

# Part 2
recursive_fuel_sum = sum(sum(f) for f in fuels)
print(f"Recursive fuel requirement is {recursive_fuel_sum}.")
