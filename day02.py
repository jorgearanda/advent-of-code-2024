from copy import deepcopy

from loader import load_strs


def is_safe(report):
    return (
        all(report[i] < report[i + 1] for i in range(len(report) - 1))
        or all(report[i] > report[i + 1] for i in range(len(report) - 1))
    ) and all(1 <= abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1))


def parse(lines):
    reports = []
    for line in lines:
        levels = line.split()
        reports.append([int(i) for i in levels])
    return reports


def safety(lines):
    reports = parse(lines)
    return sum(1 if is_safe(report) else 0 for report in reports)


def is_dampened(report):
    dampened_reports = [report[:i] + report[i + 1 :] for i in range(len(report))]
    return any(is_safe(dampened) for dampened in dampened_reports)


def dampened_safety(lines):
    reports = parse(lines)
    return sum(1 if is_safe(report) or is_dampened(report) else 0 for report in reports)


if __name__ == "__main__":
    lines = load_strs("inputs/day02.txt")

    print(f"Part 1: {safety(lines)}")
    print(f"Part 2: {dampened_safety(lines)}")


# -- Tests --
fixture = ["7 6 4 2 1", "1 2 7 8 9", "9 7 6 2 1", "1 3 2 4 5", "8 6 4 4 1", "1 3 6 7 9"]


def test_is_safe():
    assert is_safe([7, 6, 4, 2, 1]) is True
    assert is_safe([1, 2, 7, 8, 9]) is False


def test_part_1():
    assert safety(fixture) == 2


def test_part_2():
    assert dampened_safety(fixture) == 4
