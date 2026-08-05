from pyrogram import Client, filters
from pyrogram.types import Message
from ..data import PRIVATE_CHAT_STATE
from ayaka import cmd
from config import Config


MODES:list[str] = ["on", "off"]

@Client.on_message(cmd(["pmpermit"]) & filters.user(Config.ADMIN_ID), group=269)
async def pmpermit_command(c:Client, m:Message):
    if len(m.command)!=2 or m.command[1] not in MODES:
        await m.reply("Usage: `pmpermit` `on`|`off`")
        return
    if m.command[1]=="on":
        if PRIVATE_CHAT_STATE.status:
            await m.reply("**PMPermit is already on**")
            return
        PRIVATE_CHAT_STATE.status = True
        await m.reply("**PMPermit enabled successfully.**")
    elif m.command[1]=="off":
        if not PRIVATE_CHAT_STATE.status:
            await m.reply("**PMPermit is already off**")
            return
        PRIVATE_CHAT_STATE.status = False
        await m.reply("**PMPermit disabled successfully.**")


@Client.on_message(cmd(["approve_pm", "disapprove_pm"]) & filters.user(Config.ADMIN_ID) & (filters.private | filters.group), group=-369)
async def approve_pm_command(c:Client, m:Message):
    command = m.command[0]
    r = m.reply_to_message
    if not r:
        await m.reply("**Reply to a user using these commands.**")
        return
    elif r:
        if command=="approve_pm":
            user_id = r.from_user.id
            if user_id in PRIVATE_CHAT_STATE.approved:
                await m.reply("**User already Approved to PrivateChat**")
                return
            PRIVATE_CHAT_STATE.approved.add(user_id)
            await m.reply("**User is Approved for PrivateChat**")
        elif command=="disapprove_pm":
            user_id = r.from_user.id
            if user_id not in PRIVATE_CHAT_STATE.approved:
                await m.reply("**User is not Approvedto PrivateChat**")
                return
            PRIVATE_CHAT_STATE.approved.discard(user_id)
            await m.reply("**User is now Disapproved for PrivateChat**")

@Client.on_message(cmd(["pmstatus"]) & filters.user(Config.ADMIN_ID), group=-469)
async def pmstatus_command(c:Client, m:Message):
    ids = []
    for id in PRIVATE_CHAT_STATE.approved:
        ids.append(id)
    msg = (
        "**《 PM Status 》**\n"
        f"**Status:** {'`🟢 Enabled`' if PRIVATE_CHAT_STATE.status else '`🔴 Disabled`'}\n"
        f"**Time Limit:** `{PRIVATE_CHAT_STATE.time_limit}seconds`\n"
        f"**Approved IDs:** {ids}"
    )
    await m.reply(msg)

@Client.on_message(cmd(["pmlimit"]) & filters.user(Config.ADMIN_ID), group=-569)
async def pmlimit_command(c:Client, m:Message):
    if len(m.command)!=2:
        await m.reply("Usage: pmlimit [seconds]")
        return
    seconds = int(m.command[1])
    if seconds<60:
        await m.reply("Limit must be greater than 60seconds.")
        return
    PRIVATE_CHAT_STATE.time_limit = seconds
    await m.reply(f"**Limit changed to {seconds}seconds.**")
    