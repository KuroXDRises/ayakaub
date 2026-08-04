from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton,
    InlineKeyboardMarkup, CallbackQuery,
    InlineQuery, InlineQueryResultArticle,
    InputTextMessageContent
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS
from ..utilities.dev import get_sh_output, eval_helper
from ..user.shell import SHEL_CACHE
from ayaka import userbot
from config import Config
import re

PASTE_RE = re.compile(r"\n*\.\.\. output too long, full result: (https://pastebin\.com/\S+)\s*$")
SEP = "━━━━━━━━━━━━━━━━━━━━"


def build_sh_result(cmd: str, raw_result: str):
    match = PASTE_RE.search(raw_result)
    paste_url = None

    if match:
        paste_url = match.group(1)
        result_text = raw_result[:match.start()].rstrip()
    else:
        result_text = "Command Executed." if raw_result == "Done." else raw_result

    text = (
        f"📟 **Shell Output**\n"
        f"{SEP}\n"
        f"**Command:**\n```bash\n{cmd}\n```\n"
        f"{SEP}\n"
        f"**Result:**\n"
        f"<blockquote>{result_text}</blockquote>"
    )
    if paste_url:
        text += f"\n{SEP}\n_Output truncated — full result on Pastebin._"

    buttons = [InlineKeyboardButton("🗑 Close", callback_data="close_sh", style=ButtonStyle.DANGER)]
    if paste_url:
        buttons.insert(0, InlineKeyboardButton("📄 See Full Output", url=paste_url, style=ButtonStyle.PRIMARY))

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

    cmd_text = parts[1]

    eval_helper["code"] = cmd_text
    eval_helper["chat_id"] = q.from_user.id

    raw_result = await get_sh_output(parts, c, None)
    eval_helper["result"] = raw_result

    text, keyboard = build_sh_result(cmd_text, raw_result)

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
    await userbot.delete_messages(
        chat_id=SHEL_CACHE["chat_id"],
        message_ids=[SHEL_CACHE["message_id"], SHEL_CACHE["sent_id"]]
    )
    await cq.answer("Closed.")
