import pygame
from pathlib import Path

from game.package.core.render_data import RenderData
from game.package.core.component import Component
from game.package.components.transform import Transform, RectTransform
from game.package.util.make_empty_surface import make_empty_surface


class SpriteRenderer(Component):

    def __init__(self):
        super().__init__()

        self.original_surface: pygame.Surface = None
        self.flag = True
        self.render_data = RenderData()

    def start(self):
        a = self.parent.get_component("Transform")
        b = self.parent.get_component("RectTransform")
        if not a is None:
            self.transform: Transform = a
        else:
            self.transform: RectTransform = b

        return super().start()

    def update(self):

        if self.flag:
            osw, osh = self.original_surface.get_size()
            psx, psy = self.transform.scale.xy
            scaled_surface = pygame.transform.scale(
                self.original_surface, (
                    osw * psx, 
                    osh * psy
                )
            )
            self.render_data.surface = scaled_surface
            self.flag = False
        
        self.render_data.position = self.transform.position
        self.render_data.layer = self.transform.layer

        return super().update()
    
    def get_surface(self) -> pygame.Surface:
        return self.original_surface
    
    def set_surface(self, surface : pygame.Surface):
        self.original_surface = surface
        self.flag = True

    def load_surface(self, image_path: Path):
        self.original_surface = pygame.image.load(image_path)
        self.flag = True