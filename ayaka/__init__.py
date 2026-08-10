from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import logging
import time
import uvloop
import asyncio
from config import Config


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("ayaka.log"), logging.StreamHandler()],
    format="[AYAKA]:%(message)s"
)

uvloop.install()
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


class UserBot(Client):
    def __init__(self):
        super().__init__(
            name="userbot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_string=Config.SESSION,
            parse_mode=ParseMode.DEFAULT,
            plugins=(dict(root="ayaka.plugins.user"))
        )

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            parse_mode=ParseMode.DEFAULT,
            plugins=(dict(root="ayaka.plugins.bot"))
        )

bot = Bot()
userbot = UserBot()

uptime:int|float = time.time()

def get_uptime() -> str:
    seconds = int(time.time() - uptime)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days:    parts.append(f"{days}d")
    if hours:   parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")

    return " ".join(parts)

def cmd(commands:list[str], prefixes:list[str]=Config.prefixes):
    return filters.command(commands, prefixes=prefixes)