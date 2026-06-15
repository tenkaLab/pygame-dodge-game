from game.package.base_object.gameobject import Gameobject
from game.package.component.transform import Transform

class Worldobject(Gameobject):
    
    def __init__(self):
        super().__init__()

        self.add_component(Transform())