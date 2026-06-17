from game.package.base_objects import Scene
from game.app.gameobjects.ui import Text
from game.app.scenes.game_scene import GameScene

class TitleScene(Scene):

    def start(self):

        title_text = Text((0.5,0.3), 200, (0.5,0.5), 1, str("DODGE GAME"), (255,255,255))
        self.add_uiobject(title_text)

        title_text = Text((0.5,0.7), 100, (0.25,0.25), 1, str("Press the Eenter key to start the game "), (255,255,255))
        self.add_uiobject(title_text)

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys
        if keys.get("escape", False):
            self.engine.shutdown()

        if keys.get("return", False):
            self.engine.change_scene(1)

        return super().update()