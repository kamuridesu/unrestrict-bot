from telethon import TelegramClient, events
from telethon.sessions import StringSession
from .configs import API_HASH, API_ID, SESSION_STRING


client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


async def get_public_chat_id_from_name(chat_name: str):
    return await client.get_peer_id(chat_name)


async def get_message_details(chat_id: str | int, message_id: str | int):
    return await client.get_messages(chat_id, ids=message_id)


async def copy_message(target_chat_id: str | int, message):
    return await client.send_message(target_chat_id, message)