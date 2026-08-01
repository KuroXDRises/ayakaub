from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputRichMessageContent, InputRichMessage, InlineQuery
from ..filters import ADMINS


@Client.on_inline_query(filters.regex("parse (.+)") & ADMINS.inline())
async def parse_inline(c:Client, q:InlineQuery):
    html = q.matches[0].group(1)
    await q.answer([
        InlineQueryResultArticle(
            title="Rich Text",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=html)
            )
        )
    ], cache_time=0)