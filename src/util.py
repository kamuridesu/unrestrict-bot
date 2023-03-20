import time
from typing import Callable, Coroutine, Any
from aiogram.types import Message
from telethon.tl.custom.message import Message as TMessage
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


class Progress:
    """Updates the message with the percentage downloaded"""

    def __init__(self, message: Message):
        self.message = message
        self.enabled = True
        self.start_time = time.perf_counter()

    async def update(self, count, total):
        """Updates the message with the download percentage every 10 seconds"""
        if time.perf_counter() - self.start_time > 10:
            self.start_time = time.perf_counter()
            percents = round(100 * count / float(total), 1)
            await self.message.edit_text(f"Downloading... {percents}%")


async def get_send_file_function(
    message_to_copy: TMessage, message: Message
) -> Callable[[bytes], Coroutine[Any, Any, Message]] | None:
    if isinstance(message_to_copy.media, MessageMediaPhoto):
        return message.reply_photo
    elif isinstance(message_to_copy.media, MessageMediaDocument):
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
    update_message = await message.reply("Downloading media")
    progress = Progress(update_message)
    sent_message = None
    if message_to_copy.media:
        print("Downloading media")
        file_bytes = await message_to_copy.download_media(
            file=bytes, progress_callback=progress.update
        )
        await update_message.edit_text("Sending media")
        if function := await get_send_file_function(message_to_copy, message):
            sent_message = await function(file_bytes)
        await update_message.delete()
        print("Done!")
        return sent_message
    return None
