import time

from game.package.core.component import Component
from game.package.components.transform import Transform
from game.package.components.transform import RectTransform


class Gameobject:
    
    def __init__(self):

        self.active: bool = True
        self.is_started: bool = False
        self.tags: list[str] = []
        self.parent = None
        self.children:dict[str, int] = {}
        self.components: dict[Component] = {}
        
        self.created_timestamp: float = time.time()

        self.engine = None
        

    def start(self):

        pass

    def update(self):

        pass
    
    def add_tag(self, name: str):

        self.tags.append(name)

    def add_child(self, name: str, child_gameobject):
        child_gameobject.parent = self
        self.children[name] = id(child_gameobject)

    def get_child(self, target_name: str):
        for name, _id in self.children.items():
            if name == target_name:
                return self.engine.current_scene.get_worldobject(_id)
        return None
    
    def add_component(self, component: Component):
        component.parent = self
        self.components[component.__class__.__name__] = component
        return component

    def get_component(self, target_name: str):
        for name, component in self.components.items():
            if name == target_name:
                return component
        return None
    
    def destroy(self):
        for gameobject in self.engine.current_scene.world:
            if self == gameobject:
                self.engine.current_scene.world.remove(gameobject)
                return

        for gameobject in self.engine.current_scene.canvas:
            if self == gameobject:
                self.engine.current_scene.canvas.remove(gameobject)
                return
           

class Gameworldobject(Gameobject):
    
    def __init__(self):
        super().__init__()

        self.add_component(Transform())

    def destroy(self):
        for gameobject in self.engine.current_scene.world:
            if self == gameobject:
                self.engine.current_scene.world.remove(gameobject)
                return


class Gameuiobject(Gameobject):

    def __init__(self):
        super().__init__()

        self.add_component(RectTransform())

    def destroy(self):
        for gameobject in self.engine.current_scene.canvas:
            if self == gameobject:
                self.engine.current_scene.canvas.remove(gameobject)
                return