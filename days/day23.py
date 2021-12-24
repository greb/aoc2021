import collections
import heapq

from days.coord import Coord

move_costs = {'A':1, 'B': 10, 'C':100, 'D':1000}
pos_to_room = {2: 'A', 4: 'B', 6:'C', 8:'D'}
room_to_pos = {'A':2, 'B':4, 'C':6, 'D':8}

empty = '_'

LEN_HALL = 11

def parse(inp):
    rooms = collections.defaultdict(list)
    for row in inp.splitlines()[2:-1]:
        for x, tile in enumerate(row):
            r = pos_to_room.get(x-1)
            if r: rooms[r].append(tile)
    return rooms

def reachable(a, b, hall):
    if a < b:
        hall = hall[a+1:b+1]
    else:
        hall = hall[b:a]
    if not any(h != empty for h in hall):
        return abs(a-b)

def moves_down(state):
    # move any shrimp to correct room if possible
    hall, rooms = state
    for x, shrimp in enumerate(hall):
        # Can move in front of room?
        room_x = room_to_pos.get(shrimp)
        if not room_x:
            continue
        dist = reachable(x, room_x, hall)
        if not dist:
            continue

        # Has room space left?
        n_rooms = dict(rooms)
        n_room = list(n_rooms[shrimp])
        for y, s in reversed(list(enumerate(n_room))):
            if s == empty:
                break
            if s != shrimp:
                y = None
                break
        if y is None: continue
        dist += y+1

        # Move shrimp
        n_hall = list(hall)
        n_hall[x] = empty
        n_room[y] = shrimp
        n_rooms[shrimp] = tuple(n_room)

        cost = move_costs[shrimp] * dist
        yield cost, (tuple(n_hall), tuple(n_rooms.items()))

def moves_up(state):
    # Move available shrips from their starting room to the hall
    hall, rooms = state
    for r, room in rooms:
        # Take first available shrimp
        for y, shrimp in enumerate(room):
            if shrimp != empty:
                break
        else:
            continue
        dist = y+1

        # Search for available spots
        for x in range(LEN_HALL):
            if hall[x] != empty or x in pos_to_room:
                continue
            hall_dist = reachable(room_to_pos[r], x, hall)
            if not hall_dist:
                continue

            # Move shrimp
            n_hall = list(hall)
            n_hall[x] = shrimp
            n_rooms = dict(rooms)
            n_room = list(room)
            n_room[y] = empty
            n_rooms[r] = tuple(n_room)

            cost = move_costs[shrimp] * (dist + hall_dist)
            yield cost, (tuple(n_hall), tuple(n_rooms.items()))

def moves(state):
    yield from moves_down(state)
    yield from moves_up(state)

def check_rooms(rooms):
    for shrimp, room in rooms:
        if any(s != shrimp for s in room):
            return False
    return True

def solve(rooms):
    hall = tuple([empty]*LEN_HALL)
    start = hall, rooms

    costs = dict()
    costs[start] = 0

    queue = [(0, start)]
    while queue:
        _, node = heapq.heappop(queue)
        cost = costs[node]

        _, rooms = node
        if check_rooms(rooms):
            return cost

        for move_cost, move_node in moves(node):
            new_cost = cost + move_cost
            if move_node not in costs or new_cost < costs[move_node]:
                costs[move_node] = new_cost
                heapq.heappush(queue, (new_cost, move_node))

def part1(rooms):
    rooms = tuple( (k, tuple(v)) for k,v in rooms.items())
    return solve(rooms)

def part2(rooms):
    fold = {'A': ['D', 'D'], 'B': ['C', 'B'],
            'C': ['B', 'A'], 'D': ['A', 'C']}
    n_rooms = dict()
    for r, room in rooms.items():
        n_room = [room[0]] + fold[r] + [room[1]]
        n_rooms[r] = n_room
    n_rooms = tuple( (k, tuple(v)) for k,v in n_rooms.items())

    return solve(n_rooms)
