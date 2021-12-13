from days.coord import Coord

def parse(inp):
    lines = iter(inp.splitlines())
    dots = set()
    folds = []

    while line := next(lines):
        args = [int(n) for n in line.split(',')]
        dot = Coord(*args)
        dots.add(dot)

    while line := next(lines, None):
        lhs, n = line.split('=')
        dim = lhs[-1]
        fold = dim, int(n)
        folds.append(fold)

    return dots, folds

def fold(dots, dim, i):
    new_dots = set()
    for dot in dots:
        if dot[dim] > i:
            dot[dim] = i - (dot[dim] - i)
        new_dots.add(dot)
    return new_dots


def part1(inp):
    dots, folds = inp

    dim, i = folds[0]
    dots = fold(dots, dim, i)
    return len(dots)


def part2(inp):
    dots, folds = inp
    for dim, i in folds:
        dots = fold(dots, dim, i)

    max_x = max(dot['x'] for dot in dots)
    max_y = max(dot['y'] for dot in dots)

    for y in range(max_y+1):
        row = [' ░'[Coord(x,y) in dots] for x in range(max_x+1)]
        print(''.join(row))

    return 'look at output'
