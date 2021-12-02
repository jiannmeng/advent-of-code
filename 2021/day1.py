import aocd


def count_increasing(data: list[int]):
    diffs = [j - i for i, j in zip(data[:-1], data[1:])]
    incrs = [x > 0 for x in diffs]
    return sum(incrs)


def count_increasing_sliding(data: list[int]):
    window_sums = [x + y + z for x, y, z in zip(data[:-2], data[1:-1], data[2:])]
    return count_increasing(window_sums)


def test():
    sample_data = """199
    200
    208
    210
    200
    207
    240
    269
    260
    263"""
    sample_data = [int(x) for x in sample_data.splitlines()]

    assert count_increasing(sample_data) == 7
    assert count_increasing_sliding(sample_data) == 5
    print("👌 Tests passed.")


def main():
    data = aocd.numbers  # type:ignore
    aocd.submit(count_increasing(data), "a")
    aocd.submit(count_increasing_sliding(data), "b")


test()
main()
