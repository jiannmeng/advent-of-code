class IntCode:
    POSITION = 0
    IMMEDIATE = 1

    def __init__(self, memory, input_):
        self.memory = memory.copy()
        self.input_ = input_.copy()
        self.output = []
        self.pointer = 0

    def get_value(self, next, mode):
        if mode == POSITION:
            return self.memory[self.memory[self.pointer + next]]
        elif mode == IMMEDIATE:
            return self.memory[self.pointer + next]
        else:
            raise ValueError(f"Invalid mode: {mode}.")

    def set_value(self, next, value):
        self.memory[self.memory[self.pointer + next]] = value
        return None

    def run(self, halt_at_output=False, debug=False):
        while True:
            instruction = str(self.memory[self.pointer]).zfill(
                2
            )  # Ensure at least 2 digits.
            opcode = instruction[-2:]

            # Determine modes of parameters.
            modes = [self.POSITION, self.POSITION, self.POSITION]
            for i in range(3):
                try:
                    modes[i] = int(instruction[-i - 3])
                except IndexError:
                    modes[i] = self.POSITION

            # Perform operation.
            if opcode == "01":
                increm = 4
                self.set_value(
                    3, self.get_value(1, modes[0]) + self.get_value(2, modes[1])
                )
            elif opcode == "02":
                increm = 4
                self.set_value(
                    3, self.get_value(1, modes[0]) * self.get_value(2, modes[1])
                )
            elif opcode == "03":
                increm = 2
                self.set_value(1, input_.pop(0))
            elif opcode == "04":
                increm = 2
                self.output.append(self.get_value(1, modes[0]))
                if halt_at_output:
                    return None
            elif opcode == "05":
                if self.get_value(1, modes[0]) != 0:
                    self.pointer = self.get_value(2, modes[1])
                    increm = 0
                else:
                    increm = 3
            elif opcode == "06":
                if self.get_value(1, modes[0]) == 0:
                    self.pointer = self.get_value(2, modes[1])
                    increm = 0
                else:
                    increm = 3
            elif opcode == "07":
                increm = 4
                self.set_value(
                    3,
                    1
                    if self.get_value(1, modes[0]) < self.get_value(2, modes[1])
                    else 0,
                )
            elif opcode == "08":
                increm = 4
                self.set_value(
                    3,
                    1
                    if self.get_value(1, modes[0]) == self.get_value(2, modes[1])
                    else 0,
                )
            elif opcode == "99":
                return None
            else:
                raise ValueError(
                    f"Current pointer value: {instruction} is not a valid instruction."
                )
            pointer += increm

