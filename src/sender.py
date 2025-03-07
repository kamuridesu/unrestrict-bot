"""Sender methods for the bot that sends the contents

It also load the configs and searches for a local web API. If not found, it gives a warning"""

from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.types import Message

from src.configs import API_HOST, BOT_TOKEN
from src.handlers import handle_invite, handle_message
from src.health import HEALTHCHECK
from src.parsers import get_message_informations

bot_client = None
if API_HOST:
    print("Starting BOT with local Telegram API")
    local_server = TelegramAPIServer.from_base(API_HOST)
    bot_client = Bot(BOT_TOKEN, server=local_server)
else:
    print("WARNING: using Telegram's default bot API will limit your bot")
    print("Some of the limits are:")
    print("  20MB limit for downloading files")
    print("  50MB limit for uploading files")
    print("Please, consider running your own bot API server to avoid those limits.")
    bot_client = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot_client)


@dispatcher.message_handler(commands=["start", "help"])
async def send_help(message: Message):
    return await message.reply(
        f"""Send me a link for a public group and I'll forward the message to you.
If you want to save content from a private group, first send me the invite link so I can see the messages too!
My source code: https://github.com/kamuridesu/unrestrict-bot
"""
    )


@dispatcher.message_handler()
async def handle_all_messages(message: Message):
    HEALTHCHECK.healthy()
    chat_message_data = await get_message_informations(message.text)
    if chat_message_data["type"] == "message":
        return await handle_message(message, chat_message_data)
    if chat_message_data["type"] == "invite":
        return await handle_invite(message, chat_message_data["hash"])
