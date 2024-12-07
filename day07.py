from loader import load_strs


def parse(line):
    target, operands = line.split(": ")
    return int(target), [int(x) for x in operands.split(" ")]


def is_solvable(target, result, operands, concat=False):
    if len(operands) == 0:
        return target == result
    return (
        is_solvable(target, result + operands[0], operands[1:], concat)
        or is_solvable(target, result * operands[0], operands[1:], concat)
        or (
            concat
            and is_solvable(
                target, int(str(result) + str(operands[0])), operands[1:], concat
            )
        )
    )


def calibration(lines, concat=False):
    res = 0
    for line in lines:
        target, operands = parse(line)
        if is_solvable(target, 0, operands, concat):
            res += target
    return res


if __name__ == "__main__":
    lines = load_strs("inputs/day07.txt")
    print(f"Part 1: {calibration(lines)}")
    print(f"Part 2: {calibration(lines, concat=True)}")


# -- Tests --
fixture = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]


def test_parse_line():
    target, operands = parse(fixture[0])
    assert target == 190
    assert operands[0] == 10
    assert operands[1] == 19


def test_is_solvable():
    target, operands = parse(fixture[0])
    assert is_solvable(target, 0, operands) is True


def test_calibration():
    assert calibration(fixture) == 3749


def test_calibration_concat():
    assert calibration(fixture, concat=True) == 11387
