import pygame

from game import config


class Engine:  

    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(
            config.game["window_size"], 
            pygame.RESIZABLE
        )

        pygame.display.set_caption(config.game["name"])
        pygame.display.set_icon(pygame.image.load(config.game["icon_image_path"]))
        
        self.running = False

        self.screen = pygame.Surface(config.game["screen_size"])
        init_scene_class = config.game["initial_scene_class"]
        self.current_scene = init_scene_class()

        self.max_tps = config.game["max_tps"]
        self.max_fps = config.game["max_fps"]

        self.delta_time = 0

        self.input_status = InputStatus()

    def start(self):
        self.running = True
        self._loop()

    def _loop(self):
        clock = pygame.time.Clock()
        accumulator = 0.0
        fixed_dt = 1.0 / self.max_tps

        tps_timer = 0
        tps_count = 0
        fps_timer = 0
        fps_count = 0
        tps = 0

        while self.running:
            dt = clock.tick(self.max_fps) / 1000
            accumulator += min(dt, fixed_dt * 5)

            fps_timer += dt

            while accumulator >= fixed_dt:
                self.delta_time = fixed_dt
                self._update()

                accumulator -= fixed_dt
                
                tps_timer += fixed_dt
                tps_count += 1
            
            self._draw()
            fps_count += 1

            if tps_timer >= 1:     
                tps = tps_count
                tps_timer = 0
                tps_count = 0

            if fps_timer >= 1:
                print(f"{tps} ticks, {fps_count} fps")

                fps_timer = 0
                fps_count = 0

    def _update(self):
        self._process_input_events()
        self.screen.fill((0, 0, 0))

        scene = self.current_scene
        if not scene.is_started:  
            scene.engine = self
            scene.start()
            scene.is_started = True

        if scene.active and scene.is_started:
            scene.update()

    def _process_input_events(self):

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.shutdown()

            elif event.type == pygame.KEYDOWN:
                self.input_status.keys[pygame.key.name(event.key)] = True

            elif event.type == pygame.KEYUP:
                self.input_status.keys[pygame.key.name(event.key)] = False

            elif event.type == pygame.MOUSEMOTION:
                self.input_status.mouse_position = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.input_status.mouse_buttons = [False] * 5
                self.input_status.mouse_buttons[event.button - 1] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.input_status.mouse_buttons = [False] * 5
                                 
    def _draw(self):
        scene = self.current_scene
        if scene.active and scene.is_started:
            scene.draw()

        scaled = pygame.transform.scale(self.screen, self.window.get_size())
        self.window.blit(scaled, (0,0))

        pygame.display.flip()

    def shutdown(self):
        self.running = False


class InputStatus:
    def __init__(self):
        self.keys = {}
        self.mouse_position = (0,0)
        self.mouse_buttons = [False] * 5