from game.package.base_object import BaseScene
from game.package.gameobject import Square
from .player import Player
from .ui import Image


class GameScene(BaseScene):

    def start(self):
        player = Player((-100,0), (2,2),4)
        self.add_worldobject(player)

        square = Square((0,0), (10,10), 1, (0,0,255))
        self.add_worldobject(square)

        image = Image((0.15,0.9), (100,50), (1,1), 1)
        self.add_uiobject(image)
    
        return super().start()