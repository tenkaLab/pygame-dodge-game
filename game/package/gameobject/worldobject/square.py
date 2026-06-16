import pygame

from game.package.base_object.worldobject import Worldobject
from game.package.component.sprite_renderer import SpriteRenderer
from game.package.component.collider import Collider

class Square(Worldobject):
    def __init__(
            self, 
            position: tuple[float,float], 
            scale: tuple[float,float], 
            layer: int,
            color: tuple[int,int,int]
        ):
        super().__init__()

        transfrom = self.get_component("Transform")
        transfrom.position = position
        transfrom.scale = scale
        transfrom.layer = layer

        sprite = SpriteRenderer()
        surface = pygame.Surface((1,1))
        surface.fill(color)
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(1,1), (255,0,0))
        self.add_component(collider)