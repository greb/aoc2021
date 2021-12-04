import itertools

from termcolor import colored

board_size = 5

def parse(inp):
    lines = inp.splitlines()

    nums = [int(n) for n in lines[0].split(',')]

    boards = []
    for i in range(2, len(lines), board_size+1):
        board_lines = lines[i:i+board_size]
        board = [int(n) for line in board_lines for n in line.split()]
        boards.append(board)

    return nums, boards


class Board:
    def __init__(self, nums):
        self.nums = nums
        self.marks = [0]*len(nums)

    def __repr__(self):
        output = []
        for num, mark in zip(self.nums, self.marks):
            num = str(num)
            if mark:
                num = colored(num, 'red')
            output.append(num)
        return ' '.join(output)

    def mark(self, num):
        for i, board_num in enumerate(self.nums):
            if board_num == num:
                self.marks[i] = 1

    def is_bingo(self):
        vals = zip(self.nums, self.marks)
        rows = list(zip(*([vals]*board_size)))
        cols = list(zip(*rows))

        for vals in itertools.chain(rows, cols):
            if all(v[1] for v in vals):
                return True

        return False

    def score(self):
        vals = zip(self.nums, self.marks)
        return sum(v[0] for v in vals if not v[1])


def part1(inp):
    nums, boards = inp
    boards = [Board(board) for board in boards]

    for num in nums:
        for board in boards:
            board.mark(num)
            if board.is_bingo():
                return num * board.score()


def part2(inp):
    nums, boards = inp
    boards = set([Board(board) for board in boards])

    for num in nums:
        for board in list(boards):
            board.mark(num)

            if board.is_bingo():
                if len(boards) == 1:
                    return num * board.score()
                else:
                    boards.remove(board)

