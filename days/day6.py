import functools

def parse(inp):
    return [int(t) for t in inp.strip().split(',')]


@functools.cache
def count_fish(fish, days):
    if days < fish:
        return 1

    # Wait until fish is ready to duplicate
    days -= fish

    n_fish = 1
    while days > 0:
        n_fish += count_fish(8, days-1)
        days -= 7
    return n_fish


def part1(fishes):
    days = 80

    n_fish = 0
    for fish in fishes:
        n_fish += count_fish(fish, days)
    return n_fish


def part2(fishes):
    days = 256

    n_fish = 0
    for fish in fishes:
        n_fish += count_fish(fish, days)
    return n_fish

