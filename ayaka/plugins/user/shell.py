from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config

SHEL_CACHE = {}

@Client.on_message(cmd(["sh"]) & ADMINS.message(), group=1)
async def sh_command(c: Client, m: Message):
    parts = m.text.split(None, 1)

    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            "❌ Usage: `/sh <command>`",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return

    username = str((await c.get_users(int(Config.BOT_TOKEN.split(":")[0]))).username)

    result = await c.get_inline_bot_results(
        bot=username,
        query=f"sh {parts[1]}"
    )

    if not result.results:
        await m.reply_text(
            "❌ Something went wrong, try again.",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return
    SHEL_CACHE["chat_id"] = m.chat.id
    x = await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )
    SHEL_CACHE["message_id"] = x.id
    SHEL_CACHE["sent_id"] = m.id