import pygame

from game.package.gameobject.worldobject.camera import Camera


class BaseScene:
    
    def __init__(self):
        self.active = True
        self.is_started = False

        self.world = [] 
        self.canvas = []

        self.camera = self.add_worldobject(Camera())

        self.engine = None

    def start(self):
        pass

    def update(self):
        for gameobjects in (self.world, self.canvas):
            for go in gameobjects:
                if go.is_started == False:
                        go.engine = self.engine
                        go.start()
                        go.is_started = True

                for comp in go.components.values():
                    if comp.is_started == False:
                        comp.engine = self.engine
                        comp.start()
                        comp.is_started = True
                        
                    comp.update()

    def draw(self):
        self._draw_worldobjects()
        self._draw_uiobjects()

    def add_worldobject(self, game_object):
        self.world.append(game_object)
        return game_object

    def add_uiobject(self, game_object):
        self.canvas.append(game_object)
        return game_object

    def get_worldobject(self, object_id):
        for game_object in self.world:
            if id(game_object) == object_id:
                return game_object
            
        return None

    def _draw_worldobjects(self):

        screen_size = self.engine.screen.get_size()

        camera = self.camera
        if not get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not get_state(camera_transform):
            return
        
        render_objects = create_render_objects(self.world)
        render_objects.sort(key=lambda x: x.layer)

        for render in render_objects:

            draw_surface = render.surface

            draw_position = (
                (render.position[0] - camera_transform.position.x) + (screen_size[0] // 2),
                (render.position[1] - camera_transform.position.y) + (screen_size[1] // 2)
            )

            self.engine.screen.blit(
                draw_surface,
                draw_position
            )

    def _draw_uiobjects(self):

        screen_size = self.engine.screen.get_size()

        render_objects = create_render_objects(self.canvas)
        render_objects.sort(key=lambda x: x.layer)

        for render in render_objects:
            draw_surface: pygame.Surface = render.surface

            position_ratio = render.position
            surface_size = draw_surface.get_size()

            draw_position = (
                (screen_size[0] * position_ratio[0] - surface_size[0] // 2),
                (screen_size[1] * position_ratio[1] - surface_size[1] // 2)
            )

            self.engine.screen.blit(draw_surface, draw_position)

def create_render_objects(gameobjects):
    return  [
        render_object
        for go in gameobjects
        if get_state(go)
        if get_state(go.get_component("Renderer"))
        for render_object in go.get_component("Renderer").render_objects.values()
    ]

def get_state(object):

    if object is None:
        return False
    
    if not object.active:
        return False
    
    return True