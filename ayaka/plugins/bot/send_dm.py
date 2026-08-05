from pyrogram import Client, filters
from pyrogram.types import Message, MessageOriginHiddenUser, MessageOriginUser
from config import Config

PM_DATA:dict = {}

@Client.on_message(filters.private & ~filters.bot)
async def send_dm(c:Client, m:Message):
    if m.from_user.id != Config.ADMIN_ID:
        await c.forward_messages(chat_id=Config.ADMIN_ID, from_chat_id=m.chat.id, message_ids=[m.id])
        key = f"{m.from_user.first_name or " "} {m.from_user.last_name or " "}".strip()
        if key not in PM_DATA:
            PM_DATA[key] = m.from_user.id
    else:
        if m.reply_to_message:
            r = m.reply_to_message.forward_origin
            if isinstance(r, MessageOriginHiddenUser):
                username = r.sender_user_name
                to_id = PM_DATA.get(username)
                if to_id:
                    await c.copy_message(
                        chat_id=to_id,
                        from_chat_id=m.chat.id,
                        message_id=m.id
                    )
            elif isinstance(r, MessageOriginUser):
                await c.copy_message(
                    chat_id=r.sender_user.id,
                    from_chat_id=m.chat.id,
                    message_id=m.id
                )