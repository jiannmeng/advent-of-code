import util


def manhattan_dist(from_coord, to_coord=(0, 0)):
    return abs(from_coord[0] - to_coord[0]) + abs(from_coord[1] - to_coord[1])


def draw_line(path):
    coords = []  # List of all coordinates reached, in order.
    here = (0, 0)  # Current location.
    for p in path:
        direction, distance = p[0], int(p[1:])
        movement = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
        for _ in range(distance):
            here = tuple(sum(x) for x in zip(here, movement[direction]))
            coords.append(here)
    return coords


# Test cases.
assert manhattan_dist((0, 0)) == 0
assert manhattan_dist((-3, 8)) == 11
assert manhattan_dist((-1, -2), (3, 4)) == 10
print("Tests passed.")

# Part 1.
input_paths = util.read_input("input_03.csv")
processed_paths = [draw_line(p) for p in input_paths]
intersections = set(processed_paths[0]).intersection(set(processed_paths[1]))
smallest_dist = min([manhattan_dist(i) for i in intersections])

# Part 2.
vals = []
# Add two due to 0-indexing (one for each axis).
for i in intersections:
    vals.append(processed_paths[0].index(i) + processed_paths[1].index(i) + 2)

util.print_solutions(smallest_dist, min(vals))

# Regression tests.
assert smallest_dist == 865
assert min(vals) == 35038
print("Regression tests passed.")
