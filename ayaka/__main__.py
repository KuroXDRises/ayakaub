from telebot.util import async_antiflood
from ayaka import bot, userbot
from pyrogram import idle
from .server import startServer
import uvloop
import asyncio


uvloop.install()
async def main():
    try:
        await bot.start()
        await userbot.start()
        asyncio.create_task(startServer())
        print("Ayaka Userbot started")
        await idle()
    except Exception as e:
        print(e)
    finally:
        try:
            if bot.is_connected:
                await bot.stop()
        except Exception:
            pass
        try:
            if userbot.is_connected:
                await userbot.stop()
        except Exception:
            pass


if __name__=="__main__":
    asyncio.run(main())