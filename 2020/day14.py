import itertools
import re

import aocd


# Functions from https://realpython.com/python-bitwise-operators/
def set_bit(value: int, bit_index: int) -> int:
    return value | (1 << bit_index)


def clear_bit(value: int, bit_index: int) -> int:
    return value & ~(1 << bit_index)


def find_positions(s: str, char: str) -> list[int]:
    return [pos for pos, c in enumerate(s) if c == char]


mask_regex = r"mask = ([01X]+)"
mem_regex = r"mem\[(\d+)\] = (\d+)"

set_mask: list[int] = []
clear_mask: list[int] = []
memory = dict()

program = aocd.lines  # type:ignore
for line in program:
    if m := re.match(mask_regex, line):
        mask = m.group(1)
        rev_mask = mask[::-1]  # reverse the string to find position from end of string
        set_mask = find_positions(rev_mask, "1")
        clear_mask = find_positions(rev_mask, "0")
    if m := re.match(mem_regex, line):
        ptr, value = map(int, m.groups())
        for s in set_mask:
            value = set_bit(value, s)
        for c in clear_mask:
            value = clear_bit(value, c)
        memory[ptr] = value

answer = sum(memory.values())
print(answer)
aocd.submit(answer, part="a")

# Part B

set_mask: list[int] = []
clear_mask: list[int] = []
float_mask: list[int] = []
memory = dict()

for line in program:
    if m := re.match(mask_regex, line):
        mask = m.group(1)
        rev_mask = mask[::-1]  # reverse the string to find position from end of string
        set_mask = find_positions(rev_mask, "1")
        clear_mask = find_positions(rev_mask, "0")
        float_mask = find_positions(rev_mask, "X")
    if m := re.match(mem_regex, line):
        ptr, value = map(int, m.groups())
        for s in set_mask:
            ptr = set_bit(ptr, s)

        runs = itertools.product([1, 0], repeat=len(float_mask))
        ptrs = []
        for run in runs:
            temp = ptr
            for which, bit_index in zip(run, float_mask):
                if which == 1:
                    temp = set_bit(temp, bit_index)
                else:
                    temp = clear_bit(temp, bit_index)
            ptrs.append(temp)

        for ptr in ptrs:
            memory[ptr] = value

answer = sum(memory.values())
print(answer)
aocd.submit(answer, part="b")
