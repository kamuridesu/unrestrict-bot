"""Grabs the content using a user account

This account may join the chat to be able to see the contents too
"""

import datetime

from telethon import TelegramClient, functions, types
from telethon.errors.rpcerrorlist import (
    ChannelPrivateError,
    FloodWaitError,
    UserAlreadyParticipantError,
)
from telethon.sessions import StringSession
from telethon.tl.custom.message import Message
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputMessagesFilterPhotoVideo

from src.configs import API_HASH, API_ID, SESSION_STRING

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


async def get_public_chat_id_from_name(chat_name: str) -> int:
    return await client.get_peer_id(chat_name)


async def get_message_details(
    chat_id: str | int, message_id: str | int
) -> Message | None:
    try:
        return await client.get_messages(chat_id, ids=message_id)
    except (ValueError, ChannelPrivateError) as e:
        print(str(e))


async def join_channel_or_group(invite_link_hash: str) -> dict[str, str | bool]:
    try:
        updates = await client(ImportChatInviteRequest(invite_link_hash))
        chat_id = updates.chats[0].id
        await client.edit_folder(chat_id, 1)  # archive chat
        client(
            functions.account.UpdateNotifySettingsRequest(
                peer=chat_id,
                settings=types.InputPeerNotifySettings(
                    mute_until=datetime.datetime(2050, 12, 12)
                ),
            )
        )
        return {"error": False}
    except (UserAlreadyParticipantError, FloodWaitError) as e:
        return {"error": True, "message": str(e)}


async def get_chat_history(chat_id: str, min_id=0):
    async for message in client.iter_messages(
        chat_id, reverse=True, filter=InputMessagesFilterPhotoVideo, min_id=min_id
    ):
        yield message
