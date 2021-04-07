import itertools
from collections import Counter
from copy import deepcopy

import aocd

layout = [[char for char in row] for row in aocd.lines]  # type:ignore
height = len(layout)
width = len(layout[0])

EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."
DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def show_layout(layout):
    print(["".join(row) for row in layout])


def valid_coords(down: int, right: int) -> bool:
    return down >= 0 and down < height and right >= 0 and right < width


def adjacent(down: int, right: int, layout):
    total = 0
    for direction in DIRECTIONS:
        d, r = down + direction[0], right + direction[1]
        if valid_coords(d, r) and layout[d][r] == OCCUPIED:
            total += 1
    return total


def sight(down: int, right: int, layout):
    total = 0
    for direction in DIRECTIONS:
        d, r = down, right
        while True:
            d, r = d + direction[0], r + direction[1]
            if not valid_coords(d, r) or layout[d][r] == EMPTY:
                break
            if layout[d][r] == OCCUPIED:
                total += 1
                break
    return total


def simulate(layout, func, threshold: int, debug=False) -> int:
    prev_layout = deepcopy(layout)
    next_layout = deepcopy(layout)
    while True:
        for d, r in itertools.product(range(height), range(width)):
            adj = func(d, r, layout=prev_layout)
            if prev_layout[d][r] == EMPTY and adj == 0:
                next_layout[d][r] = OCCUPIED
            elif prev_layout[d][r] == OCCUPIED and adj >= threshold:
                next_layout[d][r] = EMPTY
            else:
                next_layout[d][r] = prev_layout[d][r]
        if debug:
            show_layout(next_layout)
        if next_layout == prev_layout:
            return next_layout
        else:
            prev_layout = next_layout
            next_layout = deepcopy(prev_layout)


def count_seats(layout) -> Counter:
    return Counter(itertools.chain.from_iterable(layout))


# Part A
part_a = simulate(layout, adjacent, threshold=4, debug=False)
answer = count_seats(part_a)[OCCUPIED]
aocd.submit(answer, part="a")

# Part B
part_b = simulate(layout, sight, threshold=5, debug=False)
answer = count_seats(part_b)[OCCUPIED]
aocd.submit(answer, part="b")
