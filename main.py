import asyncio

from src.forward import forward_media
from src.grabber import client
from src.sender import dispatcher


async def main():
    async with client:
        # print((await client.get_entity("me")))
        # await forward_media()
        print("Bot started")
        await dispatcher.start_polling()
        # print(StringSession.save(client.session))
        # return


if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(asyncio.gather(task))
    loop.run_forever()
