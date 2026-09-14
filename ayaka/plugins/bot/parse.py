from pyrogram import Client, filters
from pyrogram.types import Message, InputRichMessage
from ayaka import cmd
from ..filters import ADMINS

@Client.on_message(cmd(["parse"]) & ADMINS.message(), group=72)
async def idk_plugin(c:Client, m:Message):
    if len(m.text.split())<2:
        await m.reply("Wrong Format")
    else:
        code = " ".join(m.text.split(" ")[2:])
        await c.send_rich_message(
            chat_id=m.chat.id,
            rich_message=InputRichMessage(html=code)
        )
