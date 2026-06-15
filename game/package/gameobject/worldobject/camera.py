import pygame
from game.package.base_object.worldobject import Worldobject

class Camera(Worldobject):
    
    def __init__(self):
        super().__init__()
        self.tags.append("camera")

        self.offset = pygame.Vector2()