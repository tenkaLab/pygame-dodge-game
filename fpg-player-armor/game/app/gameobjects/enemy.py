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

        self.tags.append("Enemy")

        self.transform = self.get_component("Transform")
        self.transform.scale = (
            random.randint(2, 6),
            random.randint(2, 6)
        )
        self.transform.layer = 1

        surface = pygame.Surface((8,8))
        surface.fill((0, 0, 255))
        self.sprite_renderer = SpriteRenderer()
        self.sprite_renderer.set_surface(surface)
        self.add_component(self.sprite_renderer)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), ((0,255,0,200)))
        collider.is_collision_enabled = False
        self.add_component(collider)

        self.speed = init_speed

        self.rotation_angle = 0
        
    def start(self):

        self.transform.position = (
            random.randint(
                0,
                self.engine.screen.get_width()
            ),
            -60
        )

        self.dt = self.engine.delta_time

    def update(self):
        
        self.transform.position.y += 20 * 10 * self.dt

        if self.transform.position.y > self.engine.screen.get_height():
            self.destroy()

        return super().update()
    
    def send_flying(self):
        fe = FlyingEnemy(
            surface= self.sprite_renderer.get_surface(),
            position= self.transform.position.xy,
            scale= self.transform.scale.xy,
            layer= self.transform.layer
        )
        self.engine.current_scene.add_gameworldobject(fe)
        self.destroy()


class FlyingEnemy(Gameworldobject):

    def __init__(self, surface:pygame.Surface, position:tuple, scale:tuple, layer:int):
        super().__init__()

        self.transform = self.get_component("Transform")
        self.transform.position = position
        self.transform.scale = scale
        self.transform.layer = layer
        
        self.sprite_renderer = SpriteRenderer()
        self.sprite_renderer.set_surface(surface)
        self.add_component(self.sprite_renderer)

        self.rotation_angle = 0

    def start(self):
        self.dt = self.engine.delta_time
        return super().start()

    def update(self):

        self.transform.position.x += 20 * 10 * self.dt
        self.transform.position.y += 40 * 10 * self.dt

        self.rotation_angle += -360 * self.dt
        self.sprite_renderer.set_rotation_angle(self.rotation_angle % 360)

        if self.transform.position.y > self.engine.screen.get_height():
            self.destroy()
        
        return super().update()