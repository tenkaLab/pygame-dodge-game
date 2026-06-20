import asyncio
import pygame
import sys
from game.src import image

class SampleScene:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.is_paused = False
        self.time = 0
        self.image = image.getImage()

    def update(self, clock, input_event):
        if input_event["keydown"]:
            self.is_paused = not self.is_paused
        if not self.is_paused:
            self.time += clock.get_time()

    def render(self, surface):
        text_surface = self.font.render(f"Time: {self.time / 1000:.2f}", True, (255, 255, 255))
        surface.blit(text_surface, (100, 100))
        text_surface = self.font.render("Click/Space to pause/resume", True, (255, 255, 255))
        surface.blit(text_surface, (100, 150))
        surface.blit(self.image, (100, 200))

class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.scene = SampleScene()

    async def loop(self):
        clock = pygame.time.Clock()
        while self.scene:
            quit_event = False
            input_event = { "keydown": False }
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        input_event["keydown"] = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Space key
                        input_event["keydown"] = True

            if self.scene:
                self.scene.update(clock, input_event)

                self.screen.fill((0, 0, 0))
                self.scene.render(self.screen)
                pygame.display.flip()

            clock.tick(60)
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()


async def main():
    e = Engine()
    await e.loop()
    
if __name__ == "__main__":
    asyncio.run(main())
    