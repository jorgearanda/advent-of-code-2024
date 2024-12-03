import re

from loader import load_strs

muls = r"mul\((\d{1,3}),(\d{1,3})\)"
muls_and_conds = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"


def find_muls(memory, pattern=muls):
    return re.findall(pattern, memory)


def do_muls(memory):
    return sum(int(a) * int(b) for line in memory for a, b in find_muls(line))


def do_muls_and_conds(memory):
    do = True
    res = 0
    for line in memory:
        instructions = find_muls(line, pattern=muls_and_conds)
        for instruction in instructions:
            command, a, b = instruction
            if command == "do()":
                do = True
            elif command == "don't()":
                do = False
            elif do == False:
                continue
            else:
                res += int(a) * int(b)
    return res


if __name__ == "__main__":
    memory = load_strs("inputs/day03.txt")

    print(f"Part 1: {do_muls(memory)}")
    print(f"Part 2: {do_muls_and_conds(memory)}")


# -- Tests --
fixture = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
fixture2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]


def test_find_muls():
    assert len(find_muls(fixture[0])) == 4
    assert find_muls(fixture[0])[0] == ("2", "4")


def test_part_1():
    assert do_muls(fixture) == 161


def test_part_2():
    assert do_muls_and_conds(fixture2) == 48
