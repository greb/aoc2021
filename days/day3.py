def parse(inp):
    lines = inp.splitlines()
    width = len(lines[0])
    nums = [int(n, 2) for n in lines]

    return width, nums


def part1(inp):
    width, nums = inp
    n_nums = len(nums)

    gamma = epsilon =  0
    for pos in reversed(range(width)):
        digits = [n & (1 << pos) for n in nums]
        zeros = digits.count(0)

        digit = zeros < (n_nums // 2)
        gamma = (gamma << 1) | digit
        epsilon = (epsilon << 1) | (not digit)

    return gamma * epsilon


def part2(inp):
    width, nums = inp

    valid_nums = list(nums)
    for pos in reversed(range(width)):
        if len(valid_nums) == 1:
            break

        digits = [n & (1 << pos) for n in valid_nums]
        zeros = digits.count(0)

        digit = zeros <= (len(valid_nums) // 2)

        valid_nums = [n for n in valid_nums if
                bool(n & (1 << pos)) == digit]
    gamma = valid_nums[0]

    valid_nums = list(nums)
    for pos in reversed(range(width)):
        if len(valid_nums) == 1:
            break

        digits = [n & (1 << pos) for n in valid_nums]
        zeros = digits.count(0)

        digit = zeros <= (len(valid_nums) // 2)

        valid_nums = [n for n in valid_nums if
                bool(n & (1 << pos)) != digit]
    epsilon = valid_nums[0]

    return gamma * epsilon
