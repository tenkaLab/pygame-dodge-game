from game.package.core.engine import Engine
import asyncio

async def main():
    e = Engine()
    await e.start()

if __name__ == "__main__":
    asyncio.run(main())