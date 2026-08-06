from pyrogram import Client, filters
from pyrogram.types import Message
from ..data import SILENT_STATE
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["silent", "unsilent", "unsilent_chat"]) & filters.user(Config.ADMIN_ID), group=700)
async def silent_command(c:Client, m:Message):
    command = m.command[0]
    if command=="silent":
        if SILENT_STATE.status and m.chat.id in SILENT_STATE.chat_ids:
            await m.reply("**Silent Mode** is already active in this chat.")
        else:
            if not SILENT_STATE.status:
                SILENT_STATE.status = True
                SILENT_STATE.chat_ids.add(m.chat.id)
                await m.reply("**Silent Mode** activated in this chat.")
            else:
                SILENT_STATE.chat_ids.add(m.chat.id)
                await m.reply("**Silent Mode** activated in this chat.")
    elif command=="unsilent":
        if not SILENT_STATE.status and m.chat.id not in SILENT_STATE.chat_ids:
            await m.reply("**Silent Mode** is not active yet.")
        else:
            SILENT_STATE.status = True
            SILENT_STATE.chat_ids = set()
            await m.reply("**Silent Mode** deactivated for all chats.")
    elif command=="unsilent_chat":
        if not SILENT_STATE.status:
            await m.reply("**Silent Mode** is not active yet.")
        elif SILENT_STATE.status and m.chat.id not in SILENT_STATE.chat_ids:
            await m.reply("**Silent Mode** is not active for this chat.")
        else:
            SILENT_STATE.chat_ids.discard(m.chat.id)
            await m.reply("**Silent Mode** deactivated for this chat.")

@Client.on_message(~filters.user(Config.ADMIN_ID), group=869)
async def read_chats(c:Client, m:Message):
    if not SILENT_STATE.status:
        return
    try:
        for chat_id in SILENT_STATE.chat_ids:
            await c.read_chat_history(chat_id)
            await c.invoke(
            __import__("pyrogram.raw.functions.account", fromlist=["UpdateStatus"])
            .UpdateStatus(offline=True)
            )
    except Exception as e:
        print(str(e))


@Client.on_message(cmd(["silent_status"]) & filters.user(Config.ADMIN_ID), group=701)
async def silent_status_command(c:Client, m:Message):
    text = (
        "**「 Silent Status 」**\n"
        f"**Status:** {"`Active`" if SILENT_STATE.status else "`Disabled`"}\n"
        f"**Silent Chats:** {[_ for _ in SILENT_STATE.chat_ids]}"
    )
    await m.reply(text)