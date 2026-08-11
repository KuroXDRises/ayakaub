from pyrogram import Client, filters, types, enums
from ayaka import cmd
from ..utilities.time import is_overnight
from ..data import NIGHT_STATE
from config import Config


@Client.on_business_message(cmd(["nightmode"]) & filters.user(Config.ADMIN_ID), group=72)
async def nightmode_handler(c: Client, m: types.Message):
    if len(m.command) != 2:
        await m.reply("Usage: .nightmode on|off.")
        return

    action = m.command[1].lower()

    if action == "on":
        if NIGHT_STATE.status:
            await m.reply("**Night Mode** is already started")
        else:
            NIGHT_STATE.status = True
            await m.reply("**Night Mode** enabled.")
    elif action == "off":
        if not NIGHT_STATE.status:
            await m.reply("**Night Mode** is already disabled")
        else:
            NIGHT_STATE.status = False
            await m.reply("**Night Mode** disabled.")
    else:
        await m.reply("Invalid Usage.")


@Client.on_business_message(filters.private & filters.incoming)
async def check_nightmode_handler(c: Client, m: types.Message):
    # feature must be turned on AND it must currently be within the
    # overnight window — status alone doesn't mean "always night",
    # it means "use the time check to decide"
    if not NIGHT_STATE.status:
        return
    if not is_overnight():
        return

    text = (
    "🌙 <b>Night Mode — ON</b>\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "❄️ I'm <b>Ayaka</b>.\n"
    "My master is currently asleep, so I'm taking over for the night.\n\n"
    "💤 Please don't disturb him right now.\n"
    "If you need to send a message, you can reach him through my bot below.\n\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🌌 <i>I'll be here until morning.</i>"
    )

    await c.send_message(
        chat_id=m.chat.id,
        text=text,
        reply_markup=types.InlineKeyboardMarkup([
            [
                types.InlineKeyboardButton(
                    "💬 Message Through Bot",
                    url=f"https://t.me/{Config.BOT_USERNAME}?start=True",
                    style=enums.ButtonStyle.PRIMARY
                )
            ]
        ]),
        business_connection_id=m.business_connection_id,
        link_previee_options=types.LinkPreviewOptions(
            url=Config.main_pic,
            show_above_text=True,
            prefer_large_media=True
        )
    )