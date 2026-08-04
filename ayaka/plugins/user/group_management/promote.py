from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.errors import ChatAdminRequired
from ayaka import cmd
from ...filters import ADMINS
from ...utilities.target import resolve_target

TITLE_MAX_LEN = 16  # Telegram's hard limit for custom admin titles


@Client.on_message(cmd(["promote"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def promote_command(c: Client, m: Message):
    r = m.reply_to_message
    args = m.command[1:]

    # if replying, every arg is part of the title; otherwise the first
    # arg is the username/id and the rest is the title
    title_words = args if r else args[1:]
    title = " ".join(title_words)[:TITLE_MAX_LEN]

    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    id = target_user.id

    try:
        await c.promote_chat_member(
            chat_id=m.chat.id,
            user_id=id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_video_chats=True
            )
        )
        if title:
            await c.set_administrator_title(chat_id=m.chat.id, user_id=id, title=title)
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to promote people.")
        return
    except Exception as e:
        await m.reply(f"❌ Could not promote: {e}")
        return

    if title:
        await m.reply(f"⬆️ Promoted **{target_user.first_name}** with title `{title}`.")
    else:
        await m.reply(f"⬆️ Promoted **{target_user.first_name}**.")


@Client.on_message(cmd(["demote"], prefixes=["."]) & ADMINS.message() & filters.admin & filters.group, group=11)
async def demote_command(c: Client, m: Message):
    target_user, error = await resolve_target(c, m)
    if error:
        await m.reply(error)
        return

    id = target_user.id

    try:
        await c.promote_chat_member(
            chat_id=m.chat.id,
            user_id=id,
            privileges=ChatPrivileges()  # everything False = strip admin rights
        )
    except ChatAdminRequired:
        await m.reply("I have to be an admin in this chat to demote people.")
        return
    except Exception as e:
        await m.reply(f"❌ Could not demote: {e}")
        return

    await m.reply(f"⬇️ Demoted **{target_user.first_name}**.")
