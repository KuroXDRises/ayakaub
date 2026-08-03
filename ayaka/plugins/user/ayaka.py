from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["ai", "ask"]), group=1)
async def ai_command(c: Client, m: Message):
    parts = m.text.split(None, 1)

    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            "❌ Usage: `/ai <question>` or `/ask <question>`",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return

    query = parts[1].strip()
    username = str((await c.get_users(int(Config.BOT_TOKEN.split(":")[0]))).username)
    result = await c.get_inline_bot_results(
        bot=username,
        query=f"ai {query}"
    )

    if not result.results:
        await m.reply_text(
            "❌ Something went wrong, try again.",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return

    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )
