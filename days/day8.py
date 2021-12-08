import collections
import functools
import itertools

def parse(inp):
    patterns = []

    for line in inp.splitlines():
        signal, output = line.split('|')
        signal = signal.strip().split()
        output = output.strip().split()
        patterns.append((signal, output))
    return patterns

easy_digits = {2:1, 3:7, 4:4, 7:8}

def part1(patterns):
    cnt = 0
    for _, output in patterns:
        for o in output:
            if len(o) in easy_digits:
                cnt += 1
    return cnt

def signal_digits(signal):
    digits = dict()

    for s in signal:
        # Find easy digits
        found = easy_digits.get(len(s))
        if found:
            digits[found] = set(s)

    for s in signal:
        segs = set(s)
        if len(segs) == 5:
            # Find 2,3,5
            if len(segs - digits[4]) == 3:
                digits[2] = segs
            elif len(segs - digits[7]) == 2:
                digits[3] = segs
            else:
                digits[5] = segs
        elif len(segs) == 6:
            # Find 0,6,9
            if len(segs - digits[4]) == 2:
                digits[9] = segs
            elif len(segs - digits[7]) == 4:
                digits[6] = segs
            else:
                digits[0] = segs

    return {frozenset(segs): digit for digit, segs in digits.items()}


def part2(patterns):
    total = 0

    for signal, output in patterns:
        digits = signal_digits(signal)
        o_digits = [digits[frozenset(segs)] for segs in output]

        f = lambda a, b: a*10 + b
        num = functools.reduce(f, o_digits)
        total += num

    return total
