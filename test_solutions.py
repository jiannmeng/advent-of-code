import solve_01
import solve_02
import solve_03
import solve_04
import solve_05

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


def test_03():
    assert solve_03.manhattan_dist((0, 0)) == 0
    assert solve_03.manhattan_dist((-3, 8)) == 11
    assert solve_03.manhattan_dist((-1, -2), (3, 4)) == 10

    assert solve_03.part1 == 865
    assert solve_03.part2 == 35038


def test_04():
    assert solve_04.is_valid_1(111111)
    assert not solve_04.is_valid_1(223450)
    assert not solve_04.is_valid_1(123789)
    assert solve_04.is_valid_2(112233)
    assert not solve_04.is_valid_2(123444)
    assert solve_04.is_valid_2(111122)

    assert solve_04.part1 == 979
    assert solve_04.part2 == 635


def test_05():
    # Tests from Day 2.
    tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    for t in tests:
        assert solve_05.intcode(memory=t[0]).memory == t[1]

    ## Memory checks.
    assert solve_05.intcode(memory=[1002, 4, 3, 4, 33]).memory == [1002, 4, 3, 4, 99]
    assert solve_05.intcode(memory=[1101, 100, -1, 4, 0]).memory == [
        1101,
        100,
        -1,
        4,
        99,
    ]

    ## Output checks.
    assert solve_05.intcode(memory=[3, 0, 4, 0, 99], input_=12).output == [12]

    ## Part 2 checks.
    assert solve_05.intcode(
        memory=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_=8
    ).output == [1]
    assert solve_05.intcode(
        memory=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_=9
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_=7
    ).output == [1]
    assert solve_05.intcode(
        memory=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_=8
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 3, 1108, -1, 8, 3, 4, 3, 99], input_=8
    ).output == [1]
    assert solve_05.intcode(
        memory=[3, 3, 1108, -1, 8, 3, 4, 3, 99], input_=9
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 3, 1107, -1, 8, 3, 4, 3, 99], input_=7
    ).output == [1]
    assert solve_05.intcode(
        memory=[3, 3, 1107, -1, 8, 3, 4, 3, 99], input_=8
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_=0
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_=10
    ).output == [1]
    assert solve_05.intcode(
        memory=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_=0
    ).output == [0]
    assert solve_05.intcode(
        memory=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_=10
    ).output == [1]

    with open("inputs/test_05.txt") as file:
        test_prog = file.read().split(",")
        test_prog = [int(x) for x in test_prog]
    assert solve_05.intcode(test_prog, input_=7).output == [999]
    assert solve_05.intcode(test_prog, input_=8).output == [1000]
    assert solve_05.intcode(test_prog, input_=9).output == [1001]

    assert solve_05.part1 == 2845163
    assert solve_05.part2 == 9436229
