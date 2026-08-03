from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ayaka import cmd
from ..filters import ADMINS
from config import Config


@Client.on_message(cmd("alive") & ADMINS.message(), group=2)
async def alive_command(c:Client, m:Message):
    username = str((await c.get_users(int(Config.BOT_TOKEN.split(":")[0]))).username)
    result = await c.get_inline_bot_results(
        bot=username,
        query=""
    )
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )