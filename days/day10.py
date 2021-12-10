def parse(inp):
    return [line for line in inp.splitlines()]

match_parens = {
    '(': ')',
    '{': '}',
    '<': '>',
    '[': ']'
}

def check_corruption(line):
    parens = []

    for paren in line:
        if paren in match_parens:
            parens.append(paren)
        else:
            last = parens.pop()
            if match_parens[last] != paren:
                return paren

    return parens


def part1(lines):
    paren_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    total_score = 0

    for line in lines:
        check = check_corruption(line)
        if isinstance(check, str):
            total_score += paren_score[check]
    return total_score


def part2(lines):
    paren_score = {'(': 1, '[': 2, '{': 3, '<': 4}
    scores = []

    for line in lines:
        score = 0
        check = check_corruption(line)
        if not isinstance(check, list):
            continue
        for paren in reversed(check):
            score *= 5
            score += paren_score[paren]
        scores.append(score)

    m = len(scores) // 2
    return sorted(scores)[m]
