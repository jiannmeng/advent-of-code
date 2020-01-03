from collections import defaultdict
from math import log, ceil


class AlchemistWorkbench:
    def __init__(self, formulafile, fuelstart):
        # Read file.
        with open(formulafile) as f:
            tmp = [x.strip() for x in f.readlines()]

        # Parse formulas into a dictionary. Key = output, Value = list of inputs.
        formulas = dict()
        for line in tmp:
            line = line.replace(" => ", " ").replace(",", "").split(" ")
            values = [(y, int(x)) for x, y in zip(line[::2], line[1::2])]
            key = values.pop()
            formulas[key] = values
        self.formulas = formulas

        # Number of crafted ingredients. e.g. {"A": 1, "B": 3}
        self.crafted = defaultdict(int)

        # Number of spare ingredients (extra ingredients created when crafting other
        # things). e.g. {"A": 3, "B": 5}
        self.spare = defaultdict(int)

        # Number of ingredients we need to craft. e.g. {"FUEL": 1, "A": 4}
        self.tocraft = defaultdict(int)
        self.tocraft["FUEL"] = fuelstart

    def __repr__(self):
        tmp = f"spare: {dict(self.spare)}, tocraft: {dict(self.tocraft)}, crafted: {dict(self.crafted)}"
        return tmp

    def _find_key(self, ingredient):
        """Enter an ingredient string. Return its key in self.formulas."""
        tmp = [key for key in self.formulas if key[0] == ingredient]
        return tmp[0]

    def _only_ore(self):
        """Return True is self.tocraft only has ORE remaining."""
        tmp = [(v == 0 or k == "ORE") for k, v in self.tocraft.items()]
        return all(tmp)

    def _pick_non_ore(self):
        """Pick a non-ORE ingredient which needs to be crafted in self.tocraft"""
        tmp = [k for k, v in self.tocraft.items() if v > 0 and k != "ORE"]
        try:
            return tmp[0]
        except:
            raise ValueError("No non-ore in tocraft!")

    def craft(self, ingredient):
        """Look at self.tocraft, and craft that many ingredients.

        Will use ingredients in self.spare, and add any extra ingredients needed to
        self.tocraft.
        """
        key = self._find_key(ingredient)
        times = ceil(self.tocraft[ingredient] / key[1])  # craft this many times.

        # Input ingredients.
        for ing, amt in self.formulas[key]:
            amt *= times
            # do we have enough spares for crafting this ing?
            surplus = self.spare[ing] - amt
            if surplus >= 0:
                # if enough spares, use them and deduct from self.spare.
                self.crafted[ing] += amt
                self.spare[ing] -= amt
            else:
                # otherwise, use up all spares and mark the remainder in self.tocraft.
                self.crafted[ing] += self.spare[ing]
                self.spare[ing] = 0
                self.tocraft[ing] += -surplus

        # Output ingredient.
        out_ingred, out_amt = key
        out_amt *= times
        self.crafted[out_ingred] += out_amt
        self.tocraft[out_ingred] -= out_amt
        # If overcrafted, add the extras to self.spare.
        if self.tocraft[out_ingred] < 0:
            self.spare[out_ingred] += -self.tocraft[out_ingred]
            self.tocraft[out_ingred] = 0

    def craft_all(self):
        """Craft until only ORE remains in self.tocraft. Return that amount of ORE."""
        while not self._only_ore():
            ing = self._pick_non_ore()
            wb.craft(ing)
        return wb.tocraft["ORE"]


filepath = "inputs/input_14.txt"
ONE_TRILLION = 1_000_000_000_000

# Part 1.
wb = AlchemistWorkbench(filepath, fuelstart=1)
part1 = wb.craft_all()
print(part1)

# Part 2.
# Use powers of 2 to find the right amount of fuel such that total ORE used is just
# under one trillion.
fuel = 0
exponent = ceil(log(ONE_TRILLION, 2))
while exponent > -1:
    fuel += 2 ** exponent  # candidate amount of fuel crafted.
    wb = AlchemistWorkbench(filepath, fuelstart=fuel)
    ore = wb.craft_all()  # number of ORE needed.
    if ore > ONE_TRILLION:
        print("Over :", fuel, ore)
        fuel -= 2 ** exponent
    else:
        print("Under:", fuel, ore)
    exponent -= 1
wb = AlchemistWorkbench(filepath, fuelstart=fuel)
ore = wb.craft_all()  # number of ORE needed.
print("FINAL:", fuel, ore)
part2 = fuel
print(part2)
