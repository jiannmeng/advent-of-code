from dataclasses import dataclass

import aocd

# Clockwise order
DIRECTIONS = {
    0: (1, 0),  # east
    1: (0, -1),  # south
    2: (-1, 0),  # west
    3: (0, 1),  # north
}


def dist(x: int, y: int) -> int:
    return abs(x) + abs(y)


instructions = aocd.lines  # type: ignore
test_instructions = [
    "F10",
    "N3",
    "F7",
    "R90",
    "F11",
]

# Part A


@dataclass
class Ship:
    x: int = 0
    y: int = 0
    facing: int = 0  # start east

    def rotate(self, action: str, value: int):
        value %= 360
        if action == "L":
            value = 360 - value
        value //= 90
        # Now we can assume clockwise turning under 360 degrees
        # Rotate 90 degrees clockwise:
        self.facing = (self.facing + value) % 4

    def move(self, direction: int, value: int):
        movement = tuple(x * value for x in DIRECTIONS[direction])
        self.x += movement[0]
        self.y += movement[1]

    def forward(self, value):
        self.move(direction=self.facing, value=value)

    def do(self, instruction: str):
        action: str = instruction[0]
        value: int = int(instruction[1:])
        if action == "E":
            self.move(0, value)
        elif action == "S":
            self.move(1, value)
        elif action == "W":
            self.move(2, value)
        elif action == "N":
            self.move(3, value)
        elif action == "L":
            self.rotate("L", value)
        elif action == "R":
            self.rotate("R", value)
        elif action == "F":
            self.forward(value)
        # print(f"{instruction=}, {self}")


ship = Ship()
for inst in instructions:
    ship.do(inst)

aocd.submit(dist(ship.x, ship.y), part="a")

# Part B
@dataclass
class ShipWithWaypoint:
    x: int = 0
    y: int = 0
    wpx: int = 10
    wpy: int = 1

    def rotate(self, action: str, value: int):
        value %= 360
        if action == "L":
            value = 360 - value
        value //= 90
        # Now we can assume clockwise turning under 360 degrees
        # Rotate 90 degrees clockwise:
        for _ in range(value):
            self.wpx, self.wpy = self.wpy, -self.wpx

    def move(self, direction: int, value: int):
        movement = tuple(x * value for x in DIRECTIONS[direction])
        self.wpx += movement[0]
        self.wpy += movement[1]

    def forward(self, value):
        self.x += self.wpx * value
        self.y += self.wpy * value

    def do(self, instruction: str):
        action: str = instruction[0]
        value: int = int(instruction[1:])
        if action == "E":
            self.move(0, value)
        elif action == "S":
            self.move(1, value)
        elif action == "W":
            self.move(2, value)
        elif action == "N":
            self.move(3, value)
        elif action == "L":
            self.rotate("L", value)
        elif action == "R":
            self.rotate("R", value)
        elif action == "F":
            self.forward(value)


ship = ShipWithWaypoint()
for inst in instructions:
    ship.do(inst)
aocd.submit(dist(ship.x, ship.y), part="b")
