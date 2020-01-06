def calc_orbits(orbits):
    # orbits = list of strings: "COM)B"
    orbits = orbits.copy()
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


def travel_to_com(orbits, here):
    # Find what `here` is orbiting.
    orbiting = [o for o in orbits if ")" + here in o][0].split(")")[0]
    return (
        ["COM"] if orbiting == "COM" else [orbiting] + travel_to_com(orbits, orbiting)
    )


# PART 1.
with open("inputs/input_06.txt") as file:
    orbits = [x.strip() for x in file.readlines()]
part1 = calc_orbits(orbits)

# PART 2.
you_to_com = travel_to_com(orbits, "YOU")
san_to_com = travel_to_com(orbits, "SAN")
san_frozen = frozenset(san_to_com)
intersecting_path = [x for x in you_to_com if x in san_frozen]
intersecting_planet = intersecting_path[0]
distance_from_you = you_to_com.index(intersecting_planet)
distance_from_san = san_to_com.index(intersecting_planet)
part2 = distance_from_you + distance_from_san

if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
