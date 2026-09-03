from game.package import (
    Scene,
    Text
)

class TitleScene(Scene):

    def start(self):

        title_text = Text(
            position=(0.5,0.3),  
            scale=(0.5,0.5), 
            layer=1,
            text= "DODGE GAME",
            size=200, 
            color=(255,255,255)
            )

        guide_text = Text(
            position=(0.5,0.7), 
            scale=(0.25,0.25), 
            layer=1, 
            text="Press the Enter key to start the game",
            size=100,  
            color=(255,255,255)
        )

        self.add_gameobject(title_text)
        self.add_gameobject(guide_text)

        return super().start()
    
    def update(self):
        
        keys = self.engine.input_status.keys

        if keys.get("escape", False):
            self.engine.shutdown()

        if keys.get("return", False):
            self.engine.change_scene(1)

        return super().update()