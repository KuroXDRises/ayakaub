import re
from html import escape
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    ChosenInlineResult,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from ..data.premdb import premiumEmojiMethods
from ..filters import ADMINS
from ..utilities.dev import eval_helper

TAG = re.compile(r'<tg-emoji emoji-id="(\d+)">')


def to_pyro(html: str) -> str:
    return TAG.sub(r'<emoji id="\1">', html).replace("</tg-emoji>", "</emoji>")


@Client.on_inline_query(filters.regex(r"^prem (.+)")& ADMINS.inline(), group=564)
async def prem_inline(c: Client, q: InlineQuery):
    token = q.query.split()[1]
    await q.answer([
        InlineQueryResultArticle(
            id=f"prem_{token}",
            title="Premium Emoji",
            input_message_content=InputTextMessageContent("⏳ Please wait..."),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⏳ Processing", callback_data="prem_wait")]])
        )
    ], cache_time=0)


@Client.on_chosen_inline_result(filters.create(lambda _, __, r: r.result_id.startswith("prem_")), group=565)
async def prem_chosen(c: Client, r: ChosenInlineResult):
    text = eval_helper.pop(f"emojify_{r.result_id[5:]}", None)
    if text is None or not r.inline_message_id:
        return
    out = await premiumEmojiMethods.generate_premium_text(text)
    for candidate in (to_pyro(out), out, escape(text)):
        try:
            await c.edit_inline_text(r.inline_message_id, candidate, parse_mode=ParseMode.HTML)
            return
        except Exception:
            continue
    await c.edit_inline_text(r.inline_message_id, "❌ Failed")