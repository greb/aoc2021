class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        coord = (self.x, self.y)
        return f'{coord}'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coord(x, y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def is_bounded(self, x_max, y_max, x_min=0, y_min=0):
        bx = x_min <= self.x < x_max
        by = y_min <= self.y < y_max
        return bx and by

    def adjacent(self):
        for d in [N,S,E,W]:
            yield self + d

N = Coord(0, -1)
E = Coord(1, 0)
S = Coord(0, 1)
W = Coord(-1, 0)

