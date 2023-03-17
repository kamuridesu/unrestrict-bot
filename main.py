import asyncio

from src.grabber import client, StringSession
from src.sender import dispatcher

async def main():
    async with client:
        print("bot started!")
        await dispatcher.start_polling()
        # executor.start_polling(dispatcher)
        # await client.run_until_disconnected()


if __name__ == "__main__":
    # print("bot started!")
    asyncio.run(main())
    
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(main())
    # loop.run_until_complete(asyncio.gather(task))
    # loop.run_forever()