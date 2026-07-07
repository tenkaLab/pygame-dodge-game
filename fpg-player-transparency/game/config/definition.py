from game.app.scenes.title_scene import TitleScene
from game.app.scenes.game_scene import GameScene
from game.app.scenes.result_scene import ResultScene


scenes = [
    TitleScene,
    GameScene,
    ResultScene
]

initial_scene_index = 0

global_values = {
    "score" : 0,
}

debug = {
    "show_colliders" : False,
    "print_key_events" : False
}