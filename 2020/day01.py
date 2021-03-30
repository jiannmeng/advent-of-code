import aocd
from itertools import product

data = set(aocd.numbers)

for x in data:
    if 2020 - x in data:
        aocd.submit(x * (2020 - x), part="a")
        break

for x, y in product(data, repeat=2):
    if 2020 - x - y in data:
        aocd.submit(x * y * (2020 - x - y), part="b")
        break
