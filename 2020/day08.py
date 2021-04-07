from dataclasses import dataclass, field
from typing import NamedTuple, Optional

import aocd


class Instruction(NamedTuple):
    op: str  # operation
    arg: int  # argument


@dataclass
class Program:
    bootcode: list[Instruction] = field(default_factory=list)
    acc: int = 0
    ptr: int = 0
    visited: set[int] = field(default_factory=set)
    terminated: bool = False

    @property
    def size(self):
        return len(self.bootcode)

    def reset(self):
        self.acc = 0
        self.ptr = 0
        self.visited = set()
        self.terminated = False
        return self

    def from_aoc(self):
        self.bootcode = [Instruction(line[:3], int(line[4:])) for line in aocd.lines]
        return self

    def run(
        self,
        steps: Optional[int] = None,
        ignore_terminated: bool = False,
        debug: bool = False,
    ):
        while True:
            if self.ptr in self.visited:
                self.terminated = True
            else:
                self.visited.add(self.ptr)

            if self.terminated and not ignore_terminated:
                if debug:
                    print("Stopping due to termination trigger.")
                return self
            elif steps is not None and steps <= 0:
                if debug:
                    print("Stopping due to number of steps.")
                return self
            elif self.ptr >= self.size:
                self.terminated = True
                if debug:
                    print("Stopping due to end of bootcode.")
                return self

            instruction = self.bootcode[self.ptr]

            if instruction.op == "acc":
                self.acc += instruction.arg
                self.ptr += 1
            elif instruction.op == "jmp":
                self.ptr += instruction.arg
            elif instruction.op == "nop":
                self.ptr += 1


# Part A
program = Program().from_aoc()
program.run()
aocd.submit(program.acc, part="a")

# Part B
program = Program().from_aoc()
original_op = ""
for i, line in enumerate(program.bootcode):
    program.reset()
    if line.op == "acc":
        continue
    elif line.op == "jmp":
        original_op = "jmp"
        program.bootcode[i] = Instruction("nop", line.arg)
    elif line.op == "nop":
        original_op = "nop"
        program.bootcode[i] = Instruction("jmp", line.arg)
    program.run()
    if program.ptr >= program.size:
        break
    program.bootcode[i] = Instruction(original_op, line.arg)

aocd.submit(program.acc, part="b")
