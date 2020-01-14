from operator import mul


def pattern(size):
    """Return a list of lists. Each list is the adjusted pattern."""
    base = [0, 1, 0, -1]
    mod = len(base)
    mat = [[base[(j + 1) // (i + 1) % mod] for j in range(size)] for i in range(size)]
    return mat


def mattimesvec(A, b):
    """Return last digit vector result for matrix A * column vector b"""
    return [abs(sum(map(mul, row, b))) % 10 for row in A]


def str2arr(string):
    return [int(x) for x in string]


def arr2str(array):
    array = [str(x) for x in array]
    return "".join(array)


def phase(signalstr, times=1):
    signal = str2arr(signalstr)
    matrix = pattern(len(signal))
    for _ in range(times):
        signal = mattimesvec(matrix, signal)
    return arr2str(signal)


with open("inputs/input_16.txt") as fp:
    signalstr = fp.readline().strip()

# PART 1.
part1 = phase(signalstr, times=100)[:8]

# PART 2.
offset = int(signalstr[:7])
signalstr = signalstr * 10_000
signalstr = signalstr[offset:]


def partial_phase(signalstr, times=1):
    length = len(signalstr)
    rev_signalstr = signalstr[::-1]  # reversed signalstr
    for _ in range(times):
        accum = 0
        result = ""
        for i in range(length):
            accum = (accum + int(rev_signalstr[i])) % 10
            result = result + str(accum)
        rev_signalstr = result
    return rev_signalstr[::-1]  # reverse it back


part2 = partial_phase(signalstr, times=100)[:8]
if __name__ == "__main__":
    print(f"Part 1: {part1}.")
    print(f"Part 2: {part2}.")
