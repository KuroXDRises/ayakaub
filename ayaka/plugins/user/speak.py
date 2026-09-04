from ayaka import cmd
from pyrogram import Client, filters
from pyrogram.types import (
    Message, ReplyParameters,
    )
from ..filters import ADMINS
from ..utilities.speak import Speak


@Client.on_message(cmd(["speak"]) & ADMINS.message(), group=43)
async def speak_query(c:Client, m:Message):
    if len(m.text.split())<2:
        return
    query = " ".join(m.text.split(" ", 1)[1:])
    file = await Speak(text=query).save()
    await c.send_audio(
        chat_id=m.chat.id,
        audio=file,
    )