import re

def parse(inp):
    re_digit = re.compile(r'-?\d+')
    return [int(n) for n in re_digit.findall(inp)]


def hit_target(xd, yd, target):
    xt0, xt1, yt0, yt1 = target
    x, y = 0,0

    while x <= xt1 and y >= yt0:
        if x >= xt0 and y <= yt1:
            return True

        x += xd
        y += yd

        if xd > 0:
            xd -= 1
        yd -= 1

    return False


def part1(target):
    _, _, yt0, _ = target
    return yt0*(yt0+1) // 2


def part2(target):
    target_cnt = 0
    _, xt1, yt0, _ = target

    for xd in range(1, xt1+1):
        for yd in range(yt0, -yt0):
            if hit_target(xd, yd, target):
                target_cnt += 1
    return target_cnt


