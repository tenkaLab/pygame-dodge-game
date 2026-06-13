from dataclasses import dataclass
import pygame

from game.package.base_object.base_component import BaseComponent

@dataclass
class Hitbox:
    offset_position: tuple[int,int]
    size: tuple[int,int]
    color: tuple[int,int,int]
        

class Collider(BaseComponent):
    def __init__(self):
        super().__init__()
        self.hitboxes = []
        self.last_pos = (0,0)
        self.debug_surface = pygame.Surface((1,1), pygame.SRCALPHA)

        self.is_collision_enabled = True
        self.is_render_debug = True

    def start(self):
        self.worldobjects = self.engine.current_scene.world

        self.transform = self.parent.get_component("Transform")
        self.renderer = self.parent.get_component("Renderer")
        self.renderer.register_render_as(id(self))

        self.last_pos = self.transform.position

        return super().start()

    def update(self):
        if self.is_render_debug:
            self._update_debug_surface()
        if self.is_collision_enabled:
            self._resolve_collision()
        

        return super().update()

    def add_hitbox(
            self, 
            offset_position: tuple[float,float], 
            size: tuple[float,float], 
            color: tuple[float,float,float]
        ):
        color = color or (255,255,255)
        self.hitboxes.append(Hitbox(offset_position, size, color))

    def is_colliding(self):
        for my_hitbox in self.hitboxes:
           
           my_rect = self._create_rect(self.transform, my_hitbox)
           
           for target_worldobject in self.worldobjects:
                if target_worldobject is self.parent:
                    continue

                target_collider = target_worldobject.get_component("Collider")
                target_transform = target_worldobject.get_component("Transform")
                if target_collider is None or target_transform is None:
                   continue

                for target_hitbox in target_collider.hitboxes:

                    target_rect = self._create_rect(target_transform, target_hitbox)

                    if my_rect.colliderect(target_rect):
                        return True
                
        return False

    def _resolve_collision(self):
        if self.is_colliding():
            self.transform.position = self.last_pos
            return
        
        self.last_pos = self.transform.position
    
    def _create_rect(self, transform, hitbox):
        pos = (
            transform.position.x + (hitbox.offset_position[0] * transform.scale.x),
            transform.position.y + (hitbox.offset_position[1] * transform.scale.y)
        )

        scaled_size = (
            hitbox.size[0] * transform.scale.x,
            hitbox.size[1] * transform.scale.y
        )

        return pygame.Rect(
            pos[0],
            pos[1],
            scaled_size[0],
            scaled_size[1]
        )
    
    def _update_debug_surface(self):

        position = self.transform.position
        scale = self.transform.scale

        scaled_hitboxes = [
            (
                hitbox.offset_position[0] * scale[0],
                hitbox.offset_position[1] * scale[1],
                hitbox.size[0] * scale[0],
                hitbox.size[1] * scale[1],
                hitbox.color
                )
            for hitbox in self.hitboxes
        ]


        first = scaled_hitboxes[0]

        left = first[0]
        top = first[1]
        right = first[0] + first[2]
        bottom = first[1] + first[3]

        for hitbox in scaled_hitboxes:
            left = min(left, hitbox[0])
            top = min(top, hitbox[1])
            right = max(right, hitbox[0] + hitbox[2])
            bottom = max(bottom, hitbox[1] + hitbox[3])

        x = left
        y = top
        w = right - left
        h = bottom - top

        combined_surface = pygame.Surface((w, h))
        combined_surface.fill((255,255,255))


        for hitbox in scaled_hitboxes:
            hitbox_surface = pygame.Surface((hitbox[2],hitbox[3]))
            hitbox_surface.fill(hitbox[4])
            combined_surface.blit(hitbox_surface, (hitbox[0] - x, hitbox[1] - y))

        obj = self.renderer.render_objects[id(self)]
        obj.surface = combined_surface
        obj.position = (position.x + x, position.y + y)
        obj.layer = self.transform.layer -1

