import collections
import pprint as pp

def parse(inp):
    lines = inp.splitlines()

    template = lines[0]
    pair_counts = collections.defaultdict(int)
    for pair in zip(template, template[1:]):
        pair_counts[pair] += 1
    # Add trail pair to make counting elments easier
    trail_elem = template[-1]
    pair_counts[(trail_elem, None)] = 1

    rules = dict()
    for line in lines[2:]:
        lhs, rhs = line.split(' -> ')
        rules[tuple(lhs)] = rhs

    return pair_counts, rules

def step(pair_counts, rules):
    n_pair_counts = collections.defaultdict(int)

    for (r, l), count in pair_counts.items():
        c = rules.get((r, l))
        if not c:
            n_pair_counts[(r,l)] = count
            continue
        n_pair_counts[(r, c)] += count
        n_pair_counts[(c, l)] += count

    return n_pair_counts

def solve(n, pair_counts, rules):
    for _ in range(n):
        pair_counts = step(pair_counts, rules)

    elem_counts = collections.defaultdict(int)
    for (r, l), count in pair_counts.items():
        elem_counts[r] += count

    max_elem = max(elem_counts.values())
    min_elem = min(elem_counts.values())
    return max_elem - min_elem


def part1(inp):
    pair_counts, rules = inp
    return solve(10, pair_counts, rules)

def part2(inp):
    pair_counts, rules = inp
    return solve(40, pair_counts, rules)
