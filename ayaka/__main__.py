from telebot.util import async_antiflood
from ayaka import Bot, UserBot
from pyrogram import idle
from .server import startServer
import uvloop
import asyncio


async def main():
    try:
        await Bot().start()
        await UserBot().start()
        asyncio.create_task(startServer())
        print("Ayaka Userbot started")
        await idle()
    except Exception as e:
        print(e)
    finally:
        try:
            if Bot().is_connected:
                await Bot().stop()
        except Exception:
            pass
        try:
            if UserBot().is_connected:
                await UserBot().stop()
        except Exception:
            pass


if __name__=="__main__":
    asyncio.run(main())