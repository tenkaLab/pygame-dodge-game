import pygame
import random

from game.package import (
    Gameworldobject,
    SpriteRenderer, 
    Collider
)
class Enemy(Gameworldobject):
    def __init__(self, init_speed):
        super().__init__()
        self.speed = init_speed
        
    def start(self):
        self.transfrom = self.get_component("Transform")
        self.transfrom.position = (
            random.randint(
                0,
                self.engine.screen.get_width()
            ),
            -60
        )
        self.transfrom.scale = (
            random.randint(20, 60),
            random.randint(20, 60)
        )
        self.transfrom.layer = 1
        
        sprite = SpriteRenderer()
        surface = pygame.Surface((1,1))
        surface.fill((0, 0, 255))
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(1,1), ((0,255,0)))
        collider.is_collision_enabled = False
        self.add_component(collider)

    def update(self):
        dt = self.engine.delta_time
        self.transfrom.position.y += 20 * 10 * dt

        if self.transfrom.position.y > self.engine.screen.get_height():
            self.destroy()

        return super().update()