import random
from settings import COLORS

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "Z": [[1, 1, 0], [0, 1, 1]],
}


class Tetris:
    def __init__(self, x, y):
        self.shape = random.choice(list(SHAPES.values()))
        self.color = random.choice(COLORS)
        self.x = x
        self.y = y

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
