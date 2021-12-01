def parse(inp):
    depths = list(map(int, inp.splitlines()))
    return depths

def part1(inp):
    depths = parse(inp)

    cnt = 0
    for (a, b) in zip(depths, depths[1:]):
        if b > a:
            cnt += 1
    return cnt


def part2(inp):
    depths = parse(inp)

    windows = list(map(sum, zip(depths, depths[1:], depths[2:])))

    cnt = 0
    for (a,b) in zip(windows, windows[1:]):
        if b > a:
            cnt += 1
    return cnt

