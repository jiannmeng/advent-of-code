from collections import defaultdict, namedtuple


class IntcodeComputer:
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    def __init__(self, mem, inp, memsize=1000):
        self.mem = mem.copy()  # memory
        if len(self.mem) < memsize:
            for _ in range(memsize - len(self.mem)):
                self.mem.append(0)
        self.base = 0  # relative base
        self.inp = inp.copy()  # input
        self.out = []  # output
        self.ptr = 0  # pointer
        self.step = 0  # step
        self.halt = False  # Whether the computer has halted.

    def __str__(self):
        return (
            f"Current state:\nMemory: {self.mem}, Input: {self.inp}, Output: {self.out}"
        )

    def getmem(self, next, mode):
        if mode == self.POSITION:
            return self.mem[self.mem[self.ptr + next]]
        elif mode == self.IMMEDIATE:
            return self.mem[self.ptr + next]
        elif mode == self.RELATIVE:
            return self.mem[self.mem[self.ptr + next] + self.base]
        else:
            raise ValueError(f"Invalid mode: {mode}.")

    def setmem(self, next, mode, value):
        if mode == self.POSITION:
            self.mem[self.mem[self.ptr + next]] = value
        elif mode == self.IMMEDIATE:
            raise ValueError("Cannot pass IMMEDIATE mode for writing!")
        elif mode == self.RELATIVE:
            self.mem[self.mem[self.ptr + next] + self.base] = value

    def append_input(self, additional_inputs):
        self.inp += additional_inputs
        return self

    def run(self, outputs=0, debug=False):
        """
        outputs: how many outputs to generate before pausing. If set to 0, will run
            until halting. Program always stops if it halts.
        debug: If true, will print debug information for each step.
        """
        output_counter = 0
        while True:
            self.step += 1  # Count the steps (for debugging purpose).

            # Get the opcode from the current pointer location.
            instruction = str(self.mem[self.ptr]).zfill(2)  # Ensure at least 2 digits.
            opcode = instruction[-2:]

            if debug:
                debug_str = (
                    f"Step: {self.step:04}, Opcode: {opcode}, Input: {self.inp}, "
                )

            # Determine modes of parameters.
            modes = [self.POSITION, self.POSITION, self.POSITION]
            for i in range(3):
                try:
                    modes[i] = int(instruction[-i - 3])
                except IndexError:
                    modes[i] = self.POSITION

            # Perform operation.
            if opcode == "01":  # ADDITION
                self.setmem(
                    3, modes[2], self.getmem(1, modes[0]) + self.getmem(2, modes[1])
                )
                self.ptr += 4
            elif opcode == "02":  # MULTIPLICATION
                self.setmem(
                    3, modes[2], self.getmem(1, modes[0]) * self.getmem(2, modes[1])
                )
                self.ptr += 4
            elif opcode == "03":  # INPUT
                self.setmem(1, modes[0], self.inp.pop(0))
                self.ptr += 2
            elif opcode == "04":  # OUTPUT
                self.out.append(self.getmem(1, modes[0]))
                self.ptr += 2
                output_counter += 1
            elif opcode == "05":  # JUMP IF TRUE
                if self.getmem(1, modes[0]) != 0:
                    self.ptr = self.getmem(2, modes[1])
                    self.ptr += 0
                else:
                    self.ptr += 3
            elif opcode == "06":  # JUMP IF FALSE
                if self.getmem(1, modes[0]) == 0:
                    self.ptr = self.getmem(2, modes[1])
                    self.ptr += 0
                else:
                    self.ptr += 3
            elif opcode == "07":  # LESS THAN
                self.setmem(
                    3,
                    modes[2],
                    1 if self.getmem(1, modes[0]) < self.getmem(2, modes[1]) else 0,
                )
                self.ptr += 4
            elif opcode == "08":  # EQUALS
                self.setmem(
                    3,
                    modes[2],
                    1 if self.getmem(1, modes[0]) == self.getmem(2, modes[1]) else 0,
                )
                self.ptr += 4
            elif opcode == "09":  # RELATIVE BASE OFFSET
                self.base += self.getmem(1, modes[0])
                self.ptr += 2
            elif opcode == "99":  # HALT COMPUTER
                self.halt = True
            else:
                raise ValueError(
                    f"Instruction:{instruction}, Opcode: {opcode}, is invalid."
                )

            if debug:
                print(debug_str + f"Output: {self.out}")

            if self.halt or output_counter >= outputs:
                return self


class Grid:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self):
        self.colours = dict()
        self.direction = self.NORTH
        self.position = (0, 0)

    def turn(self, turndir):
        turndir = -1 if turndir == 0 else 1
        self.direction = (self.direction + turndir) % 4
        return self

    def move(self):
        if self.direction == self.NORTH:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == self.EAST:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == self.SOUTH:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == self.WEST:
            self.position = (self.position[0] - 1, self.position[1])
        else:
            raise ValueError("Invalid direction!")

    def paint(self):
        all_x = [k[0] for k in self.colours]
        all_y = [k[1] for k in self.colours]

        range_x = range(min(all_x), max(all_x) + 1)
        range_y = range(min(all_y), max(all_y) + 1)

        all_coords = [(x, y) for y in range_y for x in range_x]
        for y in range_y:
            line = ""
            for x in range_x:
                if self.colours.get((x, y), 0) == 0:
                    line += "."
                else:
                    line += "#"
            print(line)


with open("input_11.csv") as file:
    program = [int(x) for x in file.read().split(",")]

computer = IntcodeComputer(mem=program, inp=[1], memsize=10000)
grid = Grid()

while not computer.halt:
    computer.run(outputs=2)
    grid.colours[grid.position] = computer.out[-2]
    grid.turn(computer.out[-1])
    grid.move()
    computer.append_input([grid.colours.get(grid.position, 0)])

print(len(grid.colours))
print(grid.colours)

grid.paint()
