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


# PART 1.
with open("inputs/input_03.txt") as file:
    input_paths = file.readlines()
    input_paths = [line.strip().split(",") for line in input_paths]
processed_paths = [draw_line(p) for p in input_paths]
intersections = set(processed_paths[0]).intersection(set(processed_paths[1]))
part1 = min([manhattan_dist(i) for i in intersections])

# PART 2.
vals = []
# Add two due to 0-indexing (one for each axis).
for i in intersections:
    vals.append(processed_paths[0].index(i) + processed_paths[1].index(i) + 2)
part2 = min(vals)

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
