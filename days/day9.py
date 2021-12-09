import math

def parse(inp):
    heightmap = []
    for line in inp.splitlines():
        row = [int(ch) for ch in line]
        heightmap.append(row)
    return heightmap


def neighbors(hm, x, y, w, h):
    d = [(1,0), (-1,0), (0,1), (0,-1)]

    for dx, dy in d:
        nx = x+dx
        ny = y+dy

        if 0 <= nx < w and 0 <= ny < h:
            yield hm[ny][nx], nx, ny


def is_low_point(height, ns):
    return all(height < n[0] for n in ns)


def part1(heightmap):
    w, h = len(heightmap[0]), len(heightmap)
    risks = []

    for y in range(h):
        for x in range(w):
            ns = neighbors(heightmap, x, y, w, h)
            height = heightmap[y][x]

            if is_low_point(height, ns):
                risks.append(height+1)

    return sum(risks)

def part2(heightmap):
    w, h = len(heightmap[0]), len(heightmap)
    low_points = []

    for y in range(h):
        for x in range(w):
            ns = neighbors(heightmap, x, y, w, h)
            height = heightmap[y][x]

            if is_low_point(height, ns):
                low_points.append((x,y))

    basins = []
    for low_point in low_points:
        visited = set()
        unvisited = [low_point]

        while unvisited:
            x, y = unvisited.pop()
            visited.add((x,y))

            ns = neighbors(heightmap, x, y, w, h)
            for n_height, nx, ny in ns:
                if (nx, ny) in visited:
                    continue
                if n_height == 9:
                    continue
                unvisited.append((nx, ny))

        basins.append(len(visited))

    basins = sorted(basins)[-3:]
    return math.prod(basins)

