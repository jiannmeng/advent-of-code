from copy import deepcopy

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRECTION = {NORTH: (0, 1), SOUTH: (0, -1), WEST: (-1, 0), EAST: (1, 0)}

GROUND = "."
WALL = "#"
UNEXPLORED = " "
OXYGEN = "!"

STATUS_WALL = 0
STATUS_MOVED = 1
STATUS_OXYGEN = 2


class IntcodeComputer:
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

    def __init__(self, mem, inp, memsize=None):
        # Copy program to memory. Increase size to memsize.
        if memsize is None:
            memsize = len(mem)
        self.mem = mem.copy()  # memory
        if len(self.mem) < memsize:
            for _ in range(memsize - len(self.mem)):
                self.mem.append(0)

        # Input/output lists.
        self.inp = inp.copy()  # input
        self.out = []  # output

        self.ptr = 0  # pointer
        self.base = 0  # relative base
        self.opcode = "00"
        self.mode = "@000"  # mode of the current instruction.

        self.step = 0  # step
        self.halted = False  # Whether the computer has halted.
        self.input_needed = False

    def __str__(self):
        return (
            f"Current state:\nMemory: {self.mem}, Input: {self.inp}, Output: {self.out}"
        )

    def getmem(self, offset):
        mode = int(self.mode[offset])
        if mode == self.POSITION:
            return self.mem[self.mem[self.ptr + offset]]
        elif mode == self.IMMEDIATE:
            return self.mem[self.ptr + offset]
        elif mode == self.RELATIVE:
            return self.mem[self.mem[self.ptr + offset] + self.base]
        else:
            raise ValueError(f"Invalid mode: {mode}.")

    def setmem(self, offset, value):
        mode = int(self.mode[offset])
        if mode == self.POSITION:
            self.mem[self.mem[self.ptr + offset]] = value
        elif mode == self.IMMEDIATE:
            raise ValueError("Cannot pass IMMEDIATE mode for writing!")
        elif mode == self.RELATIVE:
            self.mem[self.mem[self.ptr + offset] + self.base] = value
        else:
            raise ValueError(f"Invalid mode: {mode}.")

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
        if self.input_needed:
            if len(self.inp) > 0:
                self.input_needed = False
                pass
            else:
                print("Awaiting input...")
                return self
        while True:
            self.step += 1  # Count the steps (for debugging purpose).

            # Get the opcode from the current pointer location.
            instruction = str(self.mem[self.ptr]).zfill(5)  # Ensure at least 2 digits.
            self.opcode = instruction[-2:]
            self.mode = "@" + instruction[2::-1]  # first 3 digits in reverse order

            if debug:
                debug_str = (
                    f"Step: {self.step:04}, Opcode: {self.opcode}, Input: {self.inp}, "
                )

            # Perform operation.
            if self.opcode == "01":  # ADDITION
                self.setmem(3, self.getmem(1) + self.getmem(2))
                self.ptr += 4
            elif self.opcode == "02":  # MULTIPLICATION
                self.setmem(3, self.getmem(1) * self.getmem(2))
                self.ptr += 4
            elif self.opcode == "03":  # INPUT
                if len(self.inp) == 0:
                    self.step -= 1
                    self.input_needed = True
                else:
                    self.setmem(1, self.inp.pop(0))
                    self.ptr += 2
            elif self.opcode == "04":  # OUTPUT
                self.out.append(self.getmem(1))
                self.ptr += 2
                output_counter += 1
            elif self.opcode == "05":  # JUMP IF TRUE
                if self.getmem(1) != 0:
                    self.ptr = self.getmem(2)
                else:
                    self.ptr += 3
            elif self.opcode == "06":  # JUMP IF FALSE
                if self.getmem(1) == 0:
                    self.ptr = self.getmem(2)
                else:
                    self.ptr += 3
            elif self.opcode == "07":  # LESS THAN
                self.setmem(
                    3, 1 if self.getmem(1) < self.getmem(2) else 0,
                )
                self.ptr += 4
            elif self.opcode == "08":  # EQUALS
                self.setmem(
                    3, 1 if self.getmem(1) == self.getmem(2) else 0,
                )
                self.ptr += 4
            elif self.opcode == "09":  # RELATIVE BASE OFFSET
                self.base += self.getmem(1)
                self.ptr += 2
            elif self.opcode == "99":  # HALT COMPUTER
                self.halted = True
            else:
                raise ValueError(
                    f"Instruction:{instruction}, Opcode: {self.opcode}, is invalid."
                )

            if debug:
                print(debug_str + f"Output: {self.out}")
            if (
                self.input_needed
                or self.halted
                or (outputs != 0 and output_counter >= outputs)
            ):
                return self


def addvec(first, second):
    return (first[0] + second[0], first[1] + second[1])


class World:
    def __init__(self, intcode_file):
        with open(intcode_file) as file:
            program = [int(x) for x in file.read().split(",")]
        itc = IntcodeComputer(mem=program, inp=[], memsize=None)

        self.tiles = {(0, 0): GROUND}  # {coord: tile}
        self.savedcomps = {(0, 0): itc}  # {coord: IntcodeComputer at that location}

    def explore(self, xy):
        """Explore the 4 points around coordinates xy.

        Return a dictionary of the form:
            {coords: tile}
        """
        result = dict()
        for k, v in DIRECTION.items():
            target = addvec(xy, v)
            if target not in self.tiles.keys():
                new_itc = deepcopy(self.savedcomps[xy])
                new_itc.inp = [k]
                new_itc.run()
                status = new_itc.out[-1]
                if status == STATUS_WALL:
                    self.tiles[target] = WALL
                elif status == STATUS_MOVED:
                    self.tiles[target] = GROUND
                    self.savedcomps[target] = new_itc
                elif status == STATUS_OXYGEN:
                    self.tiles[target] = OXYGEN
                    self.savedcomps[target] = new_itc
                else:
                    raise ValueError("Invalid status!")
            result[target] = self.tiles[target]
        return result

    def distance_from(self, xy):
        if xy not in self.tiles.keys():
            raise ValueError("xy must be an explored coordinate!")
        distance = 0
        this_round = [xy]
        next_round = []
        result = {xy: distance}
        while True:
            distance += 1
            for xy in this_round:
                for k, v in self.explore(xy).items():
                    if v == WALL:
                        pass
                    elif k not in result.keys() or distance < result[k]:
                        result[k] = distance
                        next_round.append(k)
            if next_round == []:
                break
            else:
                this_round = next_round
                next_round = []
        return result

    def find_tiles(self, tile):
        return [k for k, v in self.tiles.items() if v == tile]

    def print_map(self):
        all_x = [k[0] for k in self.tiles.keys()]
        all_y = [k[1] for k in self.tiles.keys()]
        range_x = range(min(all_x), max(all_x) + 1)
        range_y = range(min(all_y), max(all_y) + 1)

        result = "<<< START MAP >>>\n"
        for y in reversed(range_y):  # draw top to bottom
            line = ""
            for x in range_x:
                line += self.tiles.get((x, y), UNEXPLORED)
            result += line + "\n"
        result += "<<<  END MAP  >>>"
        print(result)


# PART 1.
world = World("inputs/input_15.txt")
dist_from_origin = world.distance_from((0, 0))
oxygen_xy = world.find_tiles(OXYGEN)[0]
part1 = dist_from_origin[oxygen_xy]

# PART 2.
dist_from_oxygen = world.distance_from(oxygen_xy)
part2 = max([v for _, v in dist_from_oxygen.items()])

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
    world.print_map()
