import pygame

def make_empty_surface() -> pygame.Surface:
    """1×1 の透明なサーフェスを返す。pygame 未初期化でも安全。"""
    try:
        surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        return surface
    except pygame.error:
        # pygame 未初期化時（テスト環境など）は代替を返す
        return pygame.Surface.__new__(pygame.Surface)