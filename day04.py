from loader import load_strs


def count_xmas_in(line):
    return line.count("XMAS") + line[::-1].count("XMAS")


def count_xmas_diagonals(lines):
    xmas = 0
    for j in range(len(lines)):
        line = "".join([lines[j - x][x] for x in range(j + 1)])
        xmas += count_xmas_in(line)
    for i in range(1, len(lines[0])):
        line = "".join(
            lines[x][i + len(lines) - 1 - x] for x in range(len(lines) - 1, i - 1, -1)
        )
        xmas += count_xmas_in(line)
    return xmas


def count_xmas(lines):
    # Horizontal
    xmas = sum(count_xmas_in(line) for line in lines)

    # Vertical
    for i in range(len(lines[0])):
        line = "".join([lines[x][i] for x in range(len(lines))])
        xmas += count_xmas_in(line)

    # Diagonals
    xmas += count_xmas_diagonals(lines)
    xmas += count_xmas_diagonals([line[::-1] for line in lines])

    return xmas


def is_x_mas_in(lines, i, j):
    if lines[i][j] != "A":
        return False
    diag1 = {lines[i - 1][j - 1], lines[i + 1][j + 1]}
    diag2 = {lines[i - 1][j + 1], lines[i + 1][j - 1]}
    return diag1 == diag2 == {"M", "S"}


def count_x_mas(lines):
    return sum(
        1 if is_x_mas_in(lines, i, j) else 0
        for i in range(1, len(lines) - 1)
        for j in range(1, len(lines[0]) - 1)
    )


if __name__ == "__main__":
    lines = load_strs("inputs/day04.txt")

    print(f"Part 1: {count_xmas(lines)}")
    print(f"Part 2: {count_x_mas(lines)}")


# -- Tests --
fixture = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]


def test_count_xmas():
    assert count_xmas(fixture) == 18


def test_count_x_mas():
    assert count_x_mas(fixture) == 9
