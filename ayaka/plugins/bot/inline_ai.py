from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery, InlineQueryResultArticle,
    InputRichMessageContent, InputRichMessage,
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)
from pyrogram.enums import ButtonStyle
from ayaka import userbot
from ..user.ayaka import AI_CACHE
from ..utilities.ai import AyakaAI
from config import Config


@Client.on_inline_query(filters.regex(r"^(?:ai|ask) (.+)"), group=-50)
async def ai_inline(c: Client, q: InlineQuery):
    match = q.matches[0]
    query = match.group(1).strip()

    if not query:
        await q.answer([
            InlineQueryResultArticle(
                thumb_url=Config.main_pic,
                title="❌ No Question Given",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(html="<b>❌ Please provide a question.</b>")
                )
            )
        ], cache_time=0)
        return

    ai = AyakaAI()
    html = await ai.query(query)

    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title=f"🤖 {query[:60]}",
            description="Ask AyakaAI",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=html)
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑 Close", callback_data="close_ai", style=ButtonStyle.DANGER)]
            ])
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^close_ai$"), group=-51)
async def close_ai_callback(c: Client, cq: CallbackQuery):
    await userbot.delete_messages(
        chat_id=AI_CACHE['chat_id'],
        message_ids=[AI_CACHE["message_id"], AI_CACHE["sent_id"]]
    )
    await cq.answer("Closed.")