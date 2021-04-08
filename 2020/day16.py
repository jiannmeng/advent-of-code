import re

import aocd

data = aocd.data  # type: ignore
rules, mine, nearby = data.split("\n\n")

rules_regex = r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)"
rules = rules.split("\n")
rules = [re.match(rules_regex, r).groups() for r in rules]
rules = {a: tuple(map(int, (b, c, d, e))) for a, b, c, d, e in rules}

mine = [int(x) for x in mine.split("\n")[1].split(",")]

nearby = nearby.split("\n")[1:]
nearby = [n.split(",") for n in nearby]
nearby = [[int(x) for x in row] for row in nearby]

# Part A
valid_nums = set()
for r in rules.values():
    min1, max1, min2, max2 = r
    valid_nums.update(range(min1, max1 + 1))
    valid_nums.update(range(min2, max2 + 1))

error_rate: int = 0
valid_nearby = []
for ticket in nearby:
    is_valid_ticket = True
    for field in ticket:
        if field not in valid_nums:
            error_rate += field
            is_valid_ticket = False
    if is_valid_ticket:
        valid_nearby.append(ticket)

aocd.submit(error_rate, part="a")

# Part B
def values_to_set(min1, max1, min2, max2):
    valid = set(range(min1, max1 + 1))
    valid.update(range(min2, max2 + 1))
    return valid


rules = {k: values_to_set(*v) for k, v in rules.items()}
candidates: list[list[str]] = []
name = ""
for col in zip(*valid_nearby):
    valid: list[str] = []
    for name, rule_set in rules.items():
        if set(col) - rule_set:
            # Contains an invalid value, hence not the right field.
            continue
        else:
            # All values valid, this is the right field!
            valid.append(name)
    candidates.append(valid)

total = 1
count = 0
while True:
    for cand, value in zip(candidates, mine):
        if len(cand) == 1:  # Only possible choice
            name = cand[0]
            candidates = [[n for n in c if n != name] for c in candidates]
            if name[:9] == "departure":
                total *= value
                count += 1
    if count == 6:
        break

print(total)
aocd.submit(total, part="b")
