from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.types import Message

from .configs import BOT_TOKEN
from .parsers import get_message_informations
from .grabber import get_message_details, copy_message

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument


bot_client = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot_client)


@dispatcher.message_handler()
async def handle_all_messages(message: Message):
    chat_message_data = await get_message_informations(message.text)
    message_to_copy = (await get_message_details(chat_message_data['chat_id'], chat_message_data['message_id']))
    sent_media = None
    if(message_to_copy.media):
        print("Downloading media")
        file_bytes = await message_to_copy.download_media(file=bytes)
        if isinstance(message_to_copy.media, MessageMediaPhoto):
            sent_media = await message.reply_photo(file_bytes)
        elif isinstance(message_to_copy.media, MessageMediaDocument):
            if message_to_copy.media.document.mime_type == "video/mp4":
                sent_media = await message.reply_video(file_bytes)
            else:
                sent_media = await message.reply_document(file_bytes)
        print("Done!")
