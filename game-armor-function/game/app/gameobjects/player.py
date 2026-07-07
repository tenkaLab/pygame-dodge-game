import pygame
import math

from game.package import (
    Gameworldobject,
    Component,
    Transform,
    SpriteRenderer, 
    Collider,
    Timer,
)
from game.app.components.state import State


class Player(Gameworldobject):

    def __init__(self, position:tuple, scale:tuple, layer:int, init_speed):
        super().__init__()
        
        self.transform = self.get_component("Transform")
        self.transform.position = position
        self.transform.scale = scale
        self.transform.layer = layer

        surface = pygame.Surface((10,10))
        surface.fill((255,0,0))

        self.sprite_renderer = SpriteRenderer()
        self.sprite_renderer.set_surface(surface)
        
        self.collider = Collider()
        self.collider.is_collision_enabled = False
        self.collider.add_hitbox((0,0), (10,10), (0,255,0,200))
        
        self.add_component(Controller())
        self.add_component(self.sprite_renderer)
        self.add_component(self.collider)

        self.count = 0
        self.flag_1 = False

        self.init_speed = init_speed
        self.speed = self.init_speed

        self.is_armored = False
        
class Controller(Component):

    def start(self):

        self.camera = self.engine.current_scene.camera
        self.block_ = False
        
        return super().start()
    
    def update(self):

        keys = self.engine.input_status.keys
        dt = self.engine.delta_time

        w, h = self.parent.sprite_renderer.get_surface().get_size()
        sx, sy = self.parent.transform.scale
        scaled_size = (
            w * sx,
            h * sy
        )

        if keys.get("w", False):
            self.parent.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * dt

            if self.parent.transform.position.y < 0:
                self.parent.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * dt

        if keys.get("s", False):
            self.parent.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * dt

            if self.parent.transform.position.y >= self.engine.screen.get_height() - scaled_size[1]:
                self.parent.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * dt

        if keys.get("a", False):
            self.parent.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * dt

            if self.parent.transform.position.x < 0:
                self.parent.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * dt
        
        if keys.get("d", False):
            self.parent.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * dt

            if self.parent.transform.position.x >= self.engine.screen.get_width() - scaled_size[0]:
                self.parent.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * dt

        if self.parent.collider.is_colliding():
            if not self.parent.is_armored:
                self.engine.current_scene.set_gameover()

        space_key = keys.get("space", False)
        if space_key and self.block_ == False:
            self.block_ = True
            self.a()
        elif space_key == False:
            self.block_ = False

        return super().update()
    
    def a(self):
        self.parent.is_armored = True
        
        surface = self.parent.sprite_renderer.get_surface()
        surface.fill((255,255,0))
        self.parent.sprite_renderer.set_surface(surface)

        self.engine.scheduler.schedule_event(1, self.b)

    def b(self):
        self.parent.is_armored = False

        surface = self.parent.sprite_renderer.get_surface()
        surface.fill((255,0,0))
        self.parent.sprite_renderer.set_surface(surface)