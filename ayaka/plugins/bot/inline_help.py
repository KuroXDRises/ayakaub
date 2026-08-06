from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery, InlineQueryResultArticle,
    InputRichMessageContent, InputRichMessage
)
from .help import build_help_message, build_home_keyboard
from ..filters import ADMINS
from config import Config


@Client.on_inline_query(filters.regex(r"^help") & ADMINS.inline(), group=869)
async def help_inline(c: Client, q: InlineQuery):
    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title="📖 Ayaka Help",
            description="Browse all commands",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=build_help_message())
            ),
            reply_markup=build_home_keyboard()
        )
    ], cache_time=0)
