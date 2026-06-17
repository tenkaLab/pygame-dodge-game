from game.package.gameobjects import Square
from game.package.components import Collider

class Enemy(Square):
    def __init__(self, position, scale, layer, color, speed):
        super().__init__(position, scale, layer, color)
        self.speed = 5 + speed
    
    def start(self):
        self.transfrom = self.get_component("Transform")
        self.collider: Collider = self.get_component("Collider")
        self.collider.is_collision_enabled = False

    def update(self):
        self.transfrom.position.y += 5

        if self.transfrom.position.y > self.engine.screen.get_height():
            self.destroy()

        return super().update()