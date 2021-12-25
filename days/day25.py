def parse(inp):
    horiz = set()
    vert  = set()
    lines = inp.splitlines()
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c == '>':
                horiz.add((x,y))
            elif c == 'v':
                vert.add((x,y))
    w, h = len(lines[0]), len(lines)
    return horiz, vert, w, h

def step(cucumbers, w, h):
    horiz, vert = cucumbers
    cnt = 0

    n_horiz = set()
    for x, y in horiz:
        c = (x+1) % w, y
        if c in horiz or c in vert:
            n_horiz.add((x,y))
        else:
            cnt += 1
            n_horiz.add(c)

    n_vert = set()
    for x, y in vert:
        c = x, (y+1) % h
        if c in n_horiz or c in vert:
            n_vert.add((x,y))
        else:
            cnt += 1
            n_vert.add(c)

    return cnt, n_horiz, n_vert

def print_cucumbers(cucumbers, w, h):
    horiz, vert = cucumbers
    for y in range(h):
        row = []
        for x in range(w):
            if (x,y) in horiz:
                row.append('>')
            elif (x,y) in vert:
                row.append('v')
            else:
                row.append('.')
        print(''.join(row))


def part1(grid):
    *cucumbers, w, h = grid

    i = 0
    while True:
        cnt, *cucumbers = step(cucumbers, w, h)
        i += 1
        if not cnt:
            break
    return i
