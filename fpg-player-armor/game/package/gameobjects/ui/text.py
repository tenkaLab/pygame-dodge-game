import pygame

from game.package.core.gameobject import Gameuiobject
from game.package.components.sprite_renderer import SpriteRenderer


class Text(Gameuiobject):
    def __init__(
        self, 
        position: tuple[float, float], 
        size: int, 
        scale: tuple[float, float], 
        layer: int, 
        text: str, 
        color:tuple[int,int,int],
        init_active: bool = True
    ):
        super().__init__()

        self.active = init_active

        transform = self.get_component("RectTransform")
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        self.add_component(SpriteRenderer())

        self.font = pygame.font.SysFont(None, size)
        self.text: str = str(text) or "None"
        self.color: tuple[int,int,int] = color or (255,255,255)

        self.flag = True

    def start(self):
        self.sprite_renderer = self.get_component("SpriteRenderer")
        self._set_surface()
        return super().start()
    
    def update(self):
        if self.flag == True:
            self._set_surface()
            self.flag = False

        return super().update()

    def set_text(self, text: str):
        self.text = str(text)
        self.flag = True

    def set_color(self, color: tuple[int,int,int]):
        self.color = tuple(color)
        self.flag = True

    def _set_surface(self):
        self.sprite_renderer.set_surface(self.font.render(self.text, True, self.color))