import cmath
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardButton,
    InlineKeyboardMarkup, CallbackQuery,
    InlineQuery, InlineQueryResultArticle,
    InputTextMessageContent
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS
from ..utilities.dev import get_output, eval_helper
from ..user.eval import EVAL_CACHE
from config import Config
from ayaka import userbot
import re

PASTE_RE = re.compile(r"\n*\.\.\. output too long, full result: (https://pastebin\.com/\S+)\s*$")
SEP = "━━━━━━━━━━━━━━━━━━━━"


class _FakeChat:
    def __init__(self, id_):
        self.id = id_


class _FakeMsg:
    """Stand-in for a Message so aexec() in dev.py works from an InlineQuery.

    Prefers a "pending" identity handed off by a command handler (see
    eval.py) right before it relayed through get_inline_bot_results — that
    relay makes the bot query itself, so q.from_user would otherwise
    resolve to the BOT, not the admin who actually ran the command.
    Falls back to q.from_user for genuine live inline typing, where
    q.from_user is already the real person typing.
    """
    def __init__(self, q: InlineQuery):
        pending_user = eval_helper.get("pending_user")
        pending_chat_id = eval_helper.get("pending_chat_id")
        pending_reply = eval_helper.get("pending_reply")

        if pending_user is not None:
            self.from_user = pending_user
            self.chat = _FakeChat(pending_chat_id or pending_user.id)
            self.reply_to_message = pending_reply
            # consume so a later live inline call doesn't reuse stale data
            eval_helper["pending_user"] = None
            eval_helper["pending_chat_id"] = None
            eval_helper["pending_reply"] = None
        else:
            self.from_user = q.from_user
            self.chat = _FakeChat(q.from_user.id)
            self.reply_to_message = None

        self.id = None
        self.text = q.query
        self.command = q.query.split()


def build_result(code: str, raw_result: str):
    match = PASTE_RE.search(raw_result)
    paste_url = None

    if match:
        paste_url = match.group(1)
        result_text = raw_result[:match.start()].rstrip()
    else:
        result_text = "Code Executed." if raw_result == "Done." else raw_result

    text = (
        f"📤 **Evaluation Output**\n"
        f"{SEP}\n"
        f"**Code:**\n```python\n{code}\n```\n"
        f"{SEP}\n"
        f"**Result:**\n"
        f"<blockquote>{result_text}</blockquote>"
    )
    if paste_url:
        text += f"\n{SEP}\n_Output truncated — full result on Pastebin._"

    buttons = [InlineKeyboardButton("🗑 Close", callback_data="close_eval", style=ButtonStyle.PRIMARY)]
    if paste_url:
        buttons.insert(0, InlineKeyboardButton("📄 See Full Output", url=paste_url, style=ButtonStyle.PRIMARY))

    return text, InlineKeyboardMarkup([buttons])


@Client.on_inline_query(filters.regex(r"^(eval|e)\s") & ADMINS.inline())
async def eval_inline(c: Client, q: InlineQuery):
    parts = q.query.split(None, 1)
    
    if len(parts) < 2 or not parts[1].strip():
        text = "❌ No code given.\n\nUsage: `eval <code>` or `e <code>`"
        await q.answer([
            InlineQueryResultArticle(
                thumb_url=Config.main_pic,
                title="❌ No Code Given",
                input_message_content=InputTextMessageContent(text)
            )
        ], cache_time=0)
        return

    code = parts[1]
    fake_msg = _FakeMsg(q)

    eval_helper["code"] = code
    eval_helper["chat_id"] = fake_msg.chat.id

    raw_result = await get_output(parts, c, fake_msg)
    eval_helper["result"] = raw_result

    text, keyboard = build_result(code, raw_result)

    await q.answer([
        InlineQueryResultArticle(
            thumb_url=Config.main_pic,
            title="📥 Eval Result",
            description=(raw_result[:60] if raw_result else "Code Executed."),
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^close_eval$") & ADMINS.callback())
async def close_eval_callback(c: Client, cq: CallbackQuery):
    await userbot.delete_messages(
        chat_id=EVAL_CACHE.get("chat_id"),
        message_ids=[EVAL_CACHE.get("message_id"), EVAL_CACHE.get("sent_id")]
    )
    await cq.answer("Closed.")
