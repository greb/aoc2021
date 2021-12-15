import collections
import heapq
import itertools

from days.coord import Coord

def parse(inp):
    risk_map = dict()

    lines = inp.splitlines()
    for y, line in enumerate(lines):
        for x, risk in enumerate(line):
            c = Coord(x, y)
            risk_map[c] = int(risk)

    w, h = len(lines[0]), len(lines)
    return risk_map, w, h


def shortest_path(risk_map, start, end):
    dists = {start: 0}
    queue = [(0, start)]

    while queue:
        _, curr = heapq.heappop(queue)
        if curr == end:
            break

        curr_dist = dists[curr]
        for n in curr.adjacent():
            if n not in risk_map:
                continue
            n_dist = curr_dist + risk_map[n]
            old_dist = dists.get(n)
            if old_dist is None or n_dist < old_dist:
                h = end.manhatten_dist(n)
                dists[n] = n_dist
                heapq.heappush(queue, (n_dist, n))

    return dists[end]


def part1(inp):
    risk_map, w, h = inp

    start = Coord(0,0)
    end = Coord(w-1, h-1)
    return shortest_path(risk_map, start, end)


def part2(inp):
    size = 5
    risk_map, w, h = inp

    for c, risk in list(risk_map.items()):
        for tile_x, tile_y in itertools.product(list(range(size)), repeat=2):
            x = tile_x * w + c.x
            y = tile_y * h + c.y
            r = risk + tile_x + tile_y
            r = ((r-1) % 9) + 1
            risk_map[Coord(x,y)] = r

    start = Coord(0,0)
    end = Coord(size*w-1, size*h-1)
    return shortest_path(risk_map, start, end)
