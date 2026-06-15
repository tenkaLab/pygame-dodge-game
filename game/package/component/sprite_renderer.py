import pygame
from pathlib import Path

from game.package.core.renderer import RenderData
from game.package.base_object.component import Component
from game.package.component import Transform

from game.package.util.make_empty_surface import make_empty_surface

class SpriteRenderer(Component):

    def __init__(self):
        super().__init__()

        self.surface: pygame.Surface = make_empty_surface()
        self.render_data = RenderData()

    def start(self):
        self.transform: Transform = self.parent.get_component("Transform") or self.parent.get_component("RectTransform")
        return super().start()

    def update(self):

        if (
            self.surface is None or 
            not self.transform.__class__ == Transform
            ):
            return super().update()
        
        
        self.render_data.surface = pygame.transform.scale(
            self.surface, (
                self.surface.get_width() * self.transform.scale.x, 
                self.surface.get_height() * self.transform.scale.y
            )
        )
        self.render_data.position = self.transform.position
        self.render_data.layer = self.transform.layer

        return super().update()
    
    def set_surface(self, surface : pygame.Surface):
        self.surface = surface

    def load_surface(self, image_path: Path):
        self.surface = pygame.image.load(image_path)