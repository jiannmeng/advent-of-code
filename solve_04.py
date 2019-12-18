import re

import util


def is_valid_1(pwd):
    pwd = str(pwd)  # Password.

    # Two adjacent digits are the same.
    has_adj_same = [pwd[i] == pwd[i + 1] for i in range(len(pwd) - 1)]
    has_adj_same = any(has_adj_same)

    # Going from left to right, the digits never decrease.
    has_no_decr = [int(pwd[i]) <= int(pwd[i + 1]) for i in range(len(pwd) - 1)]
    has_no_decr = all(has_no_decr)

    return has_adj_same and has_no_decr


def is_valid_2(pwd):
    pwd = str(pwd)

    # Has exactly 2 adjacent digits which are the same.
    repeats = re.compile(r"(\d)\1+").finditer(pwd)
    repeats = [r.group() for r in repeats]
    has_exactly_2_adj = [True if len(r) == 2 else False for r in repeats]
    has_exactly_2_adj = any(has_exactly_2_adj)

    # Going from left to right, the digits never decrease.
    has_no_decr = [int(pwd[i]) <= int(pwd[i + 1]) for i in range(len(pwd) - 1)]
    has_no_decr = all(has_no_decr)

    return has_exactly_2_adj and has_no_decr


# Test cases.
assert is_valid_1(111111)
assert not is_valid_1(223450)
assert not is_valid_1(123789)
assert is_valid_2(112233)
assert not is_valid_2(123444)
assert is_valid_2(111122)
print("Tests passed.")

# Part 1.
input_range = util.read_input("input_04.csv")[0][0].split("-")
pwd_range = tuple(int(x) for x in input_range)
part1_solution = 0
for x in range(pwd_range[0], pwd_range[1] + 1):
    if is_valid_1(x):
        part1_solution += 1

# Part 2.
part2_solution = 0
for x in range(pwd_range[0], pwd_range[1] + 1):
    if is_valid_2(x):
        part2_solution += 1

util.print_solutions(part1_solution, part2_solution)

# Regression tests.
assert part1_solution == 979
assert part2_solution == 635
print("Regression tests passed.")
