import itertools

'''
All instruction blocks have the same format:

 0: mul x 0
 1: add x z
 2: mod x 26
 3: div z {a} # 1 or 26
 4: add x {b} # positive when a==1 else negative
 5: eql x w
 6: eql x 0
 7: mul y 0
 8: add y 25
 9: mul y x
10: add y 1
11: mul z y
12: mul y 0
13: add y w
14: add y {c}
15: mul y x
16: add z y

Let's reverse engineer those instructions:

 2: x = z % 26
 3: z = z // {a}
 4: x = x + {b}
 6: x = x != w       # 0 or 1
10: y = 25 * x + 1   # 1 or 26
11: z = z*y
14: y = w + {c}
15: y = y*x
16: z = z+y

Simplify:

x = (z % 26) + b != w  # (2,4,6)
z = z // a             # (3)
z *= 25 * x + 1        # (10,11)
z += (w+c) * x         # (14,15,16)

'''

def parse(inp):
    blocks = []
    block = []
    for line in inp.splitlines():
        if line.startswith('inp'):
            if block:
                blocks.append(block)
            block = []
        else:
            block.append(line.split())
    blocks.append(block)

    digit_deltas = {}
    z_stack = [] # number in base 26
    for i, block in enumerate(blocks):
        check = int(block[4][2])
        offset = int(block[14][2])
        if check > 0:
            z_stack.append((i, offset))
        else:
            j, offset = z_stack.pop()
            digit_deltas[i] = (j, offset + check)
    return digit_deltas

def part1(digit_deltas):
    digits = [0] * 14
    for i, (j, delta) in digit_deltas.items():
        digits[i] = min(9, 9 + delta)
        digits[j] = min(9, 9 - delta)
    return ''.join(map(str, digits))

def part2(digit_deltas):
    digits = [0] * 14
    for i, (j, delta) in digit_deltas.items():
        digits[i] = max(1, 1 + delta)
        digits[j] = max(1, 1 - delta)
    return ''.join(map(str, digits))

