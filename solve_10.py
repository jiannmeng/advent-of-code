import math
from itertools import product


def diff(base, to):
    """Return difference between x and y cooords of base and to."""
    return (to[0] - base[0], to[1] - base[1])


def distance(base, to):
    """Return scalar difference between base and to."""
    x, y = diff(base, to)
    return math.sqrt(x ** 2 + y ** 2)


def between(base, to):
    """Return all points directly in the path between base and to."""
    # base = (0,0); to = (3,9)
    distance = diff(base, to)  # distance = (3, 9)
    jumps = math.gcd(*distance)  # jumps = 3
    each_jump = tuple(s // jumps for s in distance)  # each_jump = (1, 3)

    all_points_between = []
    if jumps > 0:
        for i in range(1, jumps):
            all_points_between.append(
                (base[0] + each_jump[0] * i, base[1] + each_jump[1] * i,)
            )  # all_points_between = [(1,3), (2,6)]
    return all_points_between


def angle(base, to):
    """Return the angle of to from base, with north as 0 degrees."""
    x, y = diff(base, to)
    if (x, y) == (0, 0):
        raise ValueError("base and to should not be the same!")
    theta = math.degrees(math.atan2(y, x))
    return (theta + 90) % 360


class Map:
    EMPTY = "."
    ASTEROID = "#"

    def __init__(self, mapfile):
        with open(mapfile) as file:
            self.map = file.read().split("\n")
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.points = [(x, y) for x in range(self.width) for y in range(self.height)]

    def __str__(self):
        out = ""
        for row in self.map:
            out += row + "\n"
        return out[:-1]  # remove last newline character.

    def __call__(self, x, y):
        return self.map[y][x]

    def find_asteroids(self):
        return [p for p in self.points if self(*p) == self.ASTEROID]


m = Map("inputs/input_10.txt")

# PART 1.

# `detected` is a dictionary with coordinate keys, and values equal to how
# many asteroids are visible from that coordinate.
detected = dict()
for base in product(range(m.width), range(m.height)):
    if m(*base) == "#":  # asteroid
        count = 0
        for to in m.points:
            if base == to:
                pass
            elif m(*to) == ".":
                pass
            elif m(*to) == "#":
                all_points_between = between(base, to)
                blocked_between = []
                for p in all_points_between:
                    blocked_between.append(m(*p) == "#")
                if not any(blocked_between):
                    count += 1
        detected[base] = count
    elif base == ".":  # empty
        pass
station = max(detected, key=detected.get)
part1 = detected[station]
print(f"Part 1: {part1}, at coordinates {station}.")

# PART 2.

burn_targets = m.find_asteroids()
burn_targets.remove(station)  # don't burn the asteroid we're on!

# Add the angle from station to each asteroid.
# Sorting in the order below is equivalent to sorting by angle, then distance.
burn_targets = [(asteroid, angle(station, asteroid)) for asteroid in burn_targets]
burn_targets.sort(key=lambda x: distance(station, x[0]))
burn_targets.sort(key=lambda x: angle(station, x[0]))

# Start burning the asteroids! `burn_order` tracks when asteroids are burned.
burn_order = []
current_angle = -1
while len(burn_targets) > 0:
    burn_coords, burn_angle = min(
        burn_targets, key=lambda x: x[1] if x[1] > current_angle else 999
    )
    current_angle = burn_angle
    burn_order.append(burn_coords)
    burn_targets.remove((burn_coords, burn_angle))
x, y = burn_order[199]
part2 = 100 * x + y
print(f"Part 2: {part2}, i.e. coordinates {x}, {y}.")
