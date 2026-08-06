from pyrogram import Client, filters
from pyrogram.types import Message

def starts(prefix: str | None = None):
    if prefix is None:
        raise Exception("No prefix is passed. Please pass a prefix first")
    prefix = prefix.lower()
    async def func(flt, c:Client, m:Message):
        text = m.text
        return text.lower().startswith(prefix) if text else False
    return filters.create(func, name="StartsFilter")