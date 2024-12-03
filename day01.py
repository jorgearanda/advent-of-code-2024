from collections import Counter

from loader import load_strs


def lists_from(lines):
    list1, list2 = zip(*(map(int, line.split()) for line in lines))
    return sorted(list1), sorted(list2)


def distance(lines):
    list1, list2 = lists_from(lines)
    return sum(abs(list1[i] - list2[i]) for i in range(len(list1)))


def similarity(lines):
    list1, list2 = lists_from(lines)
    hash2 = Counter(list2)
    return sum(i * hash2.get(i, 0) for i in list1)


if __name__ == "__main__":
    lines = load_strs("inputs/day01.txt")

    print(f"Part 1: {distance(lines)}")
    print(f"Part 2: {similarity(lines)}")


# -- Tests --
fixture = ["3   4", "4   3", "2   5", "1   3", "3   9", "3   3"]


def test_part_1():
    assert distance(fixture) == 11


def test_part_2():
    assert similarity(fixture) == 31
