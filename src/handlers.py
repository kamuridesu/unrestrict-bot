"""Handlers for handling messages, join groups and more.
"""

import os
import asyncio
import telethon

from tempfile import NamedTemporaryFile
from typing import Callable, Coroutine, Any, Tuple
from aiogram.types import Message, InputFile
from aiogram.utils.exceptions import BadRequest
from telethon.tl.custom.message import Message as TMessage
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    DocumentAttributeFilename,
    Document,
)

from .grabber import get_message_details, join_channel_or_group, client
from .FastTelethon import download_file
from .util import Progress


async def search_for_file_name(attributes: list) -> str:
    for attr in attributes:
        if isinstance(attr, DocumentAttributeFilename):
            return attr.file_name
    return ""


async def get_download_document(message: TMessage) -> Document:
    print(message)


async def get_send_file_function(
    message_to_copy: TMessage, message: Message
) -> Tuple[Callable[[bytes | InputFile], Coroutine[Any, Any, Message]], str] | Tuple[
    None, None
]:
    if isinstance(message_to_copy.media, MessageMediaPhoto):
        return message.reply_photo, ""
    if isinstance(message_to_copy.media, MessageMediaDocument):
        if message_to_copy.media.document.mime_type == "video/mp4":
            return message.reply_video, ""
        else:
            print("Unknown media type! Sending as document")
            print(message_to_copy.media)
            filename = await search_for_file_name(
                message_to_copy.media.document.attributes
            )
            return message.reply_document, filename
    return None, ""


async def forward_message(
    message_to_copy: TMessage, message: Message
) -> Message | None:
    update_message = await message.reply("Checking message")
    progress = Progress(update_message)
    sent_message = None
    if message_to_copy.media:
        await update_message.edit_text("Downloading media")
        print("Downloading media")
        with NamedTemporaryFile("rb+") as file:
            if message_to_copy.document:
                await download_file(
                    client, message_to_copy.media, file, progress.update
                )
            else:
                await message_to_copy.download_media(
                    file=file, progress_callback=progress.update
                )
            await update_message.edit_text("Sending media")
            if function_filename := await get_send_file_function(
                message_to_copy, message
            ):
                function = function_filename[0]
                filename = function_filename[1]
                if filename == "":
                    filename = os.path.basename(file.name)
                file.seek(0)
                for _ in range(10):
                    try:
                        sent_message = await function(
                            InputFile(file.name, filename=filename),
                            caption=message_to_copy.text,
                            parse_mode="Markdown",
                        )
                        break
                    except BadRequest as e:
                        print(f"Failed to send media: {e}! Retrying...")
                        await asyncio.sleep(3)
                else:
                    print("Failed to send media!")
                    return
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
                "Could not download media! Message or chat was probably deleted."
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
