from game.package import Scene
from game.package import Text


class DifficultySelectionScreen(Scene):
    def __init__(self):
        super().__init__()

        self.add_gameobject(Text((0.5,0.3), 60, (1,1), 0, "Difficulty Selection", (255,255,255), True))


        self.choice_texts = [
            Text((0.5,0.6), 40, (1,1), 0, "Easy", (255,255,255)),
            Text((0.5,0.7), 40, (1,1), 0, "Normal", (255,255,255)),
            Text((0.5,0.8), 40, (1,1), 0, "Hard", (255,255,255))
        ]

        for obj in self.choice_texts:
            self.add_gameobject(obj)

        self.index = 1

        self.block = [False,False]

    def start(self):
        self.input_keys :dict = self.engine.input_status.keys
        return super().start()

    def update(self):
        if self.input_keys.get("space", False):
            self.engine.change_scene(2)

        if self.input_keys.get("up", False) and not self.block[1]:
            self.index = (self.index - 1 + 3) % 3
            self.block[1] = True
        elif not self.input_keys.get("up", False):
            self.block[1] = False
    
        if self.input_keys.get("down", False) and not self.block[0]:
            self.index = (self.index + 1) % 3
            self.block[0] = True
        elif not self.input_keys.get("down", False):
            self.block[0] = False


        self.choice_texts[self.index].set_color((255,255,0))

        for i in range(len(self.choice_texts)):
            self.choice_texts[i].set_color((255,255,255))
            if i == self.index:
                self.choice_texts[i].set_color((255,255,0))

        return super().update()