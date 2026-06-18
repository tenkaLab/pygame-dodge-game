from game import paths
from game.app.scenes.title_scene import TitleScene
from game.app.scenes.game_scene import GameScene
from game.app.scenes.result_scene import ResultScene

game = {
    "name" : "pygame-dodge-game",
    "version" : "0.21",
    "icon_image_path" : paths.DEFAULT_ICON_IMAGE,
    
    "window_size" : [640, 480],
    "screen_size" : [640, 480],

    "max_tps" : 30,
    "max_fps" : 30,

    "initial_scene_index" : 0,
}

global_values = {
    "score" : 0,
}

debug = {
    "show_colliders" : False,
    "print_key_events" : False
}

scenes = [
    TitleScene,
    GameScene,
    ResultScene
]
