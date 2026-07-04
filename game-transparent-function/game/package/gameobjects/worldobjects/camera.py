import pygame
from game.package.base_objects.worldobject import Worldobject

class Camera(Worldobject):
    
    def __init__(self):
        super().__init__()
        self.tags.append("camera")

        self._offset_position: pygame.Vector2 = pygame.Vector2()

    @property
    def offset_position(self) -> pygame.Vector2:
        return self._offset_position

    @offset_position.setter
    def offset_position(self, value: tuple[float, float]):
        self._offset_position = pygame.Vector2(value[0], value[1])