import pygame

from game.package.base_object.base_component import BaseComponent


class Sprite(BaseComponent):
    def __init__(self):
        super().__init__()
        self._original_surface: pygame.Surface | None = None
        self._parent_scale_cache: tuple[float, float] = (0.0, 0.0)

    def start(self):
        if self.parent.get_component("Transform") is not None:
            self.transform = self.parent.get_component("Transform")
        else:
            self.transform = self.parent.get_component("RectTransform")
            
        self.renderer = self.parent.get_component("Renderer")
        self.renderer.register_render_as(id(self))
        
        return super().start()

    def update(self):
        if self._original_surface is None:
            return super().update()

        obj = self.renderer.render_objects[id(self)]
        obj.position = tuple(self.transform.position)
        obj.layer = self.transform.layer
        
        current_scale: tuple =  self.transform.scale.xy
        if current_scale != self._parent_scale_cache:
            self._scale_surface(current_scale)

        return super().update()
    
    def set_surface(self, surface: pygame.Surface) -> None:
        self._original_surface = surface
        self._parent_scale_cache = (0.0, 0.0)
    
    def _scale_surface(self, scale: tuple[float, float]) -> None:
        scale_x, scale_y = scale
        w, h = self._original_surface.get_size()
        
        obj = self.renderer.render_objects[id(self)]
        obj.surface = pygame.transform.scale(self._original_surface, (w * scale_x, h * scale_y))


        self._parent_scale_cache = scale