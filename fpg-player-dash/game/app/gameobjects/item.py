import pygame
import random

from game.config import paths
from game.package import (
    Gameworldobject,
    SpriteRenderer, 
    Collider
)
from game.package.util.split_spritesheet import split_sprite_sheet

class Item(Gameworldobject):
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
        self.transfrom.scale = (2,2)
        self.transfrom.layer = 1

        frames = split_sprite_sheet(
            image_path= paths.APP_ASSET_DIR/"img"/"arrow.png", 
            cut_size=(16,16)
        )
        sprite = SpriteRenderer()
        sprite.set_surface(frames[random.randint(0,3)])
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(16,16), ((0,255,0)))
        collider.is_collision_enabled = False
        self.add_component(collider)

    def update(self):
        dt = self.engine.delta_time
        self.transfrom.position.y += 15 * self.speed * dt

        if self.transfrom.position.y > self.engine.screen.get_height():
            self.destroy()

        return super().update()