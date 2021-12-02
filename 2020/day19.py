import aocd
from rich import print
data = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

# parsed_rules = {
#     0: [(4, 1, 5)],
#     1: [(2, 3), (3, 2)],
#     2: [(4, 4), (5, 5)],
#     3: [(4, 5), (5, 4)],
#     4: "a",
#     5: "b",
# }

# data = aocd.data


def strings_to_ints(strings: str) -> tuple[int]:
    return tuple(int(x) for x in strings.split(" "))


rules, phrases = data.split("\n\n")
rules = rules.split("\n")
rules_dict = dict()
for rule in rules:
    label, subrules = rule.split(": ")
    label = int(label)
    if subrules[0] == '"':
        subrules = subrules[1]
    else:
        subrules = subrules.split(" | ")
        subrules = [strings_to_ints(sr) for sr in subrules]
    rules_dict[label] = subrules

print(rules_dict)

# print(rules_dict == parsed_rules)

phrases = phrases.split("\n")


def rule_match(ruleno: int, message: str) -> str:
    if message == "":
        return ""
        
    rule = rules_dict[ruleno]
    # if primitive
    if isinstance(rule, str):
        if rule == message[0]:
            return message[0]
        else:
            return ""

    # otherwise, parse each subrule one by one until one is true.
    for rulepart in rule:
        message_copy = message
        # break each rulepart into component rules. stop if any don't match,
        # if all match, proceed.
        matchall = True
        for component in rulepart:
            rulematch = rule_match(component, message_copy)
            if not rulematch:
                matchall = False
                break
            message_copy = message_copy.removeprefix(rulematch)
        if matchall:
            return message.removesuffix(message_copy)

    return ""


def exact_match(phrase: str) -> bool:
    result = rule_match(0, phrase)
    return phrase == result


results = {phrase: exact_match(phrase) for phrase in phrases}
num_true = sum(results.values())
print(num_true)
# aocd.submit(num_true, "a")

# part 2
rules_dict[8] = [(42,), (42, 8)]
rules_dict[11] = [(42, 31), (42, 11, 31)]

print(rules_dict)
for phrase in phrases:
    print(f"{phrase}: {exact_match(phrase)}")

results = {phrase: exact_match(phrase) for phrase in phrases}
num_true = sum(results.values())
print(num_true)
# aocd.submit(num_true, "b")
