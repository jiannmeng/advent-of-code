from itertools import accumulate, combinations

import aocd

data = aocd.numbers

invalid = 0
for i, elem in enumerate(data[25:], 25):
    sums = set(sum(tup) for tup in combinations(data[i-25:i], 2))
    if elem not in sums:
        invalid = elem
        break

aocd.submit(invalid, part="a")

length = len(data)
answer = 0
for i, elem in enumerate(data):
    for j, total in enumerate(accumulate(data[i:])):
        if total > invalid:
            break
        if total == invalid:
            contiguous = data[i:i+j]
            answer = min(contiguous) + max(contiguous)
            break
    if answer:
        break

aocd.submit(answer, part="b")
    
        

