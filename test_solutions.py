import solve_01
import solve_02
import solve_03
import solve_04
import solve_05
import solve_06
import solve_07
import solve_08
import solve_09
import solve_10

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
    from solve_05 import intcode

    # Tests from Day 2.
    d2tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    for t in d2tests:
        assert intcode(memory=t[0]).memory == t[1]

    # Tests from Day 5.
    ## Memory checks.
    ## (memory_before, memory_after)
    d5tests_mem = [
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99,]),
    ]
    for t in d5tests_mem:
        assert intcode(memory=t[0]).memory == t[1]

    ## Output checks.
    ## (memory, input, output)
    d5tests_out = [
        ([3, 0, 4, 0, 99], 12, [12]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, [1]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, [0]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, [1]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, [1]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 10, [1]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, [0]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 10, [1]),
    ]
    for t in d5tests_out:
        assert intcode(memory=t[0], input_=t[1]).output == t[2]

    ## "Larger example" test.
    with open("inputs/test_05.txt") as file:
        test_prog = file.read().split(",")
        test_prog = [int(x) for x in test_prog]
    assert intcode(test_prog, input_=7).output == [999]
    assert intcode(test_prog, input_=8).output == [1000]
    assert intcode(test_prog, input_=9).output == [1001]

    assert solve_05.part1 == 2845163
    assert solve_05.part2 == 9436229


def test_06():
    with open("inputs/test_06.txt") as file:
        test_orbits = [x.strip() for x in file.readlines()]
    assert solve_06.calc_orbits(test_orbits) == 42

    assert solve_06.part1 == 253104
    assert solve_06.part2 == 499


def test_07():
    memory = dict()
    for letter in ["a", "b", "c", "d", "e"]:
        with open(f"inputs/test_07{letter}.txt") as file:
            memory[letter] = [int(x.strip()) for x in file.read().split(",")]

    single_test = {"a": 43210, "b": 54321, "c": 65210}
    for letter in single_test:
        assert solve_07.run_amps("single", memory[letter]) == single_test[letter]

    feedback_test = {"d": 139629729, "e": 18216}
    for letter in feedback_test:
        assert solve_07.run_amps("feedback", memory[letter]) == feedback_test[letter]

    assert solve_07.part1 == 422858
    assert solve_07.part2 == 14897241


def test_08():
    assert solve_08.part1 == 1548
    assert solve_08.part2 == [
        " ##  #### #  # #  #  ##  ",
        "#  # #    # #  #  # #  # ",
        "#    ###  ##   #  # #  # ",
        "#    #    # #  #  # #### ",
        "#  # #    # #  #  # #  # ",
        " ##  #### #  #  ##  #  # ",
    ]


def test_09():
    from solve_09 import IntcodeComputer

    # Tests from Day 2.
    d2tests = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ]
    for t in d2tests:
        itc = IntcodeComputer(mem=t[0], inp=[]).run()
        assert itc.mem == t[1]

    # Tests from Day 5.
    ## Memory checks.
    ## (memory_before, memory_after)
    d5tests_mem = [
        ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99,]),
    ]
    for t in d5tests_mem:
        itc = IntcodeComputer(mem=t[0], inp=[]).run()
        assert itc.mem == t[1]

    ## Output checks.
    ## (memory, input, output)
    d5tests_out = [
        ([3, 0, 4, 0, 99], [12], [12]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8], [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [9], [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7], [1]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8], [0]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8], [1]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [9], [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7], [1]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8], [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0], [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [10], [1]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0], [0]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [10], [1]),
    ]
    for t in d5tests_out:
        itc = IntcodeComputer(mem=t[0], inp=t[1]).run()
        assert itc.out == t[2]

    ## "Larger example" test.
    with open("inputs/test_05.txt") as file:
        test_prog = file.read().split(",")
        test_prog = [int(x) for x in test_prog]
    ## (input, output)
    d5tests_large = [([7], [999]), ([8], [1000]), ([9], [1001])]
    for t in d5tests_large:
        itc = IntcodeComputer(mem=test_prog, inp=t[0]).run()
        assert itc.out == t[1]

    assert solve_09.part1 == 3906448201
    assert solve_09.part2 == 59785


def test_10():
    assert solve_10.part1 == 269
    assert solve_10.part2 == 612
