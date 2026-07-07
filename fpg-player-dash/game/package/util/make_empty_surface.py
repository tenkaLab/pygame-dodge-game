import pygame

from game.config import paths


def make_empty_surface() -> pygame.Surface:
    try:
        surface = pygame.image.load(paths.PACKAGE_ASSET_DIR / "img" / "cb.jpg")
        return surface
    except pygame.error:
        return pygame.Surface.__new__(pygame.Surface)