from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMemberStatus
from datetime import datetime, timedelta
import re

from ayaka import cmd
from ...filters import ADMINS
from ...utilities.target import resolve_target


MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)

# restored on unmute — adjust if your group's default permissions differ
UNMUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)


def parse_duration(text: str) -> int | None:
    """Parse a duration string like '10m', '2h', '1d' into seconds."""
    match = re.fullmatch(r"(\d+)([smhd])", text.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
    return value * multiplier


@Client.on_message(cmd(["mute", "tmute"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def mute_command(c: Client, m: Message):
    is_tmute = m.command[0].lower() == "tmute"

    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    duration_text = None
    duration_seconds = None
    if is_tmute:
        args = m.command[1:]
        duration_text = args[-1] if args else None
        duration_seconds = parse_duration(duration_text) if duration_text else None
        if duration_seconds is None:
            await m.reply("❌ Usage: `/tmute <reply|username|id> <duration>` (e.g. 10m, 2h, 1d)")
            return

    id = target_user.id
    member = await c.get_chat_member(chat_id=m.chat.id, user_id=id)

    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await m.reply("❌ Unable to mute an admin.\nPlease demote them first.")
        return

    until_date = None
    if duration_seconds:
        until_date = datetime.utcnow() + timedelta(seconds=duration_seconds)

    try:
        await c.restrict_chat_member(
            chat_id=m.chat.id,
            user_id=id,
            permissions=MUTED_PERMISSIONS,
            until_date=until_date
        )
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to mute people.")
        return

    if duration_seconds:
        await m.reply(f"🔇 Muted **{target_user.first_name}** for `{duration_text}`.")
    else:
        await m.reply(f"🔇 Muted **{target_user.first_name}**.")


@Client.on_message(cmd(["unmute"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def unmute_command(c: Client, m: Message):
    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    id = target_user.id

    try:
        await c.restrict_chat_member(
            chat_id=m.chat.id,
            user_id=id,
            permissions=UNMUTED_PERMISSIONS
        )
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to unmute people.")
        return
    except Exception as e:
        await m.reply(f"❌ Could not unmute: {e}")
        return

    await m.reply(f"🔊 Unmuted **{target_user.first_name}**.")
