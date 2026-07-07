import pygame

from game.package.core.gameobject import Gameworldobject


class Camera(Gameworldobject):
    
    def __init__(self):
        super().__init__()
        self.tags.append("camera")

        self._anchor = pygame.Vector2()

    @property
    def anchor(self) -> pygame.Vector2:
        return self._anchor

    @anchor.setter
    def anchor(self, value: tuple[float, float]):
        self._anchor = pygame.Vector2(value[0], value[1])