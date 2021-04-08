import aocd

numbers = [int(x) for x in aocd.data.split(",")]  # type: ignore
last_seen = dict()
last_last_seen = dict()

x: int = 0
for turn in range(1, 30_000_000 + 1):
    if numbers:
        x = numbers.pop(0)
        last_seen[x] = turn
    else:
        if x in last_last_seen.keys():
            x = turn - 1 - last_last_seen.get(x, 0)
        else:
            x = 0

        if x in last_seen.keys():
            last_last_seen[x] = last_seen[x]
        last_seen[x] = turn

    if turn % 1_000_000 == 0:
        print(f"{turn=}")
    if turn == 2020:
        aocd.submit(x, part="a")
    if turn == 30_000_000:
        aocd.submit(x, part="b")
        break
