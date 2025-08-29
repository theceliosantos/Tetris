import pygame
import sys
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris - Menu")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 50)
    small_font = pygame.font.SysFont("Arial", 36)

    selected = 0  # opção selecionada (0 = Start, 1 = Quit)
    options = ["Start", "Quit"]

    while True:
        screen.fill(BLACK)

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Start
                        game = Game()
                        game.run()
                    elif selected == 1:  # Quit
                        pygame.quit()
                        sys.exit()

        # desenha título
        title_surface = font.render("TETRIS", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 100))

        # desenha opções
        for i, option in enumerate(options):
            color = WHITE
            if i == selected:
                color = (255, 0, 0)  # opção selecionada em vermelho
            option_surface = small_font.render(option, True, color)
            screen.blit(option_surface, (SCREEN_WIDTH//2 - option_surface.get_width()//2, 250 + i*60))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()