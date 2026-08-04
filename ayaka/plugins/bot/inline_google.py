from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineQuery,
    InlineQueryResultArticle, InputRichMessageContent,
    InputRichMessage, InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS


BASE_URL:str = "https://letmegooglethat.com"


def change_text(text:str) -> str:
    words = text.split()
    return "+".join(words)


@Client.on_inline_query(filters.regex(r"^google_it (.+)") & ADMINS.inline())
async def google_inline(c:Client, q:InlineQuery):
    text = q.matches[0].group(1)
    google_url = f"{BASE_URL}/?q={change_text(text)}"
    html = """
    <h3>Google Search</h3>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    <p>I googled it fir you. Click on the button below. :)</p>
    <sup>Inline Result By @AyakaRBot</sup>
    """
    await q.answer([
        InlineQueryResultArticle(
            title="Google",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=html)
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Redirect", url=google_url, style=ButtonStyle.PRIMARY)]
            ])
        )
    ])