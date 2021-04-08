import itertools

import aocd

ACTIVE = "#"
INACTIVE = "."

Coord = tuple[int, int, int, int]

active: set[Coord] = set()


def active_neighbours(x: int, y: int, z: int, w: int, dims):
    movement = []
    total = 0
    adj = [-1, 0, 1]
    if dims == 3:
        movement = [(a, 0, c, d) for a in adj for c in adj for d in adj]
        movement.remove((0, 0, 0, 0))
    elif dims == 4:
        movement = list(itertools.product(adj, repeat=4))
        movement.remove((0, 0, 0, 0))
    for a, b, c, d in movement:
        if (x + a, y + b, z + c, w + d) in active:
            total += 1
    return total


def search_space(active_set: set) -> list[Coord]:
    mins: list[int] = list(map(min, zip(*active_set)))
    maxs: list[int] = list(map(max, zip(*active_set)))
    ranges = [range(small - 1, large + 2) for small, large in zip(mins, maxs)]
    return list(itertools.product(*ranges))  # type:ignore


def parse(initial):
    for r, row in enumerate(initial):
        for c, col in enumerate(row):
            if col == ACTIVE:
                active.add((0, 0, r, c))


initial = aocd.lines  # type: ignore
parse(initial)

for cycle in range(1, 7):
    new_active = set()
    for coord in search_space(active):
        an = active_neighbours(*coord, dims=3)
        if coord in active and an in [2, 3]:
            new_active.add(coord)
        elif coord not in active and an == 3:
            new_active.add(coord)
    active = new_active

aocd.submit(len(active), part="a")

# Part B
active = set()
parse(initial)

for cycle in range(1, 7):
    new_active = set()
    for coord in search_space(active):
        an = active_neighbours(*coord, dims=4)
        if coord in active and an in [2, 3]:
            new_active.add(coord)
        elif coord not in active and an == 3:
            new_active.add(coord)
    active = new_active

print(len(active))
aocd.submit(len(active), part="b")
