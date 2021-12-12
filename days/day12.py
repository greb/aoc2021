import collections

def parse(inp):
    connections = [line.split('-') for line in inp.splitlines()]

    edges = collections.defaultdict(list)
    for vert_a, vert_b in connections:
        edges[vert_a].append(vert_b)
        edges[vert_b].append(vert_a)
    return edges

def count_paths(edges, vert, dup_allowed, visited=set()):
    if vert == 'end':
        return 1

    if vert.islower():
        if vert in visited:
            if dup_allowed:
                dup_allowed = False
            else:
                return 0

        visited = visited.copy()
        visited.add(vert)

    n = 0
    for n_vert in edges[vert]:
        if n_vert == 'start':
            continue
        n += count_paths(edges, n_vert, dup_allowed, visited)

    return n

def part1(edges):
    return count_paths(edges, 'start', False)

def part2(edges):
    return count_paths(edges, 'start', True)
