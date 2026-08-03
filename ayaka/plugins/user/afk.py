import isort
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..utilities.afk import (
    set_afk, remove_afk, is_afk, format_afk_duration,
    has_been_notified, mark_notified
)
from ..decorators.check_state import require_afk_inactive, require_afk_active
from ..data import AFK_DATA
from ayaka import cmd


AFK_PHOTO = "https://ibb.co/ymdKW7Br"


async def _replied_to_me(_, __, m: Message) -> bool:
    return bool(
        m.reply_to_message
        and m.reply_to_message.from_user
        and m.reply_to_message.from_user.is_self
    )


replied_to_me = filters.create(_replied_to_me)


@Client.on_message(cmd(["afk"]) & filters.me)
@require_afk_inactive
async def afk_command(c: Client, m: Message):
    parts = m.text.split(None, 1)
    reason = parts[1].strip() if len(parts) > 1 else "Not Provided"

    media_from_chat = None
    message_media_id = None
    if m.reply_to_message and m.reply_to_message.media:
        media_from_chat = m.reply_to_message.chat.id
        message_media_id = m.reply_to_message.id

    set_afk(reason=reason, media_from_chat=media_from_chat, message_media_id=message_media_id)

    await m.edit_text(f"🌙 **AFK Activated**\n**Reason:** {reason}")


@Client.on_message(cmd(["unafk"]) & filters.me)
@require_afk_active
async def unafk_command(c: Client, m: Message):
    duration = format_afk_duration()
    remove_afk()
    await m.edit_text(f"✅ **Welcome back!**\n\nYou were AFK for **{duration}**.")


@Client.on_message(
    filters.incoming & ~filters.me & ~filters.bot &
    (filters.private | filters.mentioned | replied_to_me),
    group=5
)
async def afk_notifier(c: Client, m: Message):
    if not is_afk():
        return

    user = m.from_user
    if not user or has_been_notified(user.id):
        return

    mark_notified(user.id)

    duration = format_afk_duration()
    reason = AFK_DATA.reason or "Not Provided"
    text = f"🌙 **I'm currently AFK**\n**Reason:** {reason}\n**Since:** {duration} ago"

    if AFK_DATA.media_from_chat and AFK_DATA.message_media_id:
        try:
            await c.copy_message(
                chat_id=m.chat.id,
                from_chat_id=AFK_DATA.media_from_chat,
                message_id=AFK_DATA.message_media_id,
                caption=text,
                reply_parameters=ReplyParameters(message_id=m.id)
            )
            return
        except Exception:
            pass

    await m.reply_photo(
        photo=AFK_PHOTO,
        caption=text,
        reply_parameters=ReplyParameters(message_id=m.id)
    )

@Client.on_message(filters.text & filters.me, group=-9)
async def auto_unafk(c:Client, m:Message):
    if is_afk():
        duration = format_afk_duration()
        remove_afk()
        await m.reply(f"{m.from_user.first_name} came back online 🟢\nAfk Since: {duration}")
    else:
        return