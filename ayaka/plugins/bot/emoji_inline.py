import re
import uuid
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    CallbackQuery,
    ChosenInlineResult,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from ..data.premdb import premiumEmojiMethods
from ..filters import ADMINS

CACHE = {}
CACHE_LIMIT = 200
CB_CONVERT = "conv_emoji"


@Client.on_inline_query(filters.regex(r"^prem (.+)", flags=re.DOTALL) & ADMINS.inline(), group=564)
async def inline_emoji(c: Client, q: InlineQuery):
    raw = q.matches[0].group(1)
    styled = await premiumEmojiMethods.generate_premium_text(raw)
    key = uuid.uuid4().hex
    CACHE[key] = styled
    while len(CACHE) > CACHE_LIMIT:
        CACHE.pop(next(iter(CACHE)))
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🪄 Processing...", callback_data=f"{CB_CONVERT}:{key}")
    ]])
    await q.answer([
        InlineQueryResultArticle(
            id=key,
            title="🪄 Please Wait...",
            input_message_content=InputTextMessageContent(
                message_text="🪄 Applying Premium Emojis...."
            ),
            reply_markup=keyboard
        )
    ], cache_time=0)


async def apply_premium_emoji(c: Client, inline_message_id: str, key: str) -> bool:
    text = CACHE.pop(key, None)
    if not text:
        return False
    try:
        await c.edit_inline_text(
            inline_message_id=inline_message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=None
        )
        return True
    except Exception as e:
        print("Emoji conversion error:", e)
        return False


@Client.on_chosen_inline_result(group=565)
async def on_chosen(c: Client, r: ChosenInlineResult):
    if not r.inline_message_id:
        return
    await apply_premium_emoji(c, r.inline_message_id, r.result_id)


@Client.on_callback_query(filters.regex(rf"^{CB_CONVERT}:"), group=566)
async def on_processing_button(c: Client, cq: CallbackQuery):
    key = cq.data.split(":", 1)[1]
    done = await apply_premium_emoji(c, cq.inline_message_id, key)
    await cq.answer("Done!" if done else "Already processed.")