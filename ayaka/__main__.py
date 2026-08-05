from ayaka import bot, userbot
from pyrogram import idle
from .server import startServer
import uvloop
import asyncio
import traceback


uvloop.install()


async def main():
    try:
        await bot.start()
        print("Bot client started")
        await userbot.start()
        print("Userbot client started")
        asyncio.create_task(startServer())
        print("Ayaka Userbot started")
        await idle()
    except Exception:
        traceback.print_exc()
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


if __name__ == "__main__":
    asyncio.run(main())
