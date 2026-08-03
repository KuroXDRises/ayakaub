from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import ReplyParameters
from ..filters import ADMINS
from ..utilities.dev import eval_helper
from ayaka import cmd
from config import Config
import time


@Client.on_message(cmd(["ping", "stats"]) & ADMINS.message(), group=1)
async def ping_command(c:Client, m:Message):
    start = time.perf_counter()
    x = await c.send_message(
        chat_id=m.chat.id,
        text="🏓 Pinging..."
    )
    latency = round((time.perf_counter()-start)*1000)
    eval_helper["latency"] = latency
    username = str((await c.get_users(int(Config.BOT_TOKEN.split(":")[0]))).username)
    result = await c.get_inline_bot_results(
        bot=username,
        query="stats"
    )
    await x.delete()
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=result.query_id,
        result_id=result.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.id)
    )