import aocd
from collections import Counter

data = aocd.data.split("\n\n")
group_sizes = [d.count("\n") + 1 for d in data]
data = [d.replace("\n", "") for d in data]

counts = [len(set(d)) for d in data]
aocd.submit(sum(counts), part='a')

answer = 0
counters = [Counter(d) for d in data]
for group, size in zip(counters, group_sizes):
    for question, count in group.items():
        if count == size:
            answer += 1
aocd.submit(answer, part="b")
