from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from ayaka import cmd


@Client.on_message(cmd(["block"]) & filters.me, group=-100)
async def block_command(c: Client, m: Message):
    if m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
        if not m.reply_to_message:
            return
        target = m.reply_to_message.from_user
        try:
            await c.block_user(target.id)
            await m.reply(f"**__✅ Blocked User [{target.first_name}](tg://user?id={target.id})__**")
        except Exception:
            pass
        return

    target_id = m.chat.id
    target = await c.get_users(target_id)
    try:
        await c.block_user(target_id)
        await m.reply(f"**__✅ Blocked User [{target.first_name}](tg://user?id={target_id})__**")
    except Exception as e:
        await m.reply(str(e))


@Client.on_message(cmd(["unblock"]) & filters.me, group=-101)
async def unblock_command(c: Client, m: Message):
    if m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
        if not m.reply_to_message:
            return
        target = m.reply_to_message.from_user
        try:
            await c.unblock_user(target.id)
            await m.reply(f"**__✅ Unblocked User [{target.first_name}](tg://user?id={target.id})__**")
        except Exception:
            pass
        return

    target_id = m.chat.id
    target = await c.get_users(target_id)
    try:
        await c.unblock_user(target_id)
        await m.reply(f"**__✅ Unblocked User [{target.first_name}](tg://user?id={target_id})__**")
    except Exception as e:
        await m.reply(str(e))
