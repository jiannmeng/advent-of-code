import collections
import util

IntCodeReturn = collections.namedtuple("IntCode", "memory output")


def intcode(memory, input_=0):
    pointer = 0
    output = []

    def get_value(next, mode):
        if mode == "pos":
            return memory[memory[pointer + next]]
        elif mode == "imm":
            return memory[pointer + next]
        else:
            raise ValueError(f"Invalid mode: {mode}.")

    def set_value(next, value):
        memory[memory[pointer + next]] = value
        return None

    while True:
        instruction = str(memory[pointer]).zfill(2)  # Ensure at least 2 digits.
        opcode = instruction[-2:]

        # Determine modes of parameters.
        modes = ["pos", "pos", "pos"]
        for i in range(3):
            try:
                modes[i] = "imm" if instruction[-i - 3] == "1" else "pos"
            except IndexError:
                modes[i] = "pos"

        # Perform operation.
        if opcode == "01":
            increm = 4
            set_value(3, get_value(1, modes[0]) + get_value(2, modes[1]))
        elif opcode == "02":
            increm = 4
            set_value(3, get_value(1, modes[0]) * get_value(2, modes[1]))
        elif opcode == "03":
            increm = 2
            set_value(1, input_)
        elif opcode == "04":
            increm = 2
            output.append(get_value(1, modes[0]))
        elif opcode == "05":
            if get_value(1, modes[0]) != 0:
                pointer = get_value(2, modes[1])
                increm = 0
            else:
                increm = 3
        elif opcode == "06":
            if get_value(1, modes[0]) == 0:
                pointer = get_value(2, modes[1])
                increm = 0
            else:
                increm = 3
        elif opcode == "07":
            increm = 4
            set_value(3, 1 if get_value(1, modes[0]) < get_value(2, modes[1]) else 0)
        elif opcode == "08":
            increm = 4
            set_value(3, 1 if get_value(1, modes[0]) == get_value(2, modes[1]) else 0)
        elif opcode == "99":
            return IntCodeReturn(memory=memory, output=output)
        else:
            raise ValueError(
                f"Current pointer value: {instruction} is not a valid instruction."
            )
        pointer += increm
    return IntCodeReturn(memory=memory, output=output)


# Test cases.
## Day 2 tests:
tests = [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
]
for t in tests:
    assert intcode(memory=t[0]).memory == t[1]
## Memory checks.
assert intcode(memory=[1002, 4, 3, 4, 33]).memory == [1002, 4, 3, 4, 99]
assert intcode(memory=[1101, 100, -1, 4, 0]).memory == [1101, 100, -1, 4, 99]
## Output checks.
assert intcode(memory=[3, 0, 4, 0, 99], input_=12).output == [12]
## Part 2 checks.
assert intcode(memory=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_=8).output == [1]
assert intcode(memory=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_=9).output == [0]
assert intcode(memory=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_=7).output == [1]
assert intcode(memory=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_=8).output == [0]
assert intcode(memory=[3, 3, 1108, -1, 8, 3, 4, 3, 99], input_=8).output == [1]
assert intcode(memory=[3, 3, 1108, -1, 8, 3, 4, 3, 99], input_=9).output == [0]
assert intcode(memory=[3, 3, 1107, -1, 8, 3, 4, 3, 99], input_=7).output == [1]
assert intcode(memory=[3, 3, 1107, -1, 8, 3, 4, 3, 99], input_=8).output == [0]
assert intcode(
    memory=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_=0
).output == [0]
assert intcode(
    memory=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_=10
).output == [1]
assert intcode(
    memory=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_=0
).output == [0]
assert intcode(
    memory=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_=10
).output == [1]
test = util.read_input("test_05.csv")[0]
test = [int(x) for x in test]
assert intcode(test, input_=7).output == [999]
assert intcode(test, input_=8).output == [1000]
assert intcode(test, input_=9).output == [1001]
print("Tests passed.")

# Part 1.
puzzle_input = util.read_input("input_05.csv")[0]
puzzle_input = [int(x) for x in puzzle_input]
part1_output = intcode(memory=puzzle_input.copy(), input_=1).output
## Diagnostics: all values should be 0 except last output.
assert all([x == 0] for x in part1_output[1:-1])
## Solution is the last output.
part1_solution = part1_output[-1]

# Part 2.
part2 = intcode(memory=puzzle_input.copy(), input_=5)
print(part2)
part2_solution = part2.output[0]


util.print_solutions(part1_solution, part2_solution)

# Regression tests.
assert part1_solution == 2845163
assert part2_solution == 9436229
print("Regression tests passed.")
