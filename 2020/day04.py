import aocd
from rich import print

data = aocd.data
data = data.split("\n\n")
data = [s.replace("\n", " ") for s in data]

mandatory = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid_passports = []
for passport in data:
    present = [m in passport for m in mandatory]
    valid_passports.append(all(present))

aocd.submit(sum(valid_passports), part="a")

data_dicts = []
for line, valid in zip(data, valid_passports):
    if not valid:
        continue
    groups = line.split(" ")
    groups = [g.split(":") for g in groups]
    pairs = {key: value for key, value in groups}
    data_dicts.append(pairs)


def validate_byr(x):
    return 1920 <= int(x) <= 2002


def validate_iyr(x):
    return 2010 <= int(x) <= 2020


def validate_eyr(x):
    return 2020 <= int(x) <= 2030


def validate_hgt(x):
    try:
        first_part = int(x[:-2])
        last_two = x[-2:]

        if last_two == "cm":
            return 150 <= first_part <= 193
        if last_two == "in":
            return 59 <= first_part <= 76

        return False
    except:
        return False


def validate_hcl(x):
    if x[0] != "#":
        return False
    for i in range(1, 7):
        if x[i] not in "0123456789abcdef":
            return False
    return True


def validate_ecl(x):
    return x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def validate_pid(x):
    return x.isdigit() and len(x) == 9


count = 0
for passport in data_dicts:
    if not validate_byr(passport["byr"]):
        continue
    if not validate_iyr(passport["iyr"]):
        continue
    if not validate_eyr(passport["eyr"]):
        continue
    if not validate_hgt(passport["hgt"]):
        continue
    if not validate_hcl(passport["hcl"]):
        continue
    if not validate_ecl(passport["ecl"]):
        continue
    if not validate_pid(passport["pid"]):
        continue
    count += 1

aocd.submit(count, part="b")
