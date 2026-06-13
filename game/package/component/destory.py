from game.package.base_object.base_component import BaseComponent

class Destroy(BaseComponent):
    def __init__(self):
        super().__init__()
        self.do_destroy = False
    
    def update(self):
        if self.do_destroy:
            if self.engine is not None:
                self.engine.current_scene.game_objects.remove(self.parent_gameobject)

        return super().update()
        