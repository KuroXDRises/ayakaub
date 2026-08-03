from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["eval", "e"]) & ADMINS.message(), group=1)
async def eval_command(c: Client, m: Message):
    parts = m.text.split(None, 1)

    if len(parts) < 2 or not parts[1].strip():
        await m.reply_text(
            "❌ No code given.\n\nUsage: `/eval <code>` or `/e <code>`",
            reply_parameters=ReplyParameters(message_id=m.id)
        )
        return
    username = str((await c.get_users(int(Config.BOT_TOKEN.split(":")[0]))).username)
    result = await c.get_inline_bot_results(
        bot=username,
        query=f"eval {parts[1]}"
    )
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )
