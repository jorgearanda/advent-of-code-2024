from loader import load_strs


class Map:
    def __init__(self, lines, obstruct_row=None, obstruct_col=None):
        self.map = [list(line) for line in lines]
        if (
            obstruct_row is not None
            and obstruct_col is not None
            and self.map[obstruct_row][obstruct_col] == "."
        ):
            self.map[obstruct_row][obstruct_col] = "O"
        self.visited = [
            [set("^") if x == "^" else set() for x in line] for line in lines
        ]
        for idx, row in enumerate(self.map):
            if "^" in row:
                self.x = row.index("^")
                self.y = idx
                self.dir = "N"
                break
        self.guard_in_map = True
        self.in_loop = False

    def step(self):
        if (
            (self.dir == "N" and self.y == 0)
            or (self.dir == "S" and self.y == len(self.map) - 1)
            or (self.dir == "W" and self.x == 0)
            or (self.dir == "E" and self.x == len(self.map[0]) - 1)
        ):
            self.guard_in_map = False
            return
        if self.dir == "N":
            if self.map[self.y - 1][self.x] == ".":
                self.map[self.y][self.x] = "."
                self.y -= 1
                self.map[self.y][self.x] = "^"
                if "^" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add("^")
            else:
                self.map[self.y][self.x] = ">"
                if ">" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add(">")
                self.dir = "E"
        elif self.dir == "E":
            if self.map[self.y][self.x + 1] == ".":
                self.map[self.y][self.x] = "."
                self.x += 1
                self.map[self.y][self.x] = ">"
                if ">" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add(">")
            else:
                self.map[self.y][self.x] = "v"
                if "v" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add("v")
                self.dir = "S"
        elif self.dir == "S":
            if self.map[self.y + 1][self.x] == ".":
                self.map[self.y][self.x] = "."
                self.y += 1
                self.map[self.y][self.x] = "v"
                if "v" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add("v")
            else:
                self.map[self.y][self.x] = "<"
                if "<" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add("<")
                self.dir = "W"
        elif self.dir == "W":
            if self.map[self.y][self.x - 1] == ".":
                self.map[self.y][self.x] = "."
                self.x -= 1
                if "<" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.map[self.y][self.x] = "<"
                self.visited[self.y][self.x].add("<")
            else:
                self.map[self.y][self.x] = "^"
                if "^" in self.visited[self.y][self.x]:
                    self.in_loop = True
                    return
                self.visited[self.y][self.x].add("^")
                self.dir = "N"

    def print(self):
        for row in self.map:
            print(f"{''.join(row)}")
        print()

    def trace(self):
        while self.guard_in_map and not self.in_loop:
            self.step()
        return sum(1 if len(cell) > 0 else 0 for row in self.visited for cell in row)

    def find_loop(self):
        while self.guard_in_map and not self.in_loop:
            self.step()
        return 1 if self.in_loop else 0


def find_loops(lines):
    loops = 0
    for j in range(len(lines)):
        for i in range(len(lines[0])):
            m = Map(lines, obstruct_row=j, obstruct_col=i)
            loops += m.find_loop()
    return loops


if __name__ == "__main__":
    lines = load_strs("inputs/day06.txt")
    print(f"Part 1: {Map(lines).trace()}")
    print(f"Part 2: {find_loops(lines)}")


# -- Tests --
fixture = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]


def test_visits():
    m = Map(fixture)
    assert m.trace() == 41


def test_loops():
    assert find_loops(fixture) == 6
