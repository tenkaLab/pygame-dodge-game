import pygame
import json

from game import paths
from game.package.base_object import BaseWorldobject, BaseComponent
from game.package.component import Renderer, Animator, Collider

class Player(BaseWorldobject):

    def __init__(self, position:tuple, scale:tuple, layer:int,):
        super().__init__()
        
        transform = self.get_component("Transform")
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        self.add_component(Renderer())

        animator = Animator()

        with open(paths.APP_ASSET_DIR / "player/animations_data.json", "r") as f:
            data = json.load(f)

        for name, info in data.items():
            frames: list[pygame.Surface] = []
            spritesheet_surface = pygame.image.load(paths.APP_ASSET_DIR / info["spritesheet_image_path"])
            for frame_info in info["frames"]:
                x, y, w, h = frame_info
                crop_area = pygame.Rect(x*w, y*h, w, h)
                cropped_surface = spritesheet_surface.subsurface(crop_area)
                frames.append(cropped_surface)

            animator.add_animation(name, frames, info["fps"],  info["is_loop"])

        self.add_component(animator)

        collider = Collider()
        collider.is_collision_enabled = False
        collider.add_hitbox((-0,-0), (14,14), (255,0,0,200))
        self.add_component(collider)

        state = State() 
        state.speed = 5
        self.add_component(state)
        
        self.add_component(Controller())
        

class State(BaseComponent):
    def __init__(self):
        super().__init__()
        
class Controller(BaseComponent):

    def start(self):
        self.transform = self.parent.get_component("Transform")
        self.renderer = self.parent.get_component("Renderer")
        self.animator: Animator = self.parent.get_component("Animator")
        self.collider: Collider = self.parent.get_component("Collider")
        self.state: State = self.parent.get_component("State")

        self.camera = self.engine.current_scene.camera

        self.stack = [0,0,0,0]

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys
        dt = self.engine.delta_time

        camera_transform = self.camera.get_component("Transform")

        scale =  self.transform.scale

        surface_size = self.renderer.render_objects[id(self.animator)].surface.get_size()
        scaled_size = (
            surface_size[0] * scale.x, 
            surface_size[1] * scale.y
        )

        state = self.state

        if keys.get("w", False):
            self.transform.position.y -= (scaled_size[1] / 2) * state.speed * dt
            self.animator.change_animation("up_walk", True)
            if self.collider.is_colliding():
                self.transform.position.y += (scaled_size[1] / 2) * state.speed * dt

        if keys.get("s", False):
            self.transform.position.y += (scaled_size[1] / 2) * state.speed * dt
            self.animator.change_animation("down_walk", True)
            if self.collider.is_colliding():
                self.transform.position.y -= (scaled_size[1] / 2) * state.speed * dt

        if keys.get("a", False):
            self.transform.position.x -= (scaled_size[0] / 2) * state.speed * dt
            self.animator.change_animation("left_walk", True)
            if self.collider.is_colliding():
                self.transform.position.x += (scaled_size[0] / 2) * state.speed * dt
        
        if keys.get("d", False):
            self.transform.position.x += (scaled_size[0] / 2) * state.speed * dt
            self.animator.change_animation("right_walk", True)
            if self.collider.is_colliding():
                self.transform.position.x -= (scaled_size[0] / 2) * state.speed * dt

        if keys.get("1", False):
            scale.x += 1
            scale.y += 1

        self.transform.scale = scale 

        camera_transform.position = self.transform.position
        
        return super().update()