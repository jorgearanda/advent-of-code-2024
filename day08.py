from collections import defaultdict
from itertools import combinations

from loader import load_strs


def get_antennas(lines):
    antennas = defaultdict(list)
    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char != ".":
                antennas[char].append((i, j))
    return antennas


def get_antinodes_of_pair(a1, a2):
    i_diff = abs(a1[0] - a2[0])
    j_diff = abs(a1[1] - a2[1])
    first, second = (a1, a2) if a1[0] < a2[0] else (a2, a1)
    slope = (second[1] - first[1]) / (second[0] - first[0])
    if slope < 0:
        antinode1 = (first[0] - i_diff, first[1] + j_diff)
        antinode2 = (second[0] + i_diff, second[1] - j_diff)
    else:
        antinode1 = (first[0] - i_diff, first[1] - j_diff)
        antinode2 = (second[0] + i_diff, second[1] + j_diff)
    return antinode1, antinode2


def count_antinodes(lines):
    height = len(lines)
    width = len(lines[0])
    antinodes = set()
    antennas = get_antennas(lines)
    for antenna_pair in antennas.values():
        for a1, a2 in combinations(antenna_pair, 2):
            antinode1, antinode2 = get_antinodes_of_pair(a1, a2)
            if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                antinodes.add(antinode1)
            if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                antinodes.add(antinode2)

    return len(antinodes)


def get_resonants_of_pair(a1, a2, height, width):
    resonants = set()
    i_diff = abs(a1[0] - a2[0])
    j_diff = abs(a1[1] - a2[1])
    first, second = (a1, a2) if a1[0] < a2[0] else (a2, a1)
    slope = (second[1] - first[1]) / (second[0] - first[0])
    col, row = a1
    while 0 <= col < width and 0 <= row < height:
        resonants.add((col, row))
        col -= i_diff  # towards first column
        if slope < 0:
            row += j_diff
        else:
            row -= j_diff
    col, row = a1
    while 0 <= col < width and 0 <= row < height:
        resonants.add((col, row))
        col += i_diff  # towards last column
        if slope < 0:
            row -= j_diff
        else:
            row += j_diff
    return resonants


def count_resonants(lines):
    height = len(lines)
    width = len(lines[0])
    antennas = get_antennas(lines)
    resonants = set()
    for antenna_pair in antennas.values():
        for a1, a2 in combinations(antenna_pair, 2):
            resonants = resonants.union(get_resonants_of_pair(a1, a2, height, width))
    return len(resonants)


if __name__ == "__main__":
    lines = load_strs("inputs/day08.txt")
    print(f"Part 1: {count_antinodes(lines)}")
    print(f"Part 2: {count_resonants(lines)}")


# -- Tests --
fixture = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]


def test_count_antinodes():
    assert count_antinodes(fixture) == 14


def test_count_resonants():
    assert count_resonants(fixture) == 34
