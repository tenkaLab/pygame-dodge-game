import random

from game.package.base_objects import Scene
from ..gameobjects.enemy import Enemy
from ..gameobjects.player import Player
from ..gameobjects.ui import Text


class GameScene(Scene):

    def start(self):

        player = Player(
            position= (
                self.engine.screen.get_width() // 2, 
                self.engine.screen.get_height() // 1.5
            ), 
            scale= (2,2), 
            layer= 4,
            speed= 13
        )
        
        self.add_worldobject(player)

        self.score_num_text = Text((0.1,0.1), 50, (1,1), 1, "0", (255,255,255))
        self.add_uiobject(self.score_num_text)

        self.gameover_text = Text((0.5,0.5), 50, (1,1), 1, "Gameover", (255,255,255))
        self.add_uiobject(self.gameover_text)
        self.gameover_text.active = False

        self.timer = 0

        self.gameover: bool = False

        self.level = 0
        self.score = 0

        self.flag = False

        return super().start()
    
    def update(self):
        
        keys = self.engine.input_status.keys

        if keys.get("escape", False):
            self.engine.shutdown()

        if self.gameover:
            if not self.flag:
                self.gameover_text.active = True
                self.engine.global_values["score"] = self.score
                self.engine.scheduler.schedule_event(1, self.engine.change_scene, 2)
                self.flag = True
            return
            
        dt = self.engine.delta_time

        self.timer += dt
        if self.timer >= 0.1:

            self.level += 0.1
            _speed = self.level * 0.01
            enemy = Enemy(
                position= (random.randint(0, self.engine.screen.get_width()), 0), 
                scale= (random.randint(20,60),random.randint(20,60)), 
                layer= 1, 
                color= (0,0,255),
                speed= _speed
            )
            self.add_worldobject(enemy)

            self.score = round((self.score + 0.1), 2)
            self.score_num_text.set_text(str(self.score))
            
            self.timer = 0

        return super().update()