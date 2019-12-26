import collections
import itertools
import util


class IntcodeComputer:
    POSITION = 0
    IMMEDIATE = 1

    def __init__(self, memory, input_):
        self.mem = memory.copy()  # memory
        self.inp = collections.deque(input_)  # input
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
        else:
            raise ValueError(f"Invalid mode: {mode}.")

    def setmem(self, next, value):
        self.mem[self.mem[self.ptr + next]] = value
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
                increm = 4
                self.setmem(3, self.getmem(1, modes[0]) + self.getmem(2, modes[1]))
            elif opcode == "02":  # MULTIPLICATION
                increm = 4
                self.setmem(3, self.getmem(1, modes[0]) * self.getmem(2, modes[1]))
            elif opcode == "03":  # INPUT
                increm = 2
                self.setmem(1, self.inp.popleft())
            elif opcode == "04":  # OUTPUT
                increm = 2
                self.out.append(self.getmem(1, modes[0]))
                if pause_on_output:
                    self.ptr += increm
                    return self
            elif opcode == "05":  # JUMP IF TRUE
                if self.getmem(1, modes[0]) != 0:
                    self.ptr = self.getmem(2, modes[1])
                    increm = 0
                else:
                    increm = 3
            elif opcode == "06":  # JUMP IF FALSE
                if self.getmem(1, modes[0]) == 0:
                    self.ptr = self.getmem(2, modes[1])
                    increm = 0
                else:
                    increm = 3
            elif opcode == "07":  # LESS THAN
                increm = 4
                self.setmem(
                    3, 1 if self.getmem(1, modes[0]) < self.getmem(2, modes[1]) else 0,
                )
            elif opcode == "08":  # EQUALS
                increm = 4
                self.setmem(
                    3, 1 if self.getmem(1, modes[0]) == self.getmem(2, modes[1]) else 0,
                )
            elif opcode == "99":  # HALT COMPUTER
                self.halt = True
                return self
            else:
                raise ValueError(
                    f"Instruction:{instruction}, Opcode: {opcode}, is invalid."
                )

            # Move the pointer by the appropriate number of positions forward.
            self.ptr += increm


def run_amps(mode, memory):
    if mode == "single":
        phase_perms = itertools.permutations(range(5))  # [0,1,2,3,4] perms
    elif mode == "feedback":
        phase_perms = itertools.permutations(range(5, 10))  # [5,6,7,8,9] perms
    else:
        raise ValueError("Invalid mode. Valid modes are 'single' and 'feedback'.")

    # Last signal sent by amplifier E to the thrusters. One for each phase permutation.
    final_signals = []

    # Repeat for all possible permutations:
    for phase_seq in phase_perms:
        amps = []
        signal = 0

        # Create amplifiers.
        for phase in phase_seq:
            amps.append(IntcodeComputer(memory, [phase]))

        if mode == "single":

            for amp in amps:
                amp.inp.append(signal)  # Receive signal from previous amp.
                amp.run(pause_on_output=False)  # Run the amp until it halts.
                signal = amp.out[-1]  # Pass signal to the next amp.
            final_signals.append(signal)  # We want the final amp's signal.

        if mode == "feedback":

            time_to_halt = False  # Stop when this turns True.
            i = 0  # Which amp to run; this goes 0, 1, 2, 3, 4, 0, 1, 2, 3, etc.
            while not time_to_halt:
                amps[i].inp.append(signal)  # Receive signal from previous amp.
                amps[i].run(pause_on_output=True)  # Run the amp until an output occurs.
                signal = amps[i].out[-1]  # Pass the signal to next amp.
                time_to_halt = amps[i].halt  # Halt all amps when one amp halts.
                i = (i + 1) % 5  # Go to next amp.

            # Once halted, store final amp's signal.
            final_signals.append(amps[4].out[-1])

    return max(final_signals)


memory_a = [int(x) for x in util.read_input("test_07a.csv")[0]]
memory_b = [int(x) for x in util.read_input("test_07b.csv")[0]]
memory_c = [int(x) for x in util.read_input("test_07c.csv")[0]]
memory_d = [int(x) for x in util.read_input("test_07d.csv")[0]]
memory_e = [int(x) for x in util.read_input("test_07e.csv")[0]]
memory = [int(x) for x in util.read_input("input_07.csv")[0]]


print(run_amps("single", memory_a))
print(run_amps("feedback", memory_d))
print(run_amps("feedback", memory_e))
print(run_amps("feedback", memory))
