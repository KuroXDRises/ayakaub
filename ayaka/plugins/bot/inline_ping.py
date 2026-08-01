from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputRichMessageContent, InputRichMessage
from ..filters import ADMINS
from ayaka import get_uptime
from ..utilities.dev import eval_helper
from config import Config
import sys



@Client.on_inline_query(filters.regex(r'^stats') & ADMINS.inline())
async def ping_inline(c:Client, q:InlineQuery):
    up = get_uptime()
    latency = eval_helper["latency"]
    text = f"""
    <h2><tg-emoji emoji-id=5413718040799899278>📊</tg-emoji> Bot Stats</h2>
    <hr>
    <table bordered striped>
    <tr>
        <th align="center">Metric</th>
        <th align="center">Value</th>
    </tr>
    <tr>
        <td align="center"><tg-emoji emoji-id=5206558904686748715>🏓</tg-emoji>Latency</td>
        <td align="center"><mark>{latency}</mark></td>
    </tr>
    <tr>
       <td align="center"><tg-emoji emoji-id=6039391666547201160>⚠️</tg-emoji>Uptime</td>
       <td align="center"><mark>{up}</mark></td>
    </tr>
    <tr>
        <td align="center"><tg-emoji emoji-id=5260480440971570446>♨️</tg-emoji>Python</td>
        <td align="center"><mark>{sys.version.split()[0]}</mark></td>
    </tr>
    </table>
    <aside>
    Ayaka is running smoothly with optimized performance.

    <cite>Ayaka-Userbot</cite>
    </aside>

    <hr/>

    <p><i>Inline Stats Panel • Live Data</i></p>
    """
    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title="📊 Bot Statistics",
            input_message_content=InputRichMessageContent(
                InputRichMessage(text)
            )
        )
    ], cache_time=0)