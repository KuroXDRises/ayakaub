from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["help"]) & ADMINS.message() & (filters.group), group=999)
async def help_command(c:Client, m:Message):
    results = await c.get_inline_bot_results(
        bot=Config.BOT_USERNAME,
        query="help"
    )
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=results.query_id,
        result_id=results.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )