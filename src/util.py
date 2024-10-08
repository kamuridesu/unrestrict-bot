"""Functions and classes that may be util in the project"""

import time

from aiogram.types import Message
from telethon.tl.custom.message import Message


class Progress:
    """Updates the message with the percentage downloaded"""

    def __init__(self, message: Message):
        self.message = message
        self.enabled = True
        self.start_time = time.perf_counter()

    async def update(self, count: int | float, total: int | float):
        """Updates the message with the download percentage every 10 seconds"""
        if time.perf_counter() - self.start_time > 10:
            self.start_time = time.perf_counter()
            percents = round(100 * count / float(total), 1)
            await self.message.edit_text(f"Downloading... {percents}%")
