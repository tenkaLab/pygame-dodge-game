import time
from game.package.component.destory import Destroy

class BaseGameobject:
    def __init__(self):
        self.active: bool = True
        self.is_started: bool = False
        self.tags: list = []
        self.children:dict[str, int] = {}
        self.components: dict = {}
        
        self.created_timestamp: float = time.time()

        self.add_component(Destroy())

        self.engine = None

    def start(self):
        pass
    
    def add_tag(self, name):
        self.tags.append(name)

    def add_child(self, name, child_gameobject):
        child_gameobject.parent = self
        self.children[name] = id(child_gameobject)

    def get_child(self, target_name):
        for name, _id in self.children.items():
            if name == target_name:
                return self.engine.current_scene.get_worldobject(_id)
        return None
    
    def add_component(self, component):
        component.parent = self
        self.components[component.__class__.__name__] = component
        return component

    def get_component(self, target_name:str):
        for name, component in self.components.items():
            if name == target_name:
                return component
            
        return None
    
    def destroy(self):
        self.get_component("Destroy").do_destroy = True