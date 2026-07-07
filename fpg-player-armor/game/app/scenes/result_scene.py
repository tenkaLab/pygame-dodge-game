import json

from game import paths
from game.package import (
    Scene,
    Text
)

class ResultScene(Scene):

    def start(self):

        title_text = Text((0.5,0.3), 200, (0.5,0.5), 1, str("Result"), (255,255,255))
        self.add_gameuiobject(title_text)

        text = Text((0.5,0.6), 100, (0.25,0.25), 1, str("score"), (255,255,255))
        self.add_gameuiobject(text)

        text = Text((0.5,0.75), 100, (0.25,0.25), 1, str("hiscore"), (255,255,255))
        self.add_gameuiobject(text)

        score = self.engine.global_values["score"]
        hiscore = 0

        try :
            with open(paths.APP_ASSET_DIR / "data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not hasattr(data, "hiscore"):
                hiscore = data["hiscore"]
            print("リザルトシーンのデータロードが成功しました。")
        except:
            hiscore = 0
            print("リザルトシーンのデータロードエラーが発生しました。")
            
        if score > hiscore:
            hiscore = score

        with open(paths.APP_ASSET_DIR / "data.json",  "w", encoding="utf-8") as f:
            json.dump({"hiscore":hiscore}, f)

        self.score_numtext = Text((0.5,0.65), 100, (0.25,0.25), 1, str(score), (255,255,255))
        self.hiscore_numtext = Text((0.5,0.8), 100, (0.25,0.25), 1, str(hiscore), (255,255,255))
        self.add_gameuiobject(self.score_numtext)  
        self.add_gameuiobject(self.hiscore_numtext)  

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