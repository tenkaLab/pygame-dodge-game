import pygame
import asyncio

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

        self.scenes = config.scenes

        init_scene_index = config.game["initial_scene_index"]
        self.current_scene = self.scenes[init_scene_index]()

        self.max_tps = config.game["max_tps"]
        self.max_fps = config.game["max_fps"]

        self.delta_time = 0

        self.input_status = InputStatus()

        self.scheduler = Scheduler()

        self.debug_settings = config.debug

        self.global_values = config.global_values

    async def start(self):
        self.running = True
        await self._loop()

    def change_scene(self, index):
        self.current_scene = self.scenes[index]()

    def shutdown(self):
        self.running = False

    async def _loop(self):
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
            await asyncio.sleep(0)  

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
        self._process_events()
        self.scheduler.update(self.delta_time)

        scene = self.current_scene
        
        if not scene.is_started:  
            scene.engine = self
            scene.start()
            scene.is_started = True

        if scene.active and scene.is_started:
            scene.update()

    def _process_events(self):

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.shutdown()

            elif event.type == pygame.KEYDOWN:
                self.input_status.keys[pygame.key.name(event.key)] = True

                if self.debug_settings["print_key_events"]:
                    print(pygame.key.name(event.key))

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
        self.screen.fill((0, 0, 0))

        scene = self.current_scene
        if scene.active and scene.is_started:
            scene.draw()

        scaled = pygame.transform.scale(self.screen, self.window.get_size())
        self.window.blit(scaled, (0,0))

        pygame.display.flip()


class InputStatus:
    def __init__(self):
        self.keys = {}
        self.mouse_position = (0,0)
        self.mouse_buttons = [False] * 5

class Scheduler:
    def __init__(self):
        self.events = []

    def schedule_event(self, delay, callback, *args, **kwargs):
        self.events.append({
            "time": delay,
            "callback": callback,
            "args" : args,
            "kwargs" : kwargs
        })

    def update(self, delta_time):
        for event in self.events[:]:
            event["time"] -= delta_time

            if event["time"] <= 0:
                event["callback"](
                    *event["args"],
                    **event["kwargs"]
                )
                self.events.remove(event)