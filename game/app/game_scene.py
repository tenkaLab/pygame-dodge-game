import random

from game.package.base_object import Scene
from .enemy import Enemy
from .player import Player
from .ui import Text


class GameScene(Scene):

    def start(self):

        player = Player(
            (
                self.engine.screen.get_width() // 2, 
                self.engine.screen.get_height() // 1.5
            ), 
            (2,2), 
            4
        )
        
        self.add_worldobject(player)

        self.score_text = Text((0.1,0.1), 50, (1,1), 1, "0", (255,255,255))
        self.add_uiobject(self.score_text)

        self.gameover_text = Text((0.5,0.5), 50, (1,1), 1, "Gameover", (255,255,255))
        self.add_uiobject(self.gameover_text)
        self.gameover_text.active = False

        self.timer = 0

        self.gameover: bool = False

        self.countup = 0
        self.score = 0

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys

        if keys.get("escape", False):
            self.engine.shutdown()

        if keys.get("r", False):
            self.engine.current_scene.__init__()


        if self.gameover:
            self.gameover_text.active = True
            return
        
        dt = self.engine.delta_time

        self.timer += dt
        if self.timer >= 0.1:
            e = Enemy(
                position= (random.randint(0, self.engine.screen.get_width()), 0), 
                scale= (random.randint(20,60),random.randint(20,60)), 
                layer= 1, 
                color= (0,0,255)
            )
            self.add_worldobject(e)

            self.score += 0.1
            self.score_text.set_text(str(round(self.score, 2)))
            
            self.timer = 0

        return super().update()