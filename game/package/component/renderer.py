from dataclasses import dataclass
import pygame

from game.package.base_object.base_component import BaseComponent
from game.package.util.make_empty_surface import make_empty_surface

@dataclass
class RenderObject:
    surface: pygame.Surface
    position: tuple[int, int]
    layer: int

class Renderer(BaseComponent):
    def __init__(self):
        super().__init__()
        self.render_objects: dict[int, RenderObject] = {}

    def register_render_as(self, component_object_id: int):
        self.render_objects[component_object_id] = RenderObject(make_empty_surface(), (0,0), 0)