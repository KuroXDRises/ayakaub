from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery, InlineQuery,
    InlineQueryResultArticle, InputRichMessageContent, InputRichMessage,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS


CACHE = {}


@Client.on_inline_query(filters.regex(r"^(?:whisper|w) (\S+) (.+)") & ADMINS.inline(), group=-69)
async def whisper_inline(c: Client, q: InlineQuery):
    match = q.matches[0]
    username = match.group(1)
    text = match.group(2)

    # accept "@username", "username", or a numeric user id
    if username.startswith("@"):
        username = username[1:]
    elif username.lstrip("-").isdigit():
        username = int(username)

    try:
        target = await c.get_users(username)
    except Exception:
        await q.answer([
            InlineQueryResultArticle(
                title="❌ User Not Found",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(
                        html=f"<b>❌ Could not find user:</b> {username}"
                    )
                )
            )
        ], cache_time=0)
        return

    CACHE[target.id] = text

    await q.answer([
        InlineQueryResultArticle(
            title=f"Whisper Message To: {target.first_name}",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(
                    html=(
                        f"<h3>Whisper Message</h3>"
                        f"<aside>A Whisper Message to {target.first_name}. Only he can read this message.</aside>"
                        f"<sup>Sent via AyakaRBot</sup>"
                    )
                )
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "《 𝗥𝗲𝗮𝗱 𝗧𝗵𝗶𝘀 》",
                    callback_data=f"whisper:{target.id}",
                    style=ButtonStyle.PRIMARY
                )]
            ])
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^whisper:"), group=-70)
async def whisper_button(c: Client, call: CallbackQuery):
    id = int(call.data.split(":", 1)[1])

    if call.from_user.id != id:
        await call.answer("This whisper is not for you.", show_alert=True)
        return

    text = CACHE.pop(id, None)
    if not text:
        await call.answer("You already opened the whisper.", show_alert=True)
        return

    await call.answer(text, show_alert=True)
    await c.edit_inline_text(
        inline_message_id=call.inline_message_id,
        rich_message=InputRichMessage(html="<h3>Message Opened</h3>"),
        reply_markup=None
    )
