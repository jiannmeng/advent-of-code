import aocd
import math

PLUS = "+"
MULT = "*"


def calculate(expr):
    length: int = len(expr)
    ptr: int = 0
    mode = PLUS
    total: int = 0
    while ptr < length:
        char: str = expr[ptr]
        if char in "0123456789":
            if mode == PLUS:
                total += int(char)
            elif mode == MULT:
                total *= int(char)
        elif char in [PLUS, MULT]:
            mode = char
        elif char == "(":
            subtotal, sublength = calculate(expr[ptr + 1 :])
            if mode == PLUS:
                total += subtotal
            elif mode == MULT:
                total *= subtotal
            ptr += sublength + 1  # jump forward to matching close bracket
        elif char == ")":
            break
        ptr += 1
    return total, ptr


def calculate2(expr: str, ptr: int = 0):
    length: int = len(expr)
    mode = MULT
    mults: list[int] = []
    while ptr < length:
        char = expr[ptr]
        if char in "0123456789":
            if mode == MULT:
                mults.append(int(char))
            elif mode == PLUS:
                last = mults.pop()
                mults.append(last + int(char))
        elif char == "(":
            ptr += 1
            subval, ptr = calculate2(expr, ptr)
            if mode == MULT:
                mults.append(subval)
            elif mode == PLUS:
                last = mults.pop()
                mults.append(last + subval)
        elif char == ")":
            return math.prod(mults), ptr
        elif char in [PLUS, MULT]:
            mode = char
        ptr += 1
    return math.prod(mults), ptr


data = aocd.lines  # type: ignore
results = [calculate(expr)[0] for expr in data]
aocd.submit(sum(results), part="a")

results = [calculate2(expr)[0] for expr in data]
aocd.submit(sum(results), part="b")
