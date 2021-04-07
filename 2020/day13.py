import math

import aocd

earliest, ids_raw = aocd.lines  # type: ignore
earliest = int(earliest)
ids = [int(i) for i in ids_raw.split(",") if i != "x"]


def divisible(num: int, divisor: int) -> bool:
    return num % divisor == 0


now = earliest
while True:
    bus = 0
    divis = [divisible(now, i) for i in ids]
    if any(divis):
        for i, d in zip(ids, divis):
            if d:
                bus = i
                break
    if bus:
        break
    else:
        now += 1

aocd.submit((now - earliest) * bus, part="a")

# Part B
# Chinese remainder theorem!
# https://www.dave4math.com/chinese-remainder-theorem/
# Remainders are the position of each bus id
# Mod is the bus id itself

# a for remainder. a[i] is the i-th remainder
# n for modular divisor. x[i] is the modular divisor for i-th equation
a: list[int] = []
n: list[int] = []
for remainder, bus in enumerate(ids_raw.split(",")):
    if bus == "x":
        continue
    a.append(-remainder)
    n.append(int(bus))
N: int = math.prod(n)
n_bar: list[int] = [N // elem for elem in n]
inv: list[int] = [pow(elem1, -1, elem2) for elem1, elem2 in zip(n_bar, n)]

answer = [x * y * z for x, y, z in zip(inv, a, n_bar)]
answer = sum(answer) % N
aocd.submit(answer, part="b")
