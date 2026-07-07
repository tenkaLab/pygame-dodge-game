import pygame

from game.package.core.gameobject import Gameworldobject
from game.package.components.sprite_renderer import SpriteRenderer
from game.package.components.collider import Collider


class Square(Gameworldobject):
    def __init__(
            self, 
            position: tuple[float,float], 
            scale: tuple[float,float], 
            layer: int,
            color: tuple[int,int,int],
            hitbox_color: tuple[int,int,int]
        ):
        super().__init__()

        transfrom = self.get_component("Transform")
        transfrom.position = position
        transfrom.scale = scale
        transfrom.layer = layer

        surface = pygame.Surface((8,8))
        surface.fill(color)
        sprite = SpriteRenderer()
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), (hitbox_color))
        self.add_component(collider)