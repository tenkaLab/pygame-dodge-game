import pygame

from game.package.core.gameobject import Gameobject
from game.package.components.transform import RectTransform
from game.package.components.sprite_renderer import SpriteRenderer


class Image(Gameobject):
    def __init__(self, position, size, scale, layer):
        super().__init__()

        transform = RectTransform()
        transform.position = position
        transform.scale = scale
        transform.layer = layer
        self.add_component(transform)


        sprite = SpriteRenderer()
        surface = pygame.Surface(size)
        surface.fill((255,255,255))
        sprite.set_surface(surface)
        self.add_component(sprite)