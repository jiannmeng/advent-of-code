class IntcodeComputer:
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    def __init__(self, mem, inp, memsize=None):
        if memsize is None:
            memsize = len(mem)
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
        self.need_input = False

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
        if self.need_input:
            if len(self.inp) > 0:
                self.need_input = False
                pass
            else:
                print("Awaiting input...")
                return self
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
                if len(self.inp) == 0:
                    self.step -= 1
                    self.need_input = True
                    # print("Awaiting input... (use method additional_inputs).")
                    return self
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

            if not self.halt and outputs == 0:
                pass
            elif self.halt or output_counter >= outputs:
                return self


EMPTY = 0
WALL = 1
BLOCK = 2
HORIZONTAL_PADDLE = 3
BALL = 4


class Game:
    def __init__(self):
        self.points = dict()
        self.score = 0

    def coord_range(self):
        all_x = set(k[0] for k in self.points)
        all_y = set(k[1] for k in self.points)
        range_x = range(min(all_x), max(all_x) + 1)
        range_y = range(min(all_y), max(all_y) + 1)
        return (range_x, range_y)

    def add_or_update_point(self, coord, point):
        if coord == (-1, 0):
            self.score = point
        else:
            self.points[coord] = point

    def ball_x(self):
        """Return x-coord of the ball."""
        try:
            return [k[0] for k, v in self.points.items() if v == BALL][0]
        except KeyError:
            return 0

    def paddle_x(self):
        """Return x-coord of the paddle."""
        try:
            return [k[0] for k, v in self.points.items() if v == HORIZONTAL_PADDLE][0]
        except KeyError:
            return 0

    def count_blocks(self):
        """Count number of blocks in the game."""
        return len([x for _, x in self.points.items() if x == BLOCK])

    def __str__(self):
        range_x, range_y = self.coord_range()
        display = ""
        for y in range_y:
            for x in range_x:
                tile = self.points.get((x, y), EMPTY)
                if tile == EMPTY:
                    display += " "
                elif tile == WALL:
                    display += "#"
                elif tile == BLOCK:
                    display += "B"
                elif tile == HORIZONTAL_PADDLE:
                    display += "="
                elif tile == BALL:
                    display += "O"
            display += "\n"
        display += f"Score: {self.score}"
        return display


with open("inputs/input_13.txt") as file:
    program = [int(x) for x in file.read().split(",")]

# PART 1.
computer = IntcodeComputer(mem=program, inp=[], memsize=10000)
grid = Game()

while True:
    computer.run(3)
    grid.add_or_update_point(
        coord=(computer.out[-3], computer.out[-2]), point=computer.out[-1]
    )
    if computer.halt:
        break

part1 = grid.count_blocks()

# PART 2.
program[0] = 2
computer = IntcodeComputer(mem=program, inp=[], memsize=10000)
grid = Game()
frame = 0

while True:
    computer.run(3)
    grid.add_or_update_point(
        coord=(computer.out[-3], computer.out[-2]), point=computer.out[-1]
    )
    if computer.need_input:
        frame += 1
        # print(grid)  # uncomment to view grid.
        # input("Press ENTER to continue...")  # uncomment to pause at each frame.

        computer.append_input(
            [
                -1
                if grid.ball_x() < grid.paddle_x()
                else 1
                if grid.ball_x() > grid.paddle_x()
                else 0
            ]
        )

    if grid.count_blocks() == 0 and computer.step > 10_000:
        # Run one more step to update score!
        computer.run(3)
        grid.add_or_update_point(
            coord=(computer.out[-3], computer.out[-2]), point=computer.out[-1]
        )
        break

part2 = grid.score

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
