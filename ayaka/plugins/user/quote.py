from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from pyrogram.enums import ChatType
from ..filters import ADMINS
from ..data import QUOTE_STATE
from ayaka import cmd


QUOTLY_BOT: str = "QuotlyBot"  # double-check this matches the bot's real username


def quote_state(
    status: bool = False,
    chat_id: int = None,
    message_id: int = None,
    topic_id: int = None
):
    QUOTE_STATE.status = status
    QUOTE_STATE.chat_id = chat_id
    QUOTE_STATE.message_id = message_id
    QUOTE_STATE.topic_id = topic_id


@Client.on_message(filters.sticker & filters.user(QUOTLY_BOT) & filters.bot, group=-19)
async def send_sticker_method(c: Client, m: Message):
    if QUOTE_STATE.status and m.sticker:
        try:
            await c.send_sticker(
                chat_id=QUOTE_STATE.chat_id,
                sticker=m.sticker.file_id,
                message_thread_id=QUOTE_STATE.topic_id,
                reply_parameters=ReplyParameters(message_id=QUOTE_STATE.message_id)
            )
        finally:
            # reset regardless of success/failure so a stray future sticker
            # from QuotlyBot never gets relayed using stale state
            quote_state()


@Client.on_message(cmd(["q"]) & ADMINS.message(), group=-20)
async def quote_command(c: Client, m: Message):
    reply = m.reply_to_message
    if not reply:
        await m.reply("❌ Reply to a message to quote it.")
        return

    chat_id = m.chat.id
    message_id = reply.id
    topic_id = m.message_thread_id if m.chat.type==ChatType.FORUM else None

    quote_state(
        status=True,
        chat_id=chat_id,
        message_id=message_id,
        topic_id=topic_id
    )

    try:
        await reply.forward(QUOTLY_BOT)
    except Exception as e:
        quote_state()  # reset so we don't leave stale "waiting" state behind
        await m.reply(f"❌ Could not send to {QUOTLY_BOT}: {e}")
