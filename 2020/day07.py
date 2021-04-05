from typing import Set

import aocd

data = aocd.lines

bag_contains_full = dict()
bag_contains_colours = dict()

for line in data:
    # Parse text
    line = line.replace(" bags", "").replace(" bag", "")
    outer, inner = line.split(" contain ")
    inner = inner.split(", ")
    inner = [word.replace(".", "") for word in inner]
    inner = [tuple(bag.split(" ", maxsplit=1)) for bag in inner]

    if "no" in inner[0]:
        bag_contains_full[outer] = None
        bag_contains_colours[outer] = set()
    else:
        bag_contains_full[outer] = [(int(num), colour) for num, colour in inner]
        bag_contains_colours[outer] = set(colour for (_, colour) in inner)

# Part A: start from shiny gold bag and look upwards through the tree.
done = set()
queue = set()
queue.add("shiny gold")

while queue:
    col = queue.pop() # col is a colour
    done.add(col)
    for k, v in bag_contains_colours.items():
        if col in v and k not in done:
            queue.add(k)

aocd.submit(len(done)-1, part='a') # deduct one because we don't count shiny gold

# Part B: Just count the number of bags iteratively.
queue = [(1, "shiny gold")]
total = -1

while queue:
    num, col = queue.pop()
    total += num
    contains = bag_contains_full[col]
    if contains:
        contains = [(n * num, c) for (n, c) in contains]
        queue.extend(contains)
    else:
        continue
    
aocd.submit(total, part='b')
