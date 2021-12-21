import functools

def parse(inp):
    lines = inp.splitlines()
    p1 = int(lines[0].split()[-1])
    p2 = int(lines[1].split()[-1])
    return p1, p2

def play(pos1, pos2, score1=0, score2=0, round=0):
    if score2 >= 1000:
        return round*score1

    pos1 = (pos1 + 3*round+6) % 10 or 10
    return play(pos2, pos1, score2, score1+pos1, round+3)


@functools.cache
def play_multi(pos1, pos2, score1=0, score2=0):
    if score2 >= 21:
        return 0, 1

    wins1, wins2 = 0, 0
    for move, n in [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]:
        n_pos1 = (pos1 + move) % 10 or 10
        w2, w1 = play_multi(pos2, n_pos1, score2, score1+n_pos1)
        wins1 += n*w1
        wins2 += n*w2
    return wins1, wins2

def part1(pos):
    pos1, pos2 = pos
    return play(pos1, pos2)


def part2(pos):
    pos1, pos2 = pos
    return max(play_multi(pos1, pos2))
