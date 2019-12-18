import csv


def intcode(memory):
    pointer = 0
    while True:
        instruction = memory[pointer]
        if instruction == 99:
            return memory
        elif instruction == 1:
            increm = 4
            p1, p2, p3 = memory[pointer + 1], memory[pointer + 2], memory[pointer + 3]
            memory[p3] = memory[p1] + memory[p2]
        elif instruction == 2:
            increm = 4
            p1, p2, p3 = memory[pointer + 1], memory[pointer + 2], memory[pointer + 3]
            memory[p3] = memory[p1] * memory[p2]
        else:
            raise ValueError(
                f"Current pointer value: {instruction} is not a valid instruction."
            )
        pointer += 4


assert intcode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
assert intcode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert intcode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
assert intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def program(memory, noun, verb):
    memory_copy = memory.copy()
    memory_copy[1] = noun
    memory_copy[2] = verb
    return intcode(memory_copy)[0]


with open("input_02.csv", "r") as f:
    input_program = [[int(x) for x in record] for record in csv.reader(f)][0]

# Part 1
print(f"Part 1: {program(input_program, 12, 2)}")
assert program(input_program, 12, 2) == 5098658

# Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        try:
            output = program(input_program, noun, verb)
            if output == 19690720:
                print(f"Part 2: {100 * noun + verb}")
        except ValueError:
            pass
assert program(input_program, 50, 64) == 19690720

