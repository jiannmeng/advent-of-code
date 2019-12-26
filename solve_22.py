from collections import deque

import util


class Deck:
    def __init__(self, num):
        self.num = num
        self.cards = deque(range(num))

    def new_stack(self):
        self.cards.reverse()

    def cut(self, position):
        self.cards.rotate(-position)

    def increment(self, by):
        inv = modinv(by, self.num)
        positions = [(inv * x) % self.num for x in range(self.num)]
        self.cards = deque(self.cards[p] for p in positions)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


instructions = [x[0].strip() for x in util.read_input("input_22.csv")]
deck = Deck(10007)
incs = []
for i in instructions:
    if "deal into new stack" in i:
        deck.new_stack()
    elif "cut" in i:
        n = int(i.split(" ")[-1])
        deck.cut(n)
    elif "deal with" in i:
        n = int(i.split(" ")[-1])
        deck.increment(n)
        incs.append(n)

print(deck.cards.index(2019))

# deck = Deck(119_315_717_514_047)
# for i in instructions:
#     if "deal into new stack" in i:
#         deck.new_stack()
#     elif "cut" in i:
#         n = int(i.split(" ")[-1])
#         deck.cut(n)
#     elif "deal with" in i:
#         n = int(i.split(" ")[-1])
#         deck.increment(n)
# print(deck.cards[2020])

### Part 2
class Card:
    def __init__(self, pos, size):
        self.size = size
        self.pos = pos

    def rev_new_stack(self):
        self.pos = self.size - self.pos

    def rev_cut(self, n):
        self.pos = (self.pos + n) % self.size

    def rev_increment(self, n):
        self.pos = self.pos


inverses = {n: modinv(n, 119315717514047) for n in incs}
print(incs)

from sympy import symbols, Poly

SIZE = 119_315_717_514_047
s, e = symbols("s e")
expr = Poly(s, s, modulus=SIZE)
for i in instructions:
    if "deal into new stack" in i:
        expr = -expr
    elif "cut" in i:
        n = int(i.split(" ")[-1])
        expr = expr - Poly(n, s, modulus=SIZE)
    elif "deal with" in i:
        n = int(i.split(" ")[-1])
        expr = expr * Poly(n, s, modulus=SIZE)

print(expr)
print(expr.subs(s, expr))

mult = -48631267756796 % SIZE
add = 6772912690760 % SIZE
print(mult, add)
multinv = modinv(mult, SIZE)
print(multinv)


def back(y):
    return (multinv * (y - add)) % SIZE


x = 2020
history = set()
len = 0
LOOPS = 101_741_582_076_661


def polypow(a, b, m, n):
    if m == 0:
        return 1, 0
    if m % 2 == 0:
        return polypow(a * a % n, (a * b + b) % n, m // 2, n)
    else:
        c, d = polypow(a, b, m - 1, n)
        return a * c % n, (a * d + b) % n


a, b = 1, 0
for i in reversed(instructions):
    print(i)
    if "deal into new stack" in i:
        a = -a
        b = SIZE - b - 1
    elif "cut" in i:
        n = int(i.split(" ")[-1])
        b = (b + n) % SIZE
    elif "deal with" in i:
        n = int(i.split(" ")[-1])
        z = modinv(n, SIZE)
        a = (a * z) % SIZE
        b = (b * z) % SIZE

print(a, b)
a, b = polypow(a, b, LOOPS, SIZE)
print(a, b)

print((2020 * a + b) % SIZE)
