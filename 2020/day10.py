import functools
from collections import Counter

import aocd

data: list[int] = aocd.numbers
data.append(0)
data.append(max(data) + 3)
data.sort()

diffs = [data[i + 1] - data[i] for i in range(len(data) - 1)]
jolts = Counter(diffs)

aocd.submit(jolts[1] * jolts[3], part="a")

end = max(data)


@functools.cache
def ways_from(x: int):
    if x not in data:
        return 0
    elif x == end:
        return 1
    else:
        return ways_from(x + 1) + ways_from(x + 2) + ways_from(x + 3)


aocd.submit(ways_from(0), part="b")
