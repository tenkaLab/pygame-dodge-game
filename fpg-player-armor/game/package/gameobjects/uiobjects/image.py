import pygame

from game.package.base_objects import Uiobject
from game.package.components import SpriteRenderer


class Image(Uiobject):
    def __init__(self, position, size, scale, layer):
        super().__init__()

        transform = self.get_component("RectTransform")
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        sprite = SpriteRenderer()
        surface = pygame.Surface(size)
        surface.fill((255,255,255))
        sprite.set_surface(surface)
        self.add_component(sprite)