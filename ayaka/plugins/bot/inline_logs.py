from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton,
    InlineKeyboardMarkup, CallbackQuery,
    InlineQuery, InlineQueryResultArticle,
    InputRichMessageContent, InputRichMessage
)
from ..filters import ADMINS
from pyrogram.enums import ButtonStyle
from config import Config
from datetime import datetime
import os
import html


emojis = {
    "cross": "<tg-emoji emoji-id=6060081662178365254>❌</tg-emoji>",
    "empty": "<tg-emoji emoji-id=5010315921877632081>♨️</tg-emoji>",
    "inbox": "<tg-emoji emoji-id=5253742260054409879>📥</tg-emoji>",
}


def get_size(path: str) -> str:
    size = os.path.getsize(path)
    for unit in ["B", "KB", "MB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def build_logs_text(content: str, max_len: int = 3000):
    total_lines = content.count("\n") + 1
    size = get_size("ayaka.log")
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    truncated = len(content) > max_len
    body = content[-max_len:] if truncated else content
    escaped = html.escape(body)

    text = f"""
<h2>{emojis['inbox']} <b>Bot Logs</b></h2>
<blockquote>📄 {total_lines} lines · 💾 {size} · 🕒 {now}</blockquote>

<pre><code class="language-python">{escaped}</code></pre>
"""
    if truncated:
        text += f"\n{emojis['empty']} <i>Truncated — showing last {max_len} characters.</i>"
    return text, total_lines, size


def logs_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"Clear Logs",
                callback_data="clear_logs",
                style=ButtonStyle.DANGER
            ),
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data="refresh_logs"
            )
        ]
    ])


@Client.on_inline_query(filters.regex(r"^logs") & ADMINS.inline())
async def logs_inline(c: Client, q: InlineQuery):
    if not os.path.exists("ayaka.log"):
        text = f"{emojis['cross']} <b>ayaka.log not found.</b>"
        await q.answer([
            InlineQueryResultArticle(
                thumb_url=Config.main_pic,
                title="❌ No Logs Found",
                input_message_content=InputRichMessageContent(
                    InputRichMessage(text)
                )
            )
        ], cache_time=0)
        return

    with open("ayaka.log", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    if not content:
        text = f"{emojis['empty']} <b>ayaka.log is empty.</b>"
        await q.answer([
            InlineQueryResultArticle(
                thumb_url=Config.main_pic,
                title="♨️ Logs Empty",
                input_message_content=InputRichMessageContent(
                    InputRichMessage(text)
                )
            )
        ], cache_time=0)
        return

    text, total_lines, size = build_logs_text(content)

    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title="📥 Bot Logs",
            description=f"{total_lines} lines · {size}",
            input_message_content=InputRichMessageContent(
                InputRichMessage(text)
            ),
            reply_markup=logs_keyboard()
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^clear_logs$") & ADMINS.callback())
async def clear_logs_callback(c: Client, cq: CallbackQuery):
    if os.path.exists("ayaka.log"):
        open("ayaka.log", "w").close()
    await cq.answer(f"{emojis['inbox']} Logs cleared.", show_alert=True)
    await cq.edit_message_text(f"{emojis['empty']} <b>Logs cleared.</b>")


@Client.on_callback_query(filters.regex(r"^refresh_logs$") & ADMINS.callback())
async def refresh_logs_callback(c: Client, cq: CallbackQuery):
    if not os.path.exists("ayaka.log"):
        await cq.answer(f"{emojis['cross']} ayaka.log not found.", show_alert=True)
        return

    with open("ayaka.log", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    if not content:
        await cq.answer(f"{emojis['empty']} Nothing to show.", show_alert=True)
        return

    text, _, _ = build_logs_text(content)
    await cq.edit_message_text(text, reply_markup=logs_keyboard())
    await cq.answer(f"{emojis['inbox']} Refreshed.")
