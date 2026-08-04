from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from ..filters import ADMINS
from ayaka import cmd
import asyncio


def change_text(text: str) -> list[str]:
    return [text[:i] for i in range(1, len(text) + 1)]


@Client.on_message(cmd(["type"]) & ADMINS.message(), group=11)
async def type_command(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: /type [msg]")

    text = " ".join(m.command[1:])
    frames = change_text(text)
    cursor = "▍"

    # for long text, skip frames so we don't spam edits / hit FloodWait
    step = max(1, len(frames) // 40)
    frames = frames[::step]
    if frames[-1] != text:
        frames.append(text)

    msg = await c.send_message(
        chat_id=m.chat.id,
        text=f"<code><u>{cursor}</u></code>"
    )
    await asyncio.sleep(0.2)

    for frame in frames:
        try:
            await msg.edit(f"<code><u>{frame}{cursor}</u></code>")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.edit(f"<code><u>{frame}{cursor}</u></code>")
        await asyncio.sleep(0.3)

    await msg.edit(f"<code><u>{text}</u></code>")
