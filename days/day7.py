def parse(inp):
    return [int(n) for n in inp.strip().split(',')]


def solve(crabs, cost_func):
    min_fuel = None

    for pos in range(0, max(crabs) + 1):
        fuel = 0
        for c in crabs:
            fuel += cost_func(abs(c - pos))
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel

    return min_fuel


def part1(crabs):
    fuel_cost = lambda n: n
    return solve(crabs, fuel_cost)


def part2(crabs):
    fuel_cost = lambda n: (n*(n+1)) // 2 # Triangle numbers
    return solve(crabs, fuel_cost)
