from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config

AI_CACHE = {}

@Client.on_message(cmd(["ai", "ask"]) & ADMINS.message(), group=1)
async def ai_command(c: Client, m: Message):
    parts = m.text.split(None, 1)

    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            "❌ Usage: `/ai <question>` or `/ask <question>`",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return

    query = parts[1].strip()
    result = await c.get_inline_bot_results(
        bot=Config.BOT_USERNAME,
        query=f"ai {query}"
    )

    if not result.results:
        await m.reply_text(
            "❌ Something went wrong, try again.",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return

    x = await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )
    AI_CACHE["chat_id"] = m.chat.id
    AI_CACHE["message_id"] = x.id
    AI_CACHE["sent_id"] = m.id