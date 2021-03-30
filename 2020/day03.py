import aocd

grid = aocd.lines
# grid[d][r]: coordinates uses d as down and r as right. zero-indexed.

SPACE = "."
TREE = "#"

height, width = len(grid), len(grid[0])
d, r = 0, 0

trees = 0
while d < height:
    if grid[d][r] == TREE:
        trees += 1
    d += 1
    r = (r + 3) % width

aocd.submit(trees, part="a")

multiple = 1
for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    d, r, trees = 0, 0, 0
    while d < height:
        if grid[d][r] == TREE:
            trees += 1
        d += down
        r = (r + right) % width
    multiple *= trees

aocd.submit(multiple, part="b")
