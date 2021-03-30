import re


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


# PART 1.
with open("inputs/input_04.txt") as file:
    input_range = file.read().split("-")
pwd_range = tuple(int(x) for x in input_range)
part1 = 0
for x in range(pwd_range[0], pwd_range[1] + 1):
    if is_valid_1(x):
        part1 += 1

# PART 2.
part2 = 0
for x in range(pwd_range[0], pwd_range[1] + 1):
    if is_valid_2(x):
        part2 += 1

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
