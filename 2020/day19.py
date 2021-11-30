import aocd

data = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
parsed_rules = {
    0: [(4,1,5)],
    1: [(2,3), (3,2)],
    2: [(4,4), (5,5)],
    3: [(4,5), (5,4)],
    4: "a",
    5: "b",
}

def strings_to_ints(strings: str) -> tuple[int]:
    return tuple(int(x) for x in strings.split(" "))

rules, phrases = data.split("\n\n")
rules = rules.split("\n")
result = dict()
for rule in rules:
    label, subrules = rule.split(": ")
    label = int(label)
    if subrules[0] == '"':
        subrules = subrules[1]
    else:
        subrules = subrules.split(" | ")
        subrules = [strings_to_ints(sr) for sr in subrules]
    result[label] = subrules

print(result)

print(result == parsed_rules)

data = "bababa"

def rule_match(ruleno: int, message: str) -> tuple[bool, str]:
    rule = result[ruleno]
    if isinstance(rule, str):
        return (True, )