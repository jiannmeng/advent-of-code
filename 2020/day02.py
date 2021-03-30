import aocd
import re

data = aocd.lines
pattern = re.compile(r"(\d+)-(\d+) (\w): (\w+)")

valid_a = 0
valid_b = 0

for d in data:
    matchobj = pattern.match(d)
    small, large, char, password = matchobj.groups()
    small = int(small)
    large = int(large)

    # Part A
    count = password.count(char)
    if small <= count <= large:
        valid_a += 1

    # Part B
    at_small = password[small - 1] == char
    at_large = password[large - 1] == char
    if at_small ^ at_large:  # XOR
        valid_b += 1

aocd.submit(valid_a, part="a")
aocd.submit(valid_b, part="b")
