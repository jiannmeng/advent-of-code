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
        return f"Memory: {self.mem}, Input: {self.inp}, Output: {self.out}"

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
        return None

    def run(self, pause_on_output=False, debug=False):
        while True:
            self.step += 1  # Count the steps (for debugging purpose).

            # Get the opcode from the current pointer location.
            instruction = str(self.mem[self.ptr]).zfill(2)  # Ensure at least 2 digits.
            opcode = instruction[-2:]

            if debug:
                print(
                    f"Step: {self.step:04}, Opcode: {opcode}, "
                    f"Input: {self.inp}, Output: {self.out}"
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
                if pause_on_output:
                    return self
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
                return self
            else:
                raise ValueError(
                    f"Instruction:{instruction}, Opcode: {opcode}, is invalid."
                )


with open("input_09.csv") as file:
    program = [int(x) for x in file.readline().split(",")]
print(program)
i = IntcodeComputer(program, [1], memsize=10000)
i.run(debug=True)

j = IntcodeComputer(program, [2], memsize=10000)
j.run()
print(j.out)
