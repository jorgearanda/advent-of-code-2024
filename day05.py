from collections import defaultdict
from functools import cmp_to_key

from loader import load_strs

befores = defaultdict(set)
afters = defaultdict(set)


def parse(lines):
    rules = defaultdict(set)
    global befores
    global afters
    updates = []
    in_rules = True
    for line in lines:
        if line == "":
            in_rules = False
            continue
        if in_rules:
            before, after = line.split("|")
            rules[int(before)].add(int(after))
            befores[int(before)].add(int(after))
            afters[int(after)].add(int(before))
        else:
            updates.append(line)
    return updates


def is_fine(update):
    pages = [int(x) for x in update.split(",")]
    for i in range(len(pages)):
        before = pages[:i]
        after = pages[i + 1 :]
        for page in before:
            if pages[i] in afters[page]:
                return False
            if page in befores[pages[i]]:
                return False
        for page in after:
            if pages[i] in befores[page]:
                return False
            if page in afters[pages[i]]:
                return False
    return True


def middle(update):
    pages = [int(x) for x in update.split(",")]
    return pages[len(pages) // 2]


def right_update_middles(lines):
    updates = parse(lines)
    return sum(middle(update) for update in updates if is_fine(update))


def goes_before(a, b):
    return -1 if b in befores[a] or a in afters[b] else 1


def sort_incorrect_update(line):
    pages = [int(x) for x in line.split(",")]
    return sorted(pages, key=cmp_to_key(goes_before))


def middle_jam(update):
    return update[len(update) // 2]


def corrected_updates(lines):
    updates = parse(lines)
    incorrects = [update for update in updates if not is_fine(update)]
    return sum(middle_jam(sort_incorrect_update(incorrect)) for incorrect in incorrects)


if __name__ == "__main__":
    lines = load_strs("inputs/day05.txt")

    print(f"Part 1: {right_update_middles(lines)}")
    print(f"Part 2: {corrected_updates(lines)}")


# -- Tests --
fixture = [
    "47|53",
    "97|13",
    "97|61",
    "97|47",
    "75|29",
    "61|13",
    "75|53",
    "29|13",
    "97|29",
    "53|29",
    "61|53",
    "97|53",
    "61|29",
    "47|13",
    "75|47",
    "97|75",
    "47|61",
    "75|61",
    "47|29",
    "75|13",
    "53|13",
    "",
    "75,47,61,53,29",
    "97,61,53,29,13",
    "75,29,13",
    "75,97,47,61,53",
    "61,13,29",
    "97,13,75,29,47",
]


def test_parse():
    updates = parse(fixture)
    assert befores[97] == {13, 61, 47, 29, 53, 75}
    assert afters[47] == {97, 75}
    assert len(updates) == 6


def test_is_fine():
    parse(fixture)
    assert is_fine("75,47,61,53,29") is True
    assert is_fine("75,97,47,61,53") is False


def test_right_update_middles():
    assert right_update_middles(fixture) == 143


def test_corrected_updates():
    assert corrected_updates(fixture) == 123
