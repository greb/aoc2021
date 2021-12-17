import re

def parse(inp):
    re_digit = re.compile(r'-?\d+')
    return [int(n) for n in re_digit.findall(inp)]


def find_y_max(yd, yt0, yt1):
    y = 0
    y_max = 0

    while y >= yt0:
        if y <= yt1:
            return y_max
        y += yd
        if y > y_max:
            y_max = y
        yd -= 1

    return None


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
    _, _, yt0, yt1 = target

    y_max = 0

    for yd in range(1000):
        n_y_max = find_y_max(yd, yt0, yt1)
        if n_y_max is None:
            continue
        y_max = n_y_max
        yd += 1

    return y_max


def part2(target):
    target_cnt = 0
    for xd in range(1000):
        for yd in range(-1000, 1000):
            if hit_target(xd, yd, target):
                target_cnt += 1
    return target_cnt


