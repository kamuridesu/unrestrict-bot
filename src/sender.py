from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.bot.api import TelegramAPIServer

from .configs import BOT_TOKEN, API_HOST
from .parsers import get_message_informations
from .grabber import get_message_details
from .util import Progress

from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import telethon

local_server = TelegramAPIServer.from_base(API_HOST)
bot_client = Bot(BOT_TOKEN, server=local_server)
dispatcher = Dispatcher(bot_client)


@dispatcher.message_handler(commands=["start", "help"])
async def send_help(message: Message):
    return await message.reply("Send me a link for a public group and I'll forward the message to you")


@dispatcher.message_handler()
async def handle_all_messages(message: Message):
    try:
        chat_message_data = await get_message_informations(message.text)
        message_to_copy = (await get_message_details(chat_message_data['chat_id'], chat_message_data['message_id']))
        sent_message = None
        if message_to_copy is None:
            return await message.reply("Could not download media! Message was probably deleted.")
        update_message = await message.reply("Downloading media")
        progress = Progress(update_message)
        if(message_to_copy.media):
            print("Downloading media")
            file_bytes = await message_to_copy.download_media(file=bytes, progress_callback=progress.update)
            await update_message.edit_text("Sending media")
            if isinstance(message_to_copy.media, MessageMediaPhoto):
                sent_message = await message.reply_photo(file_bytes)
            elif isinstance(message_to_copy.media, MessageMediaDocument):
                if message_to_copy.media.document.mime_type == "video/mp4":
                    sent_message = await message.reply_video(file_bytes)
                else:
                    print("Unknown media type! Sending as document")
                    print(message_to_copy.media)
                    sent_message = await message.reply_document(file_bytes)
            await update_message.delete()
            print("Done!")
    except (telethon.errors.rpcerrorlist.FloodWaitError) as e:
        sent_message = await message.reply(f"Failed to send the file! Reason: {e}")
