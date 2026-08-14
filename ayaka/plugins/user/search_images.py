from pyrogram import Client, filters
from pyrogram.types import Message
from ..filters import ADMINS
from ..utilities.images import get_images
from ayaka import cmd
import asyncio


@Client.on_message(cmd(["search_img"]) & ADMINS.message(), group=14)
async def search_img_command(userbot:Client, message:Message):
    if len(message.command)<2:
        await message.reply("**Usage:** .search_img {img}")
    else:
        try:
            image_query = " ".join(message.command[1:])
            images = await get_images(image_query)
            if not images:
                await message.reply("**No images found.**")
            else:
                for image in images:
                    await message.reply_photo(
                        photo=image,
                        caption=f"`{image_query}`"
                    )
                    await asyncio.sleep(1)
                await message.reply("**Search successful**")
        except Exception as e:
            await message.reply(str(e))