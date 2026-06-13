from game.package.base_object.base_gameobject import BaseGameobject
from game.package.component.transform import RectTransform

class BaseUiobject(BaseGameobject):
    def __init__(self):
        super().__init__()
        self.add_component(RectTransform())