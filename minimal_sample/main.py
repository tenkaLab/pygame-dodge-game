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


async def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    scene = SampleScene()

    while scene:
        quit_event = False
        input_event = { "keydown": False }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    input_event["keydown"] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space key
                    input_event["keydown"] = True

        if scene:
            scene.update(clock, input_event)

            screen.fill((0, 0, 0))
            scene.render(screen)
            pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())