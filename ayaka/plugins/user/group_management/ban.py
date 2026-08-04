from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import ChatMemberStatus
from ayaka import cmd
from ...filters import ADMINS
from ...utilities.target import resolve_target


@Client.on_message(cmd(["ban", "dban"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def ban_command(c: Client, m: Message):
    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    id = target_user.id
    member = await c.get_chat_member(chat_id=m.chat.id, user_id=id)

    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await m.reply("❌ Unable to ban an admin.\nPlease demote them first to ban.")
        return

    try:
        await c.ban_chat_member(chat_id=m.chat.id, user_id=id)
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to ban people.")
        return

    r = m.reply_to_message
    if m.command[0].lower() == "dban" and r:
        await r.delete()
        await m.reply(f"✅ Banned and deleted message from **{target_user.first_name}**.")
    else:
        await m.reply(f"✅ Banned **{target_user.first_name}**.")


@Client.on_message(cmd(["unban"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def unban_command(c: Client, m: Message):
    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    id = target_user.id

    try:
        await c.unban_chat_member(chat_id=m.chat.id, user_id=id)
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to unban people.")
        return
    except Exception as e:
        await m.reply(f"❌ Could not unban: {e}")
        return

    await m.reply(f"✅ Unbanned **{target_user.first_name}**.")
