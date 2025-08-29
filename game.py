import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, FPS, BLACK, SIDE_PANEL_WIDTH
from board import Board
from tetris import Tetris
from utils import load_sounds, draw_centered_text


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=128)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_piece = Tetris(0, 0)
        self.next_piece = Tetris(0, 0)
        self.spawn_piece()
        self.game_over = False
        self.paused = False
        self.score = 0
        self.flash_timer = 0

        # Sons
        self.sounds, self.channels = load_sounds()
        pygame.mixer.music.load("sounds/bgm.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def spawn_piece(self):
        if hasattr(self, "next_piece"):
            self.current_piece = self.next_piece
        self.next_piece = Tetris(0, 0)
        self.current_piece.x = self.board.cols // 2 - len(self.current_piece.shape[0]) // 2
        self.current_piece.y = 0
        if not self.board.is_valid_position(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if not self.paused and not self.game_over:
                    moved = False
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        if self.board.is_valid_position(self.current_piece.shape, self.current_piece.x - 1, self.current_piece.y):
                            self.current_piece.x -= 1
                            moved = True
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        if self.board.is_valid_position(self.current_piece.shape, self.current_piece.x + 1, self.current_piece.y):
                            self.current_piece.x += 1
                            moved = True
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        if self.board.is_valid_position(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                            moved = True
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        old_shape = self.current_piece.shape
                        self.current_piece.rotate()
                        if not self.board.is_valid_position(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
                            self.current_piece.shape = old_shape
                        else:
                            moved = True
                    elif event.key == pygame.K_SPACE:
                        while self.board.is_valid_position(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                        self.channels["drop"].play(self.sounds["drop"])
                        self.lock_piece()

                    if moved:
                        self.channels["move"].play(self.sounds["move"])
                if self.game_over and event.key == pygame.K_RETURN:
                    return True
        return False

    def lock_piece(self):
        self.board.add_piece(self.current_piece)
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.channels["line"].play(self.sounds["line"])
            self.flash_timer = 5
        self.spawn_piece()

    def update(self):
        if not self.paused and not self.game_over:
            if self.board.is_valid_position(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1):
                self.current_piece.y += 1
            else:
                self.lock_piece()

    def draw(self):
        bg_color = (255, 255, 255) if self.flash_timer > 0 else BLACK
        if self.flash_timer > 0:
            self.flash_timer -= 1
        self.screen.fill(bg_color)

        # tabuleiro
        for y, row in enumerate(self.board.grid):
            for x, color in enumerate(row):
                draw_color = bg_color if self.flash_timer > 0 else color
                pygame.draw.rect(
                    self.screen, draw_color,
                    ((x * BLOCK_SIZE) + SIDE_PANEL_WIDTH, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(
                    self.screen, (50, 50, 50),
                    ((x * BLOCK_SIZE) + SIDE_PANEL_WIDTH, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1
                )

        # peça atual
        offset_x = SIDE_PANEL_WIDTH
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    draw_color = bg_color if self.flash_timer > 0 else self.current_piece.color
                    pygame.draw.rect(
                        self.screen, draw_color,
                        ((self.current_piece.x + j) * BLOCK_SIZE + offset_x,
                         (self.current_piece.y + i) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen, (50, 50, 50),
                        ((self.current_piece.x + j) * BLOCK_SIZE + offset_x,
                         (self.current_piece.y + i) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE), 1
                    )

        self.draw_sidebar()

        if self.paused:
            draw_centered_text(self.screen, "PAUSE", 50, (255, 255, 0))
        if self.game_over:
            draw_centered_text(self.screen, "GAME OVER", 50, (255, 0, 0))
            draw_centered_text(self.screen, "Press ENTER to return to menu", 30, (255, 255, 255), y_offset=60)

        pygame.display.flip()

    def draw_sidebar(self):
        font = pygame.font.SysFont('Arial', 24)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (20, 20))

        label = font.render('Next:', True, (255, 255, 255))
        self.screen.blit(label, (20, 80))

        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen, self.next_piece.color,
                        (20 + j * BLOCK_SIZE, 110 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen, (50, 50, 50),
                        (20 + j * BLOCK_SIZE, 110 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1
                    )

    def run(self):
        while True:
            go_to_menu = self.handle_events()
            if go_to_menu:
                return
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(FPS)
