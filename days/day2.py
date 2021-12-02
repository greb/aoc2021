def parse(inp):
    commands = []

    for line in inp.splitlines():
        direction, val = line.split()
        commands.append( (direction, int(val)))

    return commands

def part1(commands):
    x,y = 0, 0

    for direction, val in commands:
        if direction == 'forward':
            x += val
        elif direction == 'down':
            y += val
        elif direction == 'up':
            y -= val

    return x*y


def part2(commands):
    x,y,aim = 0, 0, 0

    for direction, val in commands:
        if direction == 'down':
            aim += val
        elif direction == 'up':
            aim -= val
        elif direction == 'forward':
            x += val
            y += aim*val

    return x*y

