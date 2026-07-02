# NOTE:
# pygbagでのビルド時、main.py 内で pygame をインポートしていないと動作しないケースがあったため残す。

import pygame
import asyncio

from game.package.core.engine import Engine


async def main():
    e = Engine()
    await e.start()
    
if __name__ == "__main__":
    asyncio.run(main())