import asyncio

from src.grabber import StringSession, client


async def main():
    async with client:
        print(StringSession.save(client.session))
        exit(0)


if __name__ == "__main__":
    asyncio.run(main())
