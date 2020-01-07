# PART 1.
PART1_DECK_SIZE = 10007
PART1_CARD = 2019

with open("inputs/input_22.txt") as file:
    instructions = file.read().split("\n")
position = PART1_CARD  # the position of card num 2019.

for i in instructions:
    if "deal into new stack" in i:
        position = PART1_DECK_SIZE - position - 1
    elif "cut" in i:
        n = int(i.split(" ")[-1])
        position = (position - n) % PART1_DECK_SIZE
    elif "deal with" in i:
        n = int(i.split(" ")[-1])
        position = (position * n) % PART1_DECK_SIZE

part1 = position

# PART 2.
PART2_DECK_SIZE = 119315717514047
PART2_LOOPS = 101741582076661
PART2_CARD = 2020


def polypow(a, b, exponent, m):
    """
    f(x) = ax + b (mod m)
    f applied to itself `exponent` times.
    """
    if exponent == 0:
        return 1, 0
    if exponent % 2 == 0:
        return polypow((a * a) % m, (a * b + b) % m, exponent // 2, m)
    else:
        c, d = polypow(a, b, exponent - 1, m)
        return (a * c) % m, (a * d + b) % m


a, b = 1, 0
# Work backwords.
for i in reversed(instructions):
    if "deal into new stack" in i:
        a = -a
        b = PART2_DECK_SIZE - b - 1
    elif "cut" in i:
        n = int(i.split(" ")[-1])
        b = (b + n) % PART2_DECK_SIZE
    elif "deal with" in i:
        n = int(i.split(" ")[-1])
        inv = pow(n, -1, PART2_DECK_SIZE)  # modular inverse, python 3.8+ only
        a = (a * inv) % PART2_DECK_SIZE
        b = (b * inv) % PART2_DECK_SIZE

a, b = polypow(a, b, PART2_LOOPS, PART2_DECK_SIZE)
part2 = (PART2_CARD * a + b) % PART2_DECK_SIZE

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
