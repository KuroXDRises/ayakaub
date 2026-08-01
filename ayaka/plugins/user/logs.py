from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["logs"]) & ADMINS.message(), group=1)
async def logs_command(c: Client, m: Message):
    result = await c.get_inline_bot_results(
        bot=int(Config.BOT_TOKEN.split(":")[0]),
        query="logs"
    )
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )
