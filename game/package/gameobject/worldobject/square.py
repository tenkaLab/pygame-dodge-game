import pygame

from game.package.base_object.base_worldobject import BaseWorldobject
from game.package.component.renderer import Renderer
from game.package.component.sprite import Sprite
from game.package.component.collider import Collider

class Square(BaseWorldobject):
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

        self.add_component(Renderer())

        sprite = Sprite()
        surface = pygame.Surface((8,8))
        surface.fill(color)
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), (255,0,0))
        self.add_component(collider)