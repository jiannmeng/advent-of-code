# Intcode test cases.
d2tests = [
    {"mem_before": [1, 0, 0, 0, 99], "mem_after": [2, 0, 0, 0, 99]},
    {"mem_before": [2, 3, 0, 3, 99], "mem_after": [2, 3, 0, 6, 99]},
    {"mem_before": [2, 4, 4, 5, 99, 0], "mem_after": [2, 4, 4, 5, 99, 9801]},
    {
        "mem_before": [1, 1, 1, 4, 99, 5, 6, 0, 99],
        "mem_after": [30, 1, 1, 4, 2, 5, 6, 0, 99],
    },
]

d5tests_mem = [
    {"mem_before": [1002, 4, 3, 4, 33], "mem_after": [1002, 4, 3, 4, 99]},
    {"mem_before": [1101, 100, -1, 4, 0], "mem_after": [1101, 100, -1, 4, 99,]},
]

d5tests_out = [
    {"mem": [3, 0, 4, 0, 99], "inp": [12], "out": [12]},
    {"mem": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "inp": [8], "out": [1]},
    {"mem": [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], "inp": [9], "out": [0]},
    {"mem": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "inp": [7], "out": [1]},
    {"mem": [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], "inp": [8], "out": [0]},
    {"mem": [3, 3, 1108, -1, 8, 3, 4, 3, 99], "inp": [8], "out": [1]},
    {"mem": [3, 3, 1108, -1, 8, 3, 4, 3, 99], "inp": [9], "out": [0]},
    {"mem": [3, 3, 1107, -1, 8, 3, 4, 3, 99], "inp": [7], "out": [1]},
    {"mem": [3, 3, 1107, -1, 8, 3, 4, 3, 99], "inp": [8], "out": [0]},
    {
        "mem": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
        "inp": [0],
        "out": [0],
    },
    {
        "mem": [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
        "inp": [10],
        "out": [1],
    },
    {"mem": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], "inp": [0], "out": [0]},
    {"mem": [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], "inp": [10], "out": [1]},
]

with open("inputs/test_05.txt") as file:
    d5tests_prog = file.read().split(",")
    d5tests_prog = [int(x) for x in d5tests_prog]

d5tests_large = [
    {"inp": [7], "out": [999]},
    {"inp": [8], "out": [1000]},
    {"inp": [9], "out": [1001]},
]


def test_01():
    import solve_01

    tests1 = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
    tests2 = [(14, 2), (1969, 966), (100756, 50346)]
    for t in tests1:
        assert solve_01.recursive_fuel(t[0])[0] == t[1]
    for t in tests2:
        assert sum(solve_01.recursive_fuel(t[0])) == t[1]

    assert solve_01.part1 == 3320816
    assert solve_01.part2 == 4978360


def test_02():
    import solve_02

    for x in d2tests:
        assert solve_02.intcode(x["mem_before"]) == x["mem_after"]

    assert solve_02.part1 == 5098658
    assert solve_02.part2 == 5064


def test_03():
    import solve_03

    assert solve_03.manhattan_dist((0, 0)) == 0
    assert solve_03.manhattan_dist((-3, 8)) == 11
    assert solve_03.manhattan_dist((-1, -2), (3, 4)) == 10

    assert solve_03.part1 == 865
    assert solve_03.part2 == 35038


def test_04():
    import solve_04

    assert solve_04.is_valid_1(111111)
    assert not solve_04.is_valid_1(223450)
    assert not solve_04.is_valid_1(123789)
    assert solve_04.is_valid_2(112233)
    assert not solve_04.is_valid_2(123444)
    assert solve_04.is_valid_2(111122)

    assert solve_04.part1 == 979
    assert solve_04.part2 == 635


def test_05():
    import solve_05
    from solve_05 import intcode

    # Tests from Day 2.
    for x in d2tests:
        assert intcode(memory=x["mem_before"]).memory == x["mem_after"]

    # Tests from Day 5.
    ## Memory checks.
    for x in d5tests_mem:
        assert intcode(memory=x["mem_before"]).memory == x["mem_after"]

    ## Output checks.
    for x in d5tests_out:
        assert intcode(memory=x["mem"], input_=x["inp"][0]).output == x["out"]

    ## "Larger example" test.
    for x in d5tests_large:
        assert intcode(memory=d5tests_prog, input_=x["inp"][0]).output == x["out"]

    assert solve_05.part1 == 2845163
    assert solve_05.part2 == 9436229


def test_06():
    import solve_06

    with open("inputs/test_06.txt") as file:
        test_orbits = [x.strip() for x in file.readlines()]
    assert solve_06.calc_orbits(test_orbits) == 42

    assert solve_06.part1 == 253104
    assert solve_06.part2 == 499


def test_07():
    import solve_07

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
    import solve_08

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
    import solve_09
    from solve_09 import IntcodeComputer

    # Tests from Day 2.
    for x in d2tests:
        itc = IntcodeComputer(mem=x["mem_before"], inp=[]).run()
        assert itc.mem == x["mem_after"]

    # Tests from Day 5.
    ## Memory checks.
    for x in d5tests_mem:
        itc = IntcodeComputer(mem=x["mem_before"], inp=[]).run()
        assert itc.mem == x["mem_after"]

    ## Output checks.
    for x in d5tests_out:
        itc = IntcodeComputer(mem=x["mem"], inp=x["inp"]).run()
        assert itc.out == x["out"]

    ## "Larger example" test.
    for x in d5tests_large:
        itc = IntcodeComputer(mem=d5tests_prog, inp=x["inp"]).run()
        assert itc.out == x["out"]

    assert solve_09.part1 == 3906448201
    assert solve_09.part2 == 59785


def test_10():
    import solve_10

    assert solve_10.part1 == 269
    assert solve_10.part2 == 612
