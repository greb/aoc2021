import functools
import itertools

def parse(inp):
    numbers = []
    for line in inp.splitlines():
        numbers.append(parse_number(line))
    return numbers

def parse_number(s):
    stack = []
    for c in s:
        if c == ',':
            continue
        elif c == '[':
            stack.append(list())
        elif c == ']':
            rhs = stack.pop()
            if stack:
               stack[-1].append(rhs)
            else:
                return rhs
        else:
            stack[-1].append(int(c))

def add_left(num, n):
    if n is None:
        return num
    if isinstance(num, int):
        return num + n

    left, right = num
    return [add_left(left, n), right]

def add_right(num, n):
    if n is None:
        return num
    if isinstance(num, int):
        return num + n

    left, right = num
    return [left, add_right(right, n)]


def explode(num, depth=0):
    if isinstance(num, int):
        return False, None, num, None

    left, right = num
    if depth == 4:
        return True, left, 0, right

    enump, enump_l, left, enump_r = explode(left, depth + 1)
    if enump:
        return enump, enump_l, [left, add_left(right, enump_r)], None

    enump, enump_l, right, enump_r = explode(right, depth + 1)
    if enump:
        return enump, None, [add_right(left, enump_l), right], enump_r

    return False, None, num, None

def split(num):
    if isinstance(num, int):
        if num >= 10:
            n0 = num // 2
            n1 = num - n0
            return True, [n0, n1]
        return False, num

    left, right = num
    sp, left = split(left)
    if sp:
        return sp, [left, right]
    sp, right = split(right)
    return sp, [left, right]

def add(a, b):
    num = [a,b]
    changed = True
    while changed:
        changed, _, num, _ = explode(num)
        if changed:
            continue
        changed, num = split(num)
    return num

def magnitude(num):
    if isinstance(num, int):
        return num
    left, right = num
    return 3*magnitude(left) + 2*magnitude(right)


def part1(numbers):
    num = functools.reduce(add, numbers)
    return magnitude(num)


def part2(numbers):
    perms = itertools.permutations(numbers, 2)
    return max(magnitude(add(a,b)) for a, b in perms)
