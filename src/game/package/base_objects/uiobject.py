from game.package.base_objects.gameobject import Gameobject
from game.package.components.transform import RectTransform

class Uiobject(Gameobject):

    def __init__(self):
        super().__init__()

        self.add_component(RectTransform())