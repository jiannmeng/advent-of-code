import aocd
from collections import Counter, defaultdict


def process_input(input: str) -> Counter:
    return Counter(int(x) for x in input.split(","))


def next_day(state: dict) -> dict:
    new_state = defaultdict(int)
    for k, v in state.items():
        if k == 0:
            new_state[8] += v
            new_state[6] += v
        else:
            new_state[k - 1] += v
    return new_state


def run_days(state: dict, days: int):
    for i in range(days):
        state = next_day(state)
        print(i, state)
    return state


def test():
    data = "3,4,3,1,2"
    state = process_input(data)
    assert sum(run_days(state, 18).values()) == 26
    assert sum(run_days(state, 80).values()) == 5934
    print("👍 Test passed!")


def main():
    data = aocd.get_data()
    state = process_input(data)
    parta = sum(run_days(state, 80).values())
    aocd.submit(parta, part="a")
    partb = sum(run_days(state, 256).values())
    aocd.submit(partb, part="b")


test()
main()
