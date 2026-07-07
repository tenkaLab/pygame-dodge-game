class Component:
    
    def __init__(self):
        self.active: bool = True
        self.tags: list[str] = []
        self.is_started: bool = False
        self.parent = None

        self.engine = None

    def start(self):
        pass

    def update(self):
        pass

    def add_tag(self, tag_name: str):
        self._tags.append(tag_name)