import pygame
from settings import BLOCK_SIZE, COLS, ROWS, BLACK, SIDE_PANEL_WIDTH

class Board:
    def __init__(self):
        self.cols = COLS
        self.rows = ROWS
        self.grid = [[BLACK for _ in range(self.cols)] for _ in range(self.rows)]

    def is_valid_position(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    nx = x + j
                    ny = y + i
                    # limites horizontais e inferior
                    if nx < 0 or nx >= self.cols or ny >= self.rows:
                        return False
                    # colisão com peça já fixa
                    if ny >= 0 and self.grid[ny][nx] != BLACK:
                        return False
        return True

    def add_piece(self, piece):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    nx = piece.x + j
                    ny = piece.y + i
                    if 0 <= nx < self.cols and 0 <= ny < self.rows:
                        self.grid[ny][nx] = piece.color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = self.rows - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [BLACK for _ in range(self.cols)])
        self.grid = new_grid
        return lines_cleared

    def draw(self, screen):
        offset_x = SIDE_PANEL_WIDTH
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(
                    screen,
                    color,
                    ((x * BLOCK_SIZE) + offset_x, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    screen,
                    (50, 50, 50),
                    ((x * BLOCK_SIZE) + offset_x, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )
