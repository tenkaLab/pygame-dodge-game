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

        self.sprite_renderer = SpriteRenderer()
        self.sprite_renderer.set_surface(pygame.Surface((8,8)))
        
        self.collider = Collider()
        self.collider.is_collision_enabled = False
        self.collider.add_hitbox((0,0), (8,8), (0,255,0,200))
        
        self.add_component(Controller())
        self.add_component(self.sprite_renderer)
        self.add_component(self.collider)

        self.count = 0
        self.flag_1 = False

        self.init_speed = init_speed
        self.speed = self.init_speed

        self.is_armored = True

        self.cach_color = (0,0,0)

    def update(self):
        if self.is_armored:
            self.set_color((255,255,0))
        else:
            self.set_color((255,0,0))
        return super().update()

    def set_color(self, rgb:tuple[int,int,int]):

        if not self.cach_color == rgb:
            self.cach_color = rgb
            surface = self.sprite_renderer.get_surface()
            surface.fill(rgb)
            self.sprite_renderer.set_surface(surface)
        
class Controller(Component):

    def __init__(self):
        super().__init__()

        self.timer = 0

    def start(self):
        self.keys = self.engine.input_status.keys
        self.dt= self.engine.delta_time
        self.camera = self.engine.current_scene.camera
        
        return super().start()
    
    def update(self):

        w, h = self.parent.sprite_renderer.get_surface().get_size()
        sx, sy = self.parent.transform.scale
        scaled_size = (
            w * sx,
            h * sy
        )

        if self.keys.get("w", False):
            self.parent.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * self.dt

            if self.parent.transform.position.y < 0:
                self.parent.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * self.dt

        if self.keys.get("s", False):
            self.parent.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * self.dt

            if self.parent.transform.position.y >= self.engine.screen.get_height() - scaled_size[1]:
                self.parent.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * self.dt

        if self.keys.get("a", False):
            self.parent.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * self.dt

            if self.parent.transform.position.x < 0:
                self.parent.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * self.dt
        
        if self.keys.get("d", False):
            self.parent.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * self.dt

            if self.parent.transform.position.x >= self.engine.screen.get_width() - scaled_size[0]:
                self.parent.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * self.dt


        colliding_gameobjects = self.parent.collider.get_colliding_gameobjects()
        for gameobject in colliding_gameobjects:
            if "Enemy" in gameobject.tags:
                enemy = gameobject
                if self.parent.is_armored:
                    enemy.send_flying()
                    self.parent.is_armored = False
                else:
                    self.engine.current_scene.set_gameover()

        
        if not self.parent.is_armored:
            self.timer += self.dt
            while self.timer > 10:
                print(1)
                self.parent.is_armored = True
                self.timer -= 10



        return super().update()