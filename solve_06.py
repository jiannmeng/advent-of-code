import util


def calc_orbits(orbits):
    # orbits = list of strings: "COM)B"
    total = 0
    score = 1
    now = ["COM"]
    next = []
    while len(orbits) != 0:
        for planet in now:
            try:
                search = [o for o in orbits if planet + ")" in o]
                [orbits.remove(s) for s in search]
                [next.append(s.split(")")[1]) for s in search]
            except IndexError:
                pass
        total += score * len(next)
        now = next
        next = []
        score += 1
    return total


# Test cases.
test_orbits = util.read_input("test_06.csv")
test_orbits = [x[0][:-1] for x in test_orbits]  # Remove newline

# Part 1.
part1_orbits = [x[0].strip() for x in util.read_input("input_06.csv")]

# Part 2.

