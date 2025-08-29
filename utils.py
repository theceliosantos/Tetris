import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

def draw_text(surface, text, size, x, y, color=WHITE, center=False):
    """Desenha texto na tela em (x, y)."""
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_centered_text(surface, text, size, color, y_offset=0):
    """Desenha texto centralizado no meio da tela (com deslocamento opcional)."""
    font = pygame.font.SysFont('Arial', size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(surf, rect)

def load_sounds():
    """Carrega sons e retorna (sons, canais)."""
    sounds = {
        "move": pygame.mixer.Sound("sounds/move.wav"),
        "drop": pygame.mixer.Sound("sounds/drop.wav"),
        "line": pygame.mixer.Sound("sounds/line.wav"),
    }
    channels = {
        "move": pygame.mixer.Channel(0),
        "drop": pygame.mixer.Channel(1),
        "line": pygame.mixer.Channel(2),
    }
    return sounds, channels
