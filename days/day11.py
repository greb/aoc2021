from days.coord import Coord

GRID_SIZE = 10

def parse(inp):
    return [[int(n) for n in line] for line in inp.splitlines()]


def step(grid):
    grid = [[n+1 for n in row] for row in grid]

    flashes = set()
    flash_stack = []
    for y, row in enumerate(grid):
        for x, n in enumerate(row):
            if n > 9:
                c = Coord(x,y)
                flashes.add(c)
                flash_stack.append(c)

    while flash_stack:
        c = flash_stack.pop()
        for n in c.adjecant8():
            if not n.is_bounded(GRID_SIZE, GRID_SIZE):
                continue
            if n in flashes:
                continue
            grid[n.y][n.x] += 1
            if grid[n.y][n.x] > 9:
                flashes.add(n)
                flash_stack.append(n)

    for f in flashes:
        grid[f.y][f.x] = 0

    return grid, len(flashes)


def part1(grid):
    n_total = 0

    for _ in range(100):
        grid, n_flashes = step(grid)
        n_total += n_flashes

    return n_total


def part2(grid):
    i = 1 
    while True:
        grid, n_flashes = step(grid)
        if n_flashes == GRID_SIZE*GRID_SIZE:
            break
        i += 1
    return i

