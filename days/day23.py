import collections
import heapq

from days.coord import Coord

room_colors = {
    2:'A', 4:'B', 6:'C', 8:'D',
}
move_cost = {'A':1, 'B': 10, 'C':100, 'D':1000}

def parse(inp):
    burrow = dict()
    for y, row in enumerate(inp.splitlines()):
        for x, tile in enumerate(row):
            if tile == '.':
                burrow[Coord(x-1,y-1)] = None
            elif tile in move_cost:
                burrow[Coord(x-1,y-1)] = tile
    return burrow

def map_neighborhood(burrow):
    neighbors = collections.defaultdict(list)
    for pos in burrow:
        for n in pos.adjacent():
            if n not in burrow:
                continue
            neighbors[pos].append(n)
    return neighbors

def hash_burrow(burrow):
    tiles = [burrow[p] for p in sorted(burrow.keys())]
    return hash(tuple(tiles))

def moves(burrow, neighbors):
    for move_pos, color in burrow.items():
        if not color:
            continue

        passed_hall = False
        moves = []
        stack = [(0, move_pos)]
        visited = set()
        while stack:
            dist, pos = stack.pop()
            if pos in visited:
                continue
            visited.add(pos)

            if pos.y > 0:
                if passed_hall:
                    below = Coord(pos.x, pos.y+1)
                    if below not in burrow or burrow[below] == color:
                        moves.append((dist, pos))
            else:
                passed_hall = True
                if pos.x not in room_colors:
                    moves.append((dist, pos))

            for n in neighbors[pos]:
                # Already occupied
                if burrow[n]:
                    continue
                # Only visit correct rooms
                if passed_hall and n.y > 0 and color != room_colors[n.x]:
                    continue
                stack.append((dist+1, n))

        for dist, pos in moves:
            if dist == 0:
                continue
            n_burrow = burrow.copy()
            n_burrow[move_pos] = None
            n_burrow[pos] = color
            cost = move_cost[color] * dist
            yield cost, n_burrow

def check_burrow(burrow):
    for pos, color in burrow.items():
        if not color:
            continue

        if pos.y == 0:
            return False

        if room_colors[pos.x] != color:
            return False
    return True

def solve(burrow):
    neighbors = map_neighborhood(burrow)

    h = hash_burrow(burrow)
    costs = dict({h: 0})
    queue = [(0, h, burrow)]
    seen = set()

    while queue:
        cost, h, burrow = heapq.heappop(queue)
        if h in seen:
            continue
        seen.add(h)

        if check_burrow(burrow):
            return cost

        for move_cost, move_burrow in moves(burrow, neighbors):
            h = hash_burrow(move_burrow)
            new_cost = cost + move_cost
            old_cost = costs.get(h)

            if not old_cost or new_cost <= old_cost:
                costs[h] = new_cost
                heapq.heappush(queue, (new_cost, h, move_burrow))

def part1(burrow):
    return solve(burrow)


def part2(burrow):
    new_burrow = dict()
    for pos, tile in burrow.items():
        if tile and pos.y == 2:
            new_burrow[Coord(pos.x, pos.y+2)] = tile
        else:
            new_burrow[pos] = tile

    new_burrow.update({
        Coord(2,2): 'D', Coord(2,3): 'D', Coord(4,2): 'C', Coord(4,3): 'B',
        Coord(6,2): 'B', Coord(6,3): 'A', Coord(8,2): 'A', Coord(8,3): 'C'
    })

    return solve(new_burrow)
