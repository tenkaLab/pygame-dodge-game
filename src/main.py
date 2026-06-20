from game.package.core.engine import Engine
import asyncio

async def main():
    e = Engine()
    print(2)
    await e.start()
    
if __name__ == "__main__":
    
    import pygame
    print(pygame.__version__)
    print(pygame.Vector2)

    asyncio.run(main())