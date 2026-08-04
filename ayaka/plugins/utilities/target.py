from pyrogram import Client
from pyrogram.types import Message


async def resolve_target(c: Client, m: Message):
    """Get the target user from a reply, or from a username/id argument.
    Returns (target_user, error_message). error_message is None on success."""
    r = m.reply_to_message
    args = m.command[1:]

    if r:
        return r.from_user, None

    if args:
        target = args[0].lstrip("@")
        target = int(target) if target.lstrip("-").isdigit() else target
        try:
            return await c.get_users(target), None
        except Exception:
            # get_users needs the peer in cache. If they're a member of this
            # chat, resolve via the chat's member list instead — that
            # doesn't need peer cache.
            try:
                member = await c.get_chat_member(chat_id=m.chat.id, user_id=target)
                return member.user, None
            except Exception:
                return None, f"❌ Could not find user: `{args[0]}`"

    return None, "❌ Reply to a user, or use: `<command> <username or id>`"
