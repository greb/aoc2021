from days.coord import Coord

def parse(inp):
    lines = inp.splitlines()

    enhance = [c == '#' for c in lines[0]]

    cells = set()
    for y, row in enumerate(lines[2:]):
        for x, cell in enumerate(row):
            if cell != '#':
                continue
            cells.add(Coord(x,y))

    return enhance, cells


neighbors = [ (-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0),
        (-1,1),  (0,1),  (1,1)]

def enh_index(coord, cells, alive):
    idx = 0
    for x,y in neighbors:
        c = coord + Coord(x,y)
        idx <<= 1
        b = (c in cells) ^ (not alive)
        idx |= b
    return idx


def step(enhance, cells, alive):
    n_cells = set()
    xs = [c.x for c in cells]
    x_min, x_max = min(xs), max(xs)
    ys = [c.y for c in cells]
    y_min, y_max = min(ys), max(ys)

    for y in range(y_min-1, y_max+2):
        for x in range(x_min-1, x_max+2):
            c = Coord(x,y)
            idx = enh_index(c, cells, alive)
            if enhance[idx] ^ alive:
                n_cells.add(c)
    return n_cells


def solve(enhance, cells, n_iter):
    for it in range(n_iter):
        alive = it % 2 == 0
        cells = step(enhance, cells, alive)
    return len(cells)


def part1(inp):
    enhance, cells = inp
    return solve(enhance, cells, 2)

def part2(inp):
    enhance, cells = inp
    return solve(enhance, cells, 50)
