import re
import collections

def parse(inp):
    segments = []

    pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
    for line in inp.splitlines():
        m = pattern.match(line)
        coords  = [int(n) for n in m.groups()]
        segments.append(coords)

    return segments


def part1(inp):
    return count_crossings(inp, False)

def part2(inp):
    return count_crossings(inp, True)

def count_crossings(segments, diagonals):
    points = collections.defaultdict(int)

    for x1,y1,x2,y2 in segments:
        dx = x2 - x1
        dy = y2 - y1

        if not diagonals and dx and dy:
            continue

        if dx != 0:
            dx //= abs(dx)
        if dy != 0:
            dy //= abs(dy)

        while (x1,y1) != (x2, y2):
            points[(x1,y1)] += 1
            x1 += dx
            y1 += dy
        points[(x1,y1)] += 1

    return len([p for p in points.values() if p >= 2])
