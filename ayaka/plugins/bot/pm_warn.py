from pyrogram import Client, filters
from pyrogram.types import (
    Message, BusinessConnection,
    InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
)
from pyrogram.enums import ButtonStyle
from ..filters import ADMINS
from ..data import PRIVATE_CHAT_STATE
from config import Config
import asyncio


COOLDOWN_USERS = set()

def build_dm_message() -> str:
    return """
<b>══════ ❀ 𝑨𝒚𝒂𝒌𝒂 ❀ ══════</b>

🌸 Hello, I'm <b>Ayaka</b>.

<i>My owner is currently not accepting direct messages.</i>

If your message is important, simply tap the <b>button below</b> to contact them.

<u>Thank you for your patience and understanding.</u> 💙

<b>══════════════════════════</b>
"""

@Client.on_business_message(filters.private & ~filters.me, group=-124)
async def send_dm_message(c:Client, m:Message):
    connection_id = m.business_connection_id
    connection = await c.get_business_connection(connection_id)
    if not connection.is_enabled or not connection.rights or not connection.rights.can_reply:
        return
    if not PRIVATE_CHAT_STATE.status:
        return
    if m.from_user.id in COOLDOWN_USERS or m.from_user.id in PRIVATE_CHAT_STATE.approved:
        return
    COOLDOWN_USERS.add(m.from_user.id)
    await c.send_message(
        chat_id=m.chat.id,
        text=build_dm_message(),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Open Bot", url=f"https://t.me/{Config.BOT_USERNAME}?start=start", style=ButtonStyle.PRIMARY)]
        ]),
        link_preview_options=LinkPreviewOptions(url=Config.main_pic, show_above_text=True),
        business_connection_id=connection_id
    )
    async def remove_cooldown_user():
        await asyncio.sleep(PRIVATE_CHAT_STATE.time_limit)
        COOLDOWN_USERS.discard(m.from_user.id)
    asyncio.create_task(remove_cooldown_user())