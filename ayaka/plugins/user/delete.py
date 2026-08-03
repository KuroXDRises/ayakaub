from pyrogram import Client, filters
from pyrogram.types import Message
from ..filters import ADMINS
from ayaka import cmd
import asyncio

@Client.on_message(cmd(["del", "delete"]) & ADMINS.message(), group=-1)
async def delete_command(c:Client, m:Message):
    r = m.reply_to_message
    if not r:
        return
    await r.delete()
    await m.delete()

@Client.on_message(cmd(["purge"]) & filters.group & ADMINS.message(), group=-2)
async def purge_command(c:Client, m:Message):
    r = m.reply_to_message
    if not r:
        return
    from_msg_id:int = r.id
    to_msg_id:int = m.id
    count:int = 0
    for i in range(from_msg_id, to_msg_id):
        try:
            count += await c.delete_messages(chat_id=m.chat.id, message_ids=i, revoke=True)
            await asyncio.sleep(0.5)
        except Exception:
            await m.reply("`[ERROR]:An Unexpected Error Occur While Purging.`")
    await m.reply(f"`[PURGE]:Purged {count} message in chat {m.chat.title}`")