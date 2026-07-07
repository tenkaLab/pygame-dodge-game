import pygame

from game.package.base_objects.component import Component


class Transform(Component):
    def __init__(self):
        super().__init__()
        self._position: pygame.Vector2 = pygame.Vector2(0,0)
        self._scale: pygame.Vector2 = pygame.Vector2(1,1)
        self.layer: int = 0

    @property
    def position(self) -> pygame.Vector2 | None:
        return self._position
    
    @position.setter
    def position(self, position: tuple):
        self._position = pygame.Vector2(position[0], position[1])

    @property
    def scale(self) -> pygame.Vector2 | None:
        return self._scale
    
    @scale.setter
    def scale(self, scale: tuple):
        self._scale = pygame.Vector2(
            max(0, scale[0]),
            max(0, scale[1])
        )
    
class RectTransform(Transform):
    def __init__(self):
        super().__init__()

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position: tuple):
        self._position = pygame.Vector2(
            max(0.0, min(1.0, position[0])),
            max(0.0, min(1.0, position[1]))
        )