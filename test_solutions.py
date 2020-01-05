import solve_01
import solve_02

# import solve_03
# import solve_04
# import solve_05
# import solve_06
# import solve_07
# import solve_08
# import solve_09
# import solve_10
# import solve_11
# import solve_12
# import solve_13
# import solve_14


def test_01():
    tests1 = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    tests2 = [(14, 2), (1969, 966), (100756, 50346)]
    for t in tests1:
        assert solve_01.recursive_fuel(t[0])[0] == t[1]
    for t in tests2:
        assert sum(solve_01.recursive_fuel(t[0])) == t[1]

    assert solve_01.part1 == 3320816
    assert solve_01.part2 == 4978360


def test_02():
    tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    for t in tests:
        assert solve_02.intcode(t[0]) == t[1]

    assert solve_02.part1 == 5098658
    assert solve_02.part2 == 5064
