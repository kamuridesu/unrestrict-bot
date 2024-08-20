import json
import os
from asyncio import sleep

from telethon.errors.rpcbaseerrors import FloodError

from src.grabber import client, get_chat_history

FROM = os.getenv("FORWARD_FROM")
TO = os.getenv("FORWARD_TO")


def save_sent(sent: list):
    with open("sent.json", "w") as f:
        json.dump(sent, f, ensure_ascii=False)


def load():
    try:
        with open("sent.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


ALREADY_SENT: list = load()


async def forward_media():
    print("bot started!")
    messages = []
    async for message in get_chat_history(
        FROM, ALREADY_SENT[-1] if len(ALREADY_SENT) > 0 else 0
    ):
        if len(messages) > 500:
            print(f"forwarding {len(messages)} messages")
            for _ in range(2):
                try:
                    await client.forward_messages(TO, messages, FROM)
                    break
                except FloodError as e:
                    if "A wait of" in str(e):
                        time = str(e).split("A wait of")[1].split(" seconds")[0].strip()
                        if time.isdecimal():
                            print("Sleeping for " + time + " seconds")
                            await sleep(int(time))
                print("Retrying...")
            ALREADY_SENT.extend(messages)
            save_sent(ALREADY_SENT)
            messages.clear()
        if message.id not in ALREADY_SENT:
            print(f"Adding message {message.id} into batch")
            messages.append(message.id)
    if len(messages) > 0:
        print(f"forwarding {len(messages)} messages")
        await client.forward_messages(TO, messages, FROM)
        ALREADY_SENT.extend(messages)
        save_sent(ALREADY_SENT)
    print("done!")
