import pygame

from game.package.gameobjects.world.camera import Camera


class Scene:
    
    def __init__(self):
        self.active = True
        self.is_started = False

        self.gameobjects = [] 


        self.engine = None

        self.camera = Camera()
        self.add_gameobject(self.camera)

    def add_gameobject(self, game_object):

        self.gameobjects.append(game_object)
        return game_object

    def get_gameobject(self, object_id):

        for game_object in self.gameobjects:
            if id(game_object) == object_id:
                return game_object
            
        return None

    def start(self):
        pass

    def update(self):

        for go in self.gameobjects:
            if go.is_started == False:
                go.engine = self.engine
                go.start()
                go.is_started = True
                
            for comp in go.components.values():
                if comp.is_started == False:
                    comp.engine = self.engine
                    comp.start()
                    comp.is_started = True

        for go in self.gameobjects:
            if go.is_started:
                go.update()
                for comp in go.components.values():       
                    comp.update()

    def render(self, screen):
        return self._render_gameobjects(screen)

    def _render_gameobjects(self, screen):

        camera = self.camera
        if not get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not get_state(camera_transform):
            return
        
        camera_position = camera_transform.position.xy
        camera_anchor = camera.anchor

        render_data_list = create_render_data_list(self.gameobjects)
        render_data_list.sort(key=lambda x: x.layer)  

        for meta_layer in ["World","Canvas"]:
            
            for render_data in render_data_list:

                draw_surface = render_data.surface
                gameobject_position = render_data.position

                position_dict = {
                    "Canvas" : (
                        gameobject_position.x - (draw_surface.get_size()[0] // 4),
                        gameobject_position.y - (draw_surface.get_size()[1] // 4)
                    ),

                    "World" : (
                        (gameobject_position[0] - camera_position[0]) + camera_anchor[0],
                        (gameobject_position[1] - camera_position[1]) + camera_anchor[1]
                    )
                } 

                if render_data.transform_type == {"Canvas":"RectTransform", "World":"Transform"}[meta_layer]:
                    draw_position = position_dict[meta_layer]
                else:
                    continue
            
                screen = self._draw_gameobject(
                    screen,
                    draw_surface,
                    draw_position,  
                ) 

        return screen

    def _draw_gameobject(
            self, 
            screen,
            draw_surface: pygame.Surface, 
            draw_position: tuple[int,int]
        ):

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

