import collections
import util

IntCode = collections.namedtuple("IntCode", "memory output")


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
        elif opcode == "99":
            return IntCode(memory=memory, output=output)
        else:
            raise ValueError(
                f"Current pointer value: {instruction} is not a valid instruction."
            )
        pointer += increm
    return IntCode(memory=memory, output=output)


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
print("Tests passed.")

# Part 1.
puzzle_input = util.read_input("input_05.csv")[0]
puzzle_input = [int(x) for x in puzzle_input]
part1_output = intcode(memory=puzzle_input, input_=1).output
## Diagnostics: all values should be 0 except last output.
assert all([x == 0] for x in part1_output[1:-1])
## Solution is the last output.
part1_solution = part1_output[-1]

# Part 2.

util.print_solutions(part1_solution, part2_solution)

# Regression tests.
assert part1_solution == 2845163
assert part2_solution == -1
print("Regression tests passed.")
