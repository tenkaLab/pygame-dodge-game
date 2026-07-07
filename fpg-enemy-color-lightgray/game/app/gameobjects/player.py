import pygame

from game.package.base_objects import Worldobject, Component
from game.package.components import Transform, SpriteRenderer, Collider
from game.app.components.state import State


class Player(Worldobject):

    def __init__(self, position:tuple, scale:tuple, layer:int, init_speed):
        super().__init__()
        
        transform = self.get_component("Transform")
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        sprite = SpriteRenderer()
        surface = pygame.Surface((10,10))
        surface.fill((255,0,0))
        sprite.set_surface(surface)
        
        collider = Collider()
        collider.is_collision_enabled = False
        collider.add_hitbox((0,0), (10,10), (0,255,0,200))
        

        self.add_component(Controller())
        self.add_component(sprite)
        self.add_component(collider)

        self.speed = init_speed
        
class Controller(Component):

    def start(self):
        self.transform: Transform = self.parent.get_component("Transform")
        self.sprite_renderer: SpriteRenderer = self.parent.get_component("SpriteRenderer")
        self.collider: Collider = self.parent.get_component("Collider")
        self.state: State = self.parent.get_component("State")

        self.camera = self.engine.current_scene.camera

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys
        dt = self.engine.delta_time

        w, h = self.sprite_renderer.get_surface().get_size()
        sx, sy = self.transform.scale
        scaled_size = (
            w * sx,
            h * sy
        )

        if keys.get("w", False):
            self.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * dt

            if self.transform.position.y < 0:
                self.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * dt

        if keys.get("s", False):
            self.transform.position.y += (scaled_size[1] / 2) * self.parent.speed * dt

            if self.transform.position.y >= self.engine.screen.get_height() - scaled_size[1]:
                self.transform.position.y -= (scaled_size[1] / 2) * self.parent.speed * dt

        if keys.get("a", False):
            self.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * dt

            if self.transform.position.x < 0:
                self.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * dt
        
        if keys.get("d", False):
            self.transform.position.x += (scaled_size[0] / 2) * self.parent.speed * dt

            if self.transform.position.x >= self.engine.screen.get_width() - scaled_size[0]:
                self.transform.position.x -= (scaled_size[0] / 2) * self.parent.speed * dt

        if self.collider.is_colliding():
            self.engine.current_scene.set_gameover()

        return super().update()