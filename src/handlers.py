import telethon

from typing import Callable, Coroutine, Any
from aiogram.types import Message
from telethon.tl.custom.message import Message as TMessage
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage

from .grabber import get_message_details, join_channel_or_group
from .util import Progress


async def get_send_file_function(
    message_to_copy: TMessage, message: Message
) -> Callable[[bytes], Coroutine[Any, Any, Message]] | None:
    if isinstance(message_to_copy.media, MessageMediaPhoto):
        return message.reply_photo
    if isinstance(message_to_copy.media, MessageMediaDocument):
        if message_to_copy.media.document.mime_type == "video/mp4":
            return message.reply_video
        else:
            print("Unknown media type! Sending as document")
            print(message_to_copy.media)
            return message.reply_document
    return None


async def forward_message(
    message_to_copy: TMessage, message: Message
) -> Message | None:
    update_message = await message.reply("Checking message")
    progress = Progress(update_message)
    sent_message = None
    if message_to_copy.media:
        await update_message.edit_text("Downloading media")
        print("Downloading media")
        file_bytes: bytes = await message_to_copy.download_media(
            file=bytes, progress_callback=progress.update
        )
        await update_message.edit_text("Sending media")
        if function := await get_send_file_function(message_to_copy, message):
            sent_message = await function(file_bytes)
        else:
            sent_message = await message.reply(message_to_copy.text)
    await update_message.delete()
    print("Done!")
    return sent_message


async def handle_message(message: Message, chat_message_data: dict[str, Any]):
    try:
        message_to_copy = await get_message_details(
            chat_message_data["chat_id"], chat_message_data["message_id"]
        )
        sent_message = None
        if message_to_copy is None:
            return await message.reply(
                "Could not download media! Message was probably deleted."
            )
        if await forward_message(message_to_copy, message) is None:
            return await message.reply("Could not send media!")
    except telethon.errors.rpcerrorlist.FloodWaitError as e:
        sent_message = await message.reply(f"Failed to send the file! Reason: {e}")
    return sent_message


async def handle_invite(message: Message, chat_hash: str):
    sent_message = await message.reply("Joining group...")
    join_report = await join_channel_or_group(chat_hash)
    if join_report["error"]:
        return await sent_message.edit_text(join_report["message"])
    return await sent_message.edit_text("Group joined!")
