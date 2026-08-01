from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton,
    InlineKeyboardMarkup, CallbackQuery,
    InlineQuery, InlineQueryResultArticle,
    InputTextMessageContent
)
from ..filters import ADMINS
from ..utilities.dev import get_sh_output, eval_helper
from config import Config
import re

PASTE_RE = re.compile(r"\n*\.\.\. output too long, full result: (https://pastebin\.com/\S+)\s*$")


def build_sh_result(cmd: str, raw_result: str):
    match = PASTE_RE.search(raw_result)
    paste_url = None

    if match:
        paste_url = match.group(1)
        result_text = raw_result[:match.start()].rstrip()
    else:
        result_text = "Command Executed." if raw_result == "Done." else raw_result

    text = (
        f"╭─────────────────╮\n"
        f"         📟 **Shell Output**\n"
        f"╰─────────────────╯\n\n"
        f"**Command:**\n```bash\n{cmd}\n```\n\n"
        f"**Result:**\n"
        f"<blockquote>{result_text}</blockquote>"
    )
    if paste_url:
        text += "\n_Output truncated — full result on Pastebin._"

    buttons = [InlineKeyboardButton("🗑 Close", callback_data="close_sh")]
    if paste_url:
        buttons.insert(0, InlineKeyboardButton("📄 See Full Output", url=paste_url))

    return text, InlineKeyboardMarkup([buttons])


@Client.on_inline_query(filters.regex(r"^sh\s") & ADMINS.inline())
async def sh_inline(c: Client, q: InlineQuery):
    parts = q.query.split(None, 1)

    if len(parts) < 2 or not parts[1].strip():
        text = "❌ No command given.\n\nUsage: `sh <command>`"
        await q.answer([
            InlineQueryResultArticle(
                thumb_url=Config.main_pic,
                title="❌ No Command Given",
                input_message_content=InputTextMessageContent(text)
            )
        ], cache_time=0)
        return

    cmd = parts[1]

    eval_helper["code"] = cmd
    eval_helper["chat_id"] = q.from_user.id

    raw_result = await get_sh_output(parts, c, None)
    eval_helper["result"] = raw_result

    text, keyboard = build_sh_result(cmd, raw_result)

    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title="📟 Shell Result",
            description=(raw_result[:60] if raw_result else "Command Executed."),
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^close_sh$") & ADMINS.callback())
async def close_sh_callback(c: Client, cq: CallbackQuery):
    await cq.message.delete()
    await cq.answer("Closed.")
