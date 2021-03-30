import aocd

def locator(ticket: str) -> int:
    length = 2 ** len(ticket)
    candidates = list(range(length))
    for letter in ticket:
        length //= 2
        if letter in "FL":
            candidates = candidates[:length]
        elif letter in "BR":
            candidates = candidates[length:]
    return candidates[0]

def seat_id(row: int, col: int) -> int:
    return row * 8 + col

data = aocd.lines

seat_ids = set()
for line in data:
    rowstr = line[:7]
    colstr = line[7:]
    row = locator(rowstr)
    col = locator(colstr)
    seat_ids.add(seat_id(row, col))

aocd.submit(max(seat_ids), part="a")

for i in range(min(seat_ids), max(seat_ids)):
    if i not in seat_ids:
        my_seat_id = i
        break

aocd.submit(my_seat_id, part="b")