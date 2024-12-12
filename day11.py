from collections import defaultdict

from loader import load_strs


def count(stones, blinks):
    qtys = stone_qtys(stones)
    for _ in range(blinks):
        qtys = blink(qtys)
    return sum(qtys.values())


def stone_qtys(stones):
    qtys = defaultdict(int)
    for stone in stones.split(" "):
        qtys[int(stone)] += 1
    return qtys


def blink(qtys):
    new_qtys = defaultdict(int)
    for key in qtys.keys():
        if key == 0:
            new_qtys[1] += qtys[0]
        elif len(str(key)) % 2 == 0:
            lt = int(str(key)[: len(str(key)) // 2])
            rt = int(str(key)[len(str(key)) // 2 :])
            new_qtys[lt] += qtys[key]
            new_qtys[rt] += qtys[key]
        else:
            new_qtys[key * 2024] += qtys[key]
    return new_qtys


if __name__ == "__main__":
    stones = load_strs("inputs/day11.txt")[0]
    print(f"Part 1: {count(stones, 25)}")
    print(f"Part 2: {count(stones, 75)}")


# -- Tests --
fixture = "125 17"


def test_25_blinks():
    assert count(fixture, 25) == 55_312
