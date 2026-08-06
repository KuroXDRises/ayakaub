from openai.types.video_create_params import InputReference
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineQuery, CallbackQuery,
    InlineQueryResultArticle, InputRichMessageContent,
    InputRichMessage, InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS
from ayaka import get_uptime
from config import Config


def rich_text_setup() -> str:
    up = get_uptime()
    return f"""
<img src="{Config.main_pic}"/>
<h1>AYAKA</h1>
<p>A powerful <b>Telegram Userbot</b> built with Kurigram.</p>
<hr/>
<details><summary>Status</summary>
<table bordered striped>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>Uptime</td><td><code>{up}</code></td></tr>
<tr><td>Status</td><td><code>Online</code></td></tr>
<tr><td>Version</td><td><code>1.0.0</code></td></tr>
</table>
</details>
<hr/>
<details><summary>Commands</summary>
<table bordered striped>
<tr><th>Command</th><th>Description</th></tr>
<tr><td><code>.eval</code></td><td>Execute Python code</td></tr>
<tr><td><code>.sh</code></td><td>Run a shell command</td></tr>
<tr><td><code>.ping</code></td><td>Latency and uptime</td></tr>
<tr><td><code>.logs</code></td><td>Loggings of the bot.</td></tr>
</table>
</details>
<hr/>
<footer>Made by <a href="https://t.me/KuroXDRises">KuroXDRises</a></footer>
"""


@Client.on_inline_query(filters.regex(r"^alive") & ADMINS.inline())
async def inline(c:Client, q:InlineQuery):
   await q.answer([
       InlineQueryResultArticle(
           title="About Ayaka",
           thumb_url=Config.main_pic,
           input_message_content=InputRichMessageContent(
               rich_message=InputRichMessage(html=rich_text_setup())
           ),
           reply_markup=InlineKeyboardMarkup([
               [InlineKeyboardButton("《 Repo 》", url="https://github.com/KuroXDRises/ayakaub", style=ButtonStyle.SUCCESS)],
               [InlineKeyboardButton("《 Owner 》", url="https://t.me/KuroXDRises", style=ButtonStyle.PRIMARY)]
           ])
       )
   ])


@Client.on_message(filters.command('start') & filters.private, group=1)
async def start_command(c:Client, m:Message):
    await c.send_rich_message(
        chat_id=m.chat.id,
        rich_message=InputRichMessage(html=rich_text_setup()),
        reply_markup=InlineKeyboardMarkup([
               [InlineKeyboardButton("《 Repo 》", url="https://github.com/KuroXDRises/ayakaub", style=ButtonStyle.SUCCESS)],
               [InlineKeyboardButton("《 Owner 》", url="https://t.me/KuroXDRises", style=ButtonStyle.PRIMARY)]
           ])
    )