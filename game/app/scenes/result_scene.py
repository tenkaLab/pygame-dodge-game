import json

from game.package.base_objects import Scene
from game.package.gameobjects.uiobjects import Text


class ResultScene(Scene):

    def start(self):

        title_text = Text((0.5,0.3), 200, (0.5,0.5), 1, str("Result"), (255,255,255))
        self.add_uiobject(title_text)

        text = Text((0.5,0.6), 100, (0.25,0.25), 1, str("score"), (255,255,255))
        self.add_uiobject(text)

        text = Text((0.5,0.75), 100, (0.25,0.25), 1, str("hiscore"), (255,255,255))
        self.add_uiobject(text)

        score = self.engine.global_values["score"]
        hiscore = 0

        try :
            with open("./game/app/assets/data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not hasattr(data, "hiscore"):
                hiscore = data["hiscore"]
        except:
            hiscore = 0
            print("リザルトシーンのデータロードエラーが発生しました。")
            
        if score > hiscore:
            hiscore = score

        with open("./game/app/assets/data.json",  "w", encoding="utf-8") as f:
            json.dump({"hiscore":hiscore}, f)

        self.score_numtext = Text((0.5,0.65), 100, (0.25,0.25), 1, str(score), (255,255,255))
        self.hiscore_numtext = Text((0.5,0.8), 100, (0.25,0.25), 1, str(hiscore), (255,255,255))
        self.add_uiobject(self.score_numtext)  
        self.add_uiobject(self.hiscore_numtext)  

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys
        if keys.get("escape", False):
            self.engine.shutdown()

        if keys.get("r", False):
            self.engine.change_scene(1)

        if keys.get("t", False):
            self.engine.change_scene(0)

        return super().update()