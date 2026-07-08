import pygame

from game.package.gameobjects.world.camera import Camera


class Scene:
    
    def __init__(self):
        self.active = True
        self.is_started = False

        self.world = [] 
        self.canvas = []

        self.engine = None

        self.camera = Camera()
        self.add_gameworldobject(self.camera)

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

            for go in gameobjects:
                if go.is_started:
                    go.update()
                    for comp in go.components.values():       
                        comp.update()

    def render(self, screen):

        return self._render_gameuiobjects(
            self._render_gameworldobjects(screen)
            )

    def add_gameworldobject(self, game_object):

        self.world.append(game_object)
        return game_object

    def add_gameuiobject(self, game_object):

        self.canvas.append(game_object)
        return game_object

    def get_gameworldobject(self, object_id):
        for game_object in self.world:
            if id(game_object) == object_id:
                return game_object
            
        return None

    def _render_gameworldobjects(self, screen):

        camera = self.camera
        if not get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not get_state(camera_transform):
            return
        
        camera_position = camera_transform.position.xy
        camera_anchor = camera.anchor

        render_data_list = create_render_data_list(self.world)
        render_data_list.sort(key=lambda x: x.layer)

        for render_data in render_data_list:
            screen = self._draw_gameworldobject(
                screen,
                camera_position,
                camera_anchor,
                render_data.surface, 
                render_data.position
            )

        return screen

    def _draw_gameworldobject(
            self, 
            screen,
            camera_position,
            camera_anchor,
            draw_surface: pygame.Surface, 
            gameobject_position: tuple[int,int]
        ):

        draw_position = (
            (gameobject_position[0] - camera_position[0]) + camera_anchor[0],
            (gameobject_position[1] - camera_position[1]) + camera_anchor[1]
        )

        screen.blit(
            draw_surface,
            draw_position
        )

        return screen

    def _render_gameuiobjects(self, screen):

        render_data_list = create_render_data_list(self.canvas)
        render_data_list.sort(key=lambda x: x.layer)

        for render_data in render_data_list:
            screen = self._draw_gameuiobject(
                screen,
                render_data.surface, 
                render_data.position
            )
        
        return screen

    def _draw_gameuiobject(
            self, 
            screen,
            draw_surface, 
            gameobject_position
        ):

        screen_size = screen.get_size()
        surface_size = draw_surface.get_size()

        draw_position = (
            gameobject_position.x - (surface_size[0] // 4),
            gameobject_position.y - (surface_size[1] // 4)
        )

        screen.blit(
            draw_surface, 
            draw_position
        )

        return screen


def create_render_data_list(gameobjects):
    return  [
        comp.render_data
        for go in gameobjects
        if get_state(go)
        for comp in go.components.values()
        if hasattr(comp, "render_data")
    ]

def get_state(object):

    if object is None:
        return False
    
    if not object.active:
        return False
    
    return True