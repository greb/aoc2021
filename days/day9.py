import math
import collections

from days.coord import Coord

def parse(inp):
    heightmap = dict()
    for y, line in enumerate(inp.splitlines()):
        row = [int(ch) for ch in line]
        for x, h in enumerate(row):
            c = Coord(x, y)
            heightmap[c] = h

    neighbors = collections.defaultdict(list)
    for c in heightmap.keys():
        for n in c.adjacent():
            if n in heightmap:
                neighbors[c].append(n)

    return heightmap, neighbors


def find_low_points(heightmap, neighbors):
    low_points = []
    for c, height in heightmap.items():
        if all(heightmap[n] > height for n in neighbors[c]):
            low_points.append(c)
    return low_points


def part1(inp):
    heightmap, neighbors = inp
    low_points = find_low_points(heightmap, neighbors)

    total_risk = sum(heightmap[p] + 1 for p in low_points)
    return total_risk


def part2(inp):
    heightmap, neighbors = inp
    low_points = find_low_points(heightmap, neighbors)

    basins = []
    for low_point in low_points:
        queue = collections.deque()
        queue.append(low_point)
        visited = set()
        visited.add(low_point)

        while queue:
            point = queue.popleft()
            for n_point in neighbors[point]:
                if n_point not in visited and heightmap[n_point] < 9:
                    queue.append(n_point)
                    visited.add(n_point)

        basins.append(len(visited))

    return math.prod(sorted(basins)[-3:])

