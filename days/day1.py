def parse(inp):
    depths = list(map(int, inp.splitlines()))
    return depths

def part1(depths):
    cnt = sum(b > a for (a, b) in zip(depths, depths[1:]))
    return cnt


def part2(depths):
    cnt = sum(b > a for (a, b) in zip(depths, depths[3:]))
    return cnt

