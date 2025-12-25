import asyncio
from cron import run


async def async_main():
    await run()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    asyncio.run(async_main())