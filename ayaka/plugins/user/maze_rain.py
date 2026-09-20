from pyrogram import Client, filters, types

TARGET_CHAT_ID = -1003929450754
TARGET_BOT_ID = 8966963895


@Client.on_message(
    filters.text & filters.chat(TARGET_CHAT_ID) & filters.user(TARGET_BOT_ID),
    group=363,
)
async def rain_handler(c: Client, m: types.Message):
    if m.text.startswith("🌧 RAIN!"):
        await m.click()
