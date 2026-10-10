import secrets
from pyrogram import Client
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from ayaka import cmd
from config import Config
from ..data.premdb import premiumEmojiMethods
from ..filters import ADMINS
from ..utilities.dev import eval_helper


def extract_emojis(m: Message) -> list:
    text = str(m.text or m.caption or "")
    raw = text.encode("utf-16-le")
    out = []
    for e in (m.entities or m.caption_entities or []):
        if e.type == MessageEntityType.CUSTOM_EMOJI:
            key = raw[e.offset * 2:(e.offset + e.length) * 2].decode("utf-16-le")
            out.append((key, int(e.custom_emoji_id)))
    return out


@Client.on_message(cmd(["add_emoji"]) & ADMINS.message(), group=561)
async def add_emoji_handler(c: Client, m: Message):
    parts = (m.text or "").split()
    pairs = []
    if len(parts) >= 3 and parts[2].isdigit():
        pairs = [(parts[1], int(parts[2]))]
    else:
        pairs = extract_emojis(m)
        if not pairs and m.reply_to_message:
            pairs = extract_emojis(m.reply_to_message)
    if not pairs:
        return await m.reply("**__Reply to a premium emoji message, or use: add_emoji 🔥 emoji_id__**")
    for key, emoji_id in pairs:
        await premiumEmojiMethods.add_premium_emoji(emoji_id, key)
    await m.reply("**__✅ Added: " + " ".join(k for k, _ in pairs) + "__**")


@Client.on_message(cmd(["rem_emoji"]) & ADMINS.message(), group=562)
async def rem_emoji_handler(c: Client, m: Message):
    keys = [k for k, _ in extract_emojis(m)]
    if not keys and m.reply_to_message:
        keys = [k for k, _ in extract_emojis(m.reply_to_message)]
    if not keys:
        keys = (m.text or "").split()[1:]
    if not keys:
        return await m.reply("**__Reply to a premium emoji message, or use: rem_emoji 🔥__**")
    removed, missing = [], []
    for key in keys:
        if await premiumEmojiMethods.remove_premium_emoji(key):
            removed.append(key)
        else:
            missing.append(key)
    text = ""
    if removed:
        text += "**__✅ Removed: " + " ".join(removed) + "__**\n"
    if missing:
        text += "**__❌ Not found: " + " ".join(missing) + "__**"
    await m.reply(text.strip())


@Client.on_message(cmd(["emojify"]) & ADMINS.message(), group=563)
async def emojify_handler(c: Client, m: Message):
    parts = (m.text or "").split(None, 1)
    text = parts[1] if len(parts) > 1 else ""
    if not text and m.reply_to_message:
        text = m.reply_to_message.text or m.reply_to_message.caption or ""
    if not text:
        return await m.reply("**__Usage: emojify text, or reply to a message__**")
    token = secrets.token_hex(4)
    eval_helper[f"emojify_{token}"] = str(text)
    results = await c.get_inline_bot_results(bot=Config.BOT_USERNAME, query=f"prem {token}")
    if not results.results:
        eval_helper.pop(f"emojify_{token}", None)
        return await m.reply("**__❌ Inline bot returned no results__**")
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=results.query_id,
        result_id=results.results[0].id
    )
    try:
        await m.delete()
    except Exception:
        pass