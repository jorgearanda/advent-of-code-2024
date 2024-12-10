import sys

from loader import load_strs

sys.setrecursionlimit(100_000)


def parse(line):
    disk_dict = {}
    idx = 0
    idnum = 0
    writing_file = True
    for chr in line:
        for _ in range(int(chr)):
            disk_dict[idx] = idnum if writing_file else None
            idx += 1
        if writing_file:
            idnum += 1
        writing_file = not writing_file
    return disk_dict


def interfile_space(disk):
    in_gap = False
    previously_in_gap = False
    for i in range(len(disk)):
        if disk[i] is None:
            if previously_in_gap:
                return True
            in_gap = True
        elif in_gap:
            previously_in_gap = True
            in_gap = False
    return False


def first_empty(disk):
    for i in range(len(disk)):
        if disk[i] is None:
            return i


def rightmost_file_block(disk):
    for i in range(len(disk) - 1, -1, -1):
        if disk[i] is not None:
            return i, disk[i]


def compact(disk):
    while interfile_space(disk):
        file_idx, file = rightmost_file_block(disk)
        disk[first_empty(disk)], disk[file_idx] = file, None
    return disk


def checksum(disk):
    return sum(i * disk[i] if disk[i] is not None else 0 for i in range(len(disk)))


class Chunk:
    def __init__(self, size, idnum, prev=None):
        self.size = size
        self.empty = idnum is None
        self.idnum = idnum
        self.prev = prev
        self.next = None

    def __str__(self):
        return f"Chunk {self.size=}, {self.empty=}, {self.idnum=}"

    def checksum(self, idx=0):
        local = int(
            0 if self.empty else self.size * (idx + ((self.size - 1) / 2)) * self.idnum
        )
        if self.next is not None:
            return local + self.next.checksum(idx + self.size)
        else:
            return local


def parse_chunks(line):
    idnum = 0
    in_file = True
    prev = None
    for chr in line:
        chunk = Chunk(int(chr), idnum if in_file else None, prev=prev)
        if prev is None:
            first_chunk = chunk
        else:
            prev.next = chunk
        prev = chunk
        if in_file:
            idnum += 1
        in_file = not in_file
    return first_chunk


def get_last_chunk(cur):
    while cur.next is not None:
        cur = cur.next
    return cur


def consolidate(first):
    cur = first
    while cur is not None and cur.next is not None:
        if cur.empty and cur.next.empty:
            cur.size += cur.next.size
            cur.next = cur.next.next
        if cur.size == 0:
            cur.prev.next = cur.next
            if cur.next is not None:
                cur.next.prev = cur.prev
        cur = cur.next


def compact_chunks(first):
    cand = get_last_chunk(first)

    while cand is not None and cand.prev is not None:
        to_process = None
        if cand.empty:
            cand = cand.prev
            continue
        cur = first
        while cur.next is not None:
            if cur == cand:
                if cand.prev is not None:
                    cand = cand.prev
                break
            if cur.empty and cur.size >= cand.size:
                cand.prev.next = Chunk(cand.size, None, cand.prev)
                cand.prev.next.next = cand.next
                if cand.next is not None:
                    cand.next.prev = cand.prev
                to_process = cand.prev
                cur.prev.next = cand
                cand.prev = cur.prev
                if cur.size > cand.size:
                    cur.size = cur.size - cand.size
                    cand.next = cur
                    cur.prev = cand
                else:
                    cur.next.prev = cand
                    cand.next = cur.next
                cand = to_process
                consolidate(first)
                break
            cur = cur.next
        else:
            if cand.prev is not None:
                cand = cand.prev


if __name__ == "__main__":
    disk = load_strs("inputs/day09.txt")[0]
    print(f"Part 1: {checksum(compact(parse(disk)))}")
    first = parse_chunks(disk)
    compact_chunks(first)
    print(f"Part 2: {first.checksum()}")

# -- Tests --
fixture1 = "12345"
fixture2 = "2333133121414131402"


def test_parse():
    disk = parse(fixture1)
    assert len(disk) == 15
    assert disk[0] == 0
    assert disk[2] is None
    assert disk[14] == 2


def test_compact():
    disk = compact(parse(fixture1))
    assert list(disk.values()) == [
        0,
        2,
        2,
        1,
        1,
        1,
        2,
        2,
        2,
        None,
        None,
        None,
        None,
        None,
        None,
    ]


def test_parse_chunks():
    first_chunk = parse_chunks(fixture1)
    assert first_chunk.size == 1
    assert first_chunk.idnum == 0
    assert first_chunk.empty is False
    assert first_chunk.next.size == 2
    assert first_chunk.next.empty is True
    assert first_chunk.next.prev == first_chunk


def test_checksum():
    assert checksum(compact(parse(fixture2))) == 1928


def test_compact_chunks():
    first = parse_chunks(fixture2)
    compact_chunks(first)
    assert first.size == 2
    assert first.idnum == 0
    assert first.next.size == 2
    assert first.next.idnum == 9


def test_checksum_chunks():
    first = parse_chunks(fixture2)
    compact_chunks(first)
    assert first.checksum() == 2858
