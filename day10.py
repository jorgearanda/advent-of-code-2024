from loader import load_strs


class Cell:
    def __init__(self, height):
        self.height = int(height)
        self.x = None
        self.y = None
        self.up = None
        self.dn = None
        self.lt = None
        self.rt = None
        self.visited = False

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, h {self.height})"

    def can_visit(self):
        return [
            cell
            for cell in {self.up, self.dn, self.lt, self.rt}
            if cell is not None and not cell.visited and cell.height == self.height + 1
        ]


class Map:
    def __init__(self, lines):
        self.rows = []
        self.rows.extend([Cell(height) for height in line] for line in lines)
        for j in range(len(self.rows)):
            for i in range(len(self.rows[0])):
                self.rows[j][i].x = i
                self.rows[j][i].y = j
                if j > 0:
                    self.rows[j][i].up = self.rows[j - 1][i]
                if j < len(self.rows) - 1:
                    self.rows[j][i].dn = self.rows[j + 1][i]
                if i > 0:
                    self.rows[j][i].lt = self.rows[j][i - 1]
                if i < len(self.rows[0]) - 1:
                    self.rows[j][i].rt = self.rows[j][i + 1]

    def trailheads(self):
        return [cell for row in self.rows for cell in row if cell.height == 0]

    def clear(self):
        for j in range(len(self.rows)):
            for i in range(len(self.rows[0])):
                self.rows[j][i].visited = False

    def score(self):
        res = 0
        for trailhead in self.trailheads():
            summits = set()
            to_visit = {trailhead}
            while to_visit:
                cell = to_visit.pop()
                cell.visited = True
                if cell.height == 9:
                    summits.add(cell)
                for next in cell.can_visit():
                    to_visit.add(next)
            res += len(summits)
            self.clear()
        return res


def find_trails(cell):
    if cell.height == 9:
        return 1
    if len(cell.can_visit()) == 0:
        return 0
    return sum(find_trails(next) for next in cell.can_visit())


def rating(m):
    return sum(find_trails(trailhead) for trailhead in m.trailheads())


if __name__ == "__main__":
    lines = load_strs("inputs/day10.txt")
    m = Map(lines)
    print(f"Part 1: {m.score()}")
    print(f"Part 2: {rating(m)}")

# -- Tests--
fixture = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]


def test_map():
    m = Map(fixture)
    assert len(m.rows) == 8
    c = m.rows[0][0]
    assert c.height == 8
    assert c.lt is None
    assert c.rt.height == 9
    assert c.rt.dn.lt.up == c


def test_trailheads():
    m = Map(fixture)
    assert len(m.trailheads()) == 9


def test_score():
    m = Map(fixture)
    assert m.score() == 36


def test_rating():
    m = Map(fixture)
    assert rating(m) == 81
