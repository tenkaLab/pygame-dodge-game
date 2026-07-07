import random
import json

from game import paths
from game.package import (
    Scene,
    Text
)
from ..gameobjects.player import Player
from ..gameobjects.enemy import Enemy


class Timer:
    def __init__(self, target_method, target_time):
        self.method = target_method
        self.target_time = target_time
        self.timer = 0

    def update(self, dt):
        self.timer += dt

        while self.timer >= self.target_time:
            self.method()
            self.timer -= self.target_time


class GameScene(Scene):

    def start(self):

        with open(paths.APP_ASSET_DIR / "parameter.json", "r") as f:
            self.parameter = json.load(f)

        self.player_init_move_speed = self.parameter["player"]["init_move_speed"]
        self.enemy_move_speed = self.parameter["enemy"]["init_move_speed"]
        self.enemy_spawn_speed = self.parameter["enemy"]["init_spawn_speed"]
        self.spawn_interval_decrease = self.parameter["difficulty"]["enemy_spawn_interval_decrease"]
        self.enemy_move_speed_increase = self.parameter["difficulty"]["enemy_move_speed_increase"]
        self.difficulty_increase_interval = self.parameter["difficulty"]["increase_interval"]

        self.score: float = 0.0
        self.level: int = 0
        self.is_gameover: bool = False

        self.timers: dict[str, Timer] = {
            "count_score": Timer(
                target_method= self._count_score, 
                target_time= 0.1
                ),
            "spawn_enemy": Timer(
                target_method= self._spawn_enemy, 
                target_time= self.enemy_spawn_speed
            ),
            "up_difficulty": Timer(
                target_method= self._up_difficulty, 
                target_time= self.difficulty_increase_interval
            )
        }

        self._add_gameobjects()

        return super().start()

    def update(self):

        keys = self.engine.input_status.keys
        dt = self.engine.delta_time

        if keys.get("escape", False):
            self.engine.shutdown()

        if self.is_gameover:
            return

        self._update_timers(dt)

        return super().update()
    
    def set_gameover(self):

        if self.is_gameover:
            return

        self.is_gameover = True

        self._on_gameover()

    def _add_gameobjects(self):

        player = Player(
            position=(
                self.engine.screen.get_width() // 2,
                self.engine.screen.get_height() // 1.5
            ),
            scale=(2, 2),
            layer=0,
            init_speed=self.player_init_move_speed
        )

        self.add_gameworldobject(player)

        self.score_num_text = Text(
            position=(0.1, 0.1),
            size=50,
            scale=(1, 1),
            layer=1,
            text="0",
            color=(255, 255, 255)
        )

        self.gameover_text = Text(
            position=(0.5, 0.5),
            size=50,
            scale=(1, 1),
            layer=1,
            text="Gameover",
            color=(255, 255, 255),
            init_active=False
        )

        self.add_gameuiobject(self.score_num_text)
        self.add_gameuiobject(self.gameover_text)


    def _update_timers(self, dt):

        for timer in self.timers.values():
            timer.update(dt)


    def _count_score(self):

        self.score += 0.1
        self.score = round(self.score, 1)

        self.score_num_text.set_text(f"{self.score:.1f}")

    def _spawn_enemy(self):

        e = Enemy(
            init_speed=self.enemy_move_speed
        )

        self.add_gameworldobject(e)

    def _up_difficulty(self):

        self.level += 1

        self.enemy_move_speed += (
            self.enemy_move_speed_increase
        )

        self.enemy_spawn_speed -= (
            self.spawn_interval_decrease
        )

        self.enemy_spawn_speed = max(
            0.02,
            self.enemy_spawn_speed
        )

        self.timers["spawn_enemy"].target_time = (
            self.enemy_spawn_speed
        )

    def _on_gameover(self):

        self.gameover_text.active = True

        self.engine.global_values["score"] = self.score

        self.engine.scheduler.schedule_event(1, self.engine.change_scene, 2)