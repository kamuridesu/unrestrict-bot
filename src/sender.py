from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.bot.api import TelegramAPIServer

from .configs import BOT_TOKEN, API_HOST
from .parsers import get_message_informations
from .handlers import handle_message, handle_invite


local_server = TelegramAPIServer.from_base(API_HOST)
bot_client = Bot(BOT_TOKEN, server=local_server)
dispatcher = Dispatcher(bot_client)


@dispatcher.message_handler(commands=["start", "help"])
async def send_help(message: Message):
    return await message.reply(
        "Send me a link for a public group and I'll forward the message to you"
    )


@dispatcher.message_handler()
async def handle_all_messages(message: Message):
    chat_message_data = await get_message_informations(message.text)
    if chat_message_data["type"] == "message":
        return await handle_message(message, chat_message_data)
    if chat_message_data["type"] == "invite":
        return await handle_invite(message, chat_message_data["hash"])
    return await message.reply("Invalid message type!")
