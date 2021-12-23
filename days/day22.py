import re
import collections

def parse(inp):
    cube_re = re.compile(r'-?\d+')
    steps = []
    for line in inp.splitlines():
        status, cube = line.split()
        is_on = status == 'on'
        x0,x1, y0,y1, z0,z1 = (int(n) for n in cube_re.findall(cube))
        cube = (x0,x1), (y0,y1), (z0, z1)
        steps.append((is_on, cube))
    return steps

def intersect(cube1, cube2):
    int_cube = []
    for a, b in zip(cube1, cube2):
        c = (max(a[0], b[0]), min(a[1], b[1]))
        if c[0] > c[1]:
            return None
        int_cube.append(c)
    return tuple(int_cube)


def cube_size(cube):
    size = 1
    for a, b in cube:
        size *= b-a+1
    return size

def count_cubicles(steps):
    count = 0

    counted_cubes = []
    for is_on, cube in reversed(steps):
        if is_on:
            int_steps = []
            for cnt_cube in counted_cubes:
                int_cube = intersect(cube, cnt_cube)
                if int_cube:
                    int_steps.append((True, int_cube))
            count += cube_size(cube)
            count -= count_cubicles(int_steps)
        counted_cubes.append(cube)
    return count

def part1(steps):
    N = 50
    region = ((-N, N), (-N, N), (-N, N))

    clipped = []
    for status, cube in steps:
        int_cube = intersect(cube, region)
        if not int_cube:
            continue
        clipped.append((status, int_cube))
    return count_cubicles(clipped)

def part2(steps):
    return count_cubicles(steps)
