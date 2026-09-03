import pygame
import math

from game.package import (
    Gameobject,
    Component,
    Transform,
    SpriteRenderer, 
    Collider,
    Timer,
)
from game.app.components.state import State


class Player(Gameobject):

    def __init__(self, position:tuple, scale:tuple, layer:int, init_speed):
        super().__init__()
        
        self.transform = Transform()
        self.transform.position = position
        self.transform.scale = scale
        self.transform.layer = layer
        self.add_component(self.transform)

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

    def generate_effect(self):
        self.engine.current_scene.add_gameobject(
            ShadowEffect(
                surface= self.sprite_renderer.get_surface().copy(),
                position=self.transform.position,
                scale=self.transform.scale,
                layer=self.transform.layer -1 
            )
        )
        
class Controller(Component):

    def __init__(self):
        super().__init__()

        self.timer = 0

        self.block_ = False

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

        
        space_key = self.keys.get("space", False)
        if space_key and self.block_ == False:
            self.block_ = True
            self.a()
        elif space_key == False:
            self.block_ = False


        colliding_gameobjects = self.parent.collider.get_colliding_gameobjects()
        for gameobject in colliding_gameobjects:
            if "Enemy" in gameobject.tags:
                enemy = gameobject
                if self.parent.is_armored:
                    enemy.send_flying()
                    self.parent.is_armored = False
                else:
                    self.engine.current_scene.set_gameover()

        
        if self.parent.is_armored == False:
            self.timer += self.dt
            while self.timer > 5:
                self.parent.is_armored = True
                self.timer -= 5

        return super().update()
    
    def a(self):
        self.parent.speed = 45

        self.parent.generate_effect()
        for i in range(5):
            self.engine.scheduler.schedule_event(0.1*i, self.parent.generate_effect)

        self.engine.scheduler.schedule_event(0.1*i, self.b)

    def b(self):
        self.parent.speed = self.parent.init_speed


class ShadowEffect(Gameobject):
    def __init__(self, surface, position, scale, layer):
        super().__init__()

        transform = Transform()
        transform.position = position
        transform.scale = scale
        transform.layer = layer
        self.add_component(transform)

        self.sprite_renderer = SpriteRenderer()

        self.sprite_renderer.set_surface(surface)
        self.add_component(self.sprite_renderer)

        self.timer = 0

        self.timer_2 = 0
        self.red = 255

    def start(self):
        self.dt = self.engine.delta_time
        return super().start()
    
    def update(self):

        self.timer_2 += self.dt
        while self.timer_2 > 0.1:
            self.red = max(self.red - 25, 0)
            surface = self.sprite_renderer.get_surface().copy()
            surface.fill((self.red,0,0))
            self.sprite_renderer.set_surface(surface)
            self.timer_2 -= 0.1

        if self.red < 1:
            self.destroy()

        return super().update()