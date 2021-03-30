def intcode(memory):
    memory = memory.copy()
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
        pointer += increm


def program(memory, noun, verb):
    memory_copy = memory.copy()
    memory_copy[1] = noun
    memory_copy[2] = verb
    return intcode(memory_copy)[0]


# PART 1.
with open("inputs/input_02.txt") as file:
    input_program = [int(x) for x in file.read().split(",")]
part1 = program(input_program, 12, 2)

# PART 2.
for noun in range(0, 100):
    for verb in range(0, 100):
        output = program(input_program, noun, verb)
        if output == 19690720:
            part2 = 100 * noun + verb

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}, noun: {noun}, verb: {verb}.")
