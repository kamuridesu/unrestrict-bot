"""Configuratioin file, DO NOT CHANGE!

Attributes:
    - `API_ID`: id for Telegram's API
    - `API_HASH`: hash for Telegram's API
    - `STRING_SESSOIN`: string containing information about a sessoin
    - `BOT_TOKEN`: Token for the bot that sends the media
    - `API_HOST`: Host for Telegram's bot API
"""

import os


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_HOST = os.getenv("API_HOST")
