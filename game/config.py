from game import paths
from game.app.game_scene import GameScene

game = {
    "name" : "MyGame",
    "version" : "0.1",
    "icon_image_path" : paths.DEFAULT_ICON_IMAGE,
    
    "window_size" : [640*1.4, 480*1.4],
    "screen_size" : [640, 480],

    "max_tps" : 30,
    "max_fps" : 30,

    "initial_scene_class" : GameScene,
}
