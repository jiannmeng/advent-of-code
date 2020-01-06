import collections

IntCodeReturn = collections.namedtuple("IntCodeReturn", "memory output")


def intcode(memory, input_=0):
    memory = memory.copy()
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


# PART 1.
with open("inputs/input_05.txt") as file:
    puzzle_input = file.read().split(",")
    puzzle_input = [int(x) for x in puzzle_input]
part1_output = intcode(memory=puzzle_input.copy(), input_=1).output
## Diagnostics: all values should be 0 except last output.
assert all([x == 0] for x in part1_output[1:-1])
## Solution is the last output.
part1 = part1_output[-1]

# PART 2.
part2 = intcode(memory=puzzle_input.copy(), input_=5)
part2 = part2.output[0]

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
