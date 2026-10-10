import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from ayaka import cmd

OUR_IDENTITY = {
    "first_name": None,
    "last_name": "",
    "bio": "",
    "photos": 0,
    "cloned": False,
}


@Client.on_message(cmd(["clone"]) & filters.me, group=691)
async def clone_handler(c: Client, m: Message):
    r = m.reply_to_message
    if not r or not r.from_user:
        return await m.reply("**Reply to a user to clone his identity.**")
    target = r.from_user
    x = await m.edit("**__Cloning...__**")
    try:
        if not OUR_IDENTITY["cloned"]:
            me = await c.get_chat("me")
            OUR_IDENTITY["first_name"] = me.first_name
            OUR_IDENTITY["last_name"] = me.last_name or ""
            OUR_IDENTITY["bio"] = me.bio or ""
            OUR_IDENTITY["cloned"] = True
        try:
            bio = ((await c.get_chat(target.id)).bio or "")[:70]
        except Exception:
            bio = ""
        await c.update_profile(
            first_name=target.first_name,
            last_name=target.last_name or "",
            bio=bio
        )
        try:
            async for p in c.get_chat_photos(target.id, limit=1):
                buf = await c.download_media(p.file_id, in_memory=True)
                await c.set_profile_photo(photo=buf)
                OUR_IDENTITY["photos"] += 1
        except Exception:
            traceback.print_exc()
        await x.edit(f"**__✅ Cloned {target.first_name}__**")
    except Exception as e:
        traceback.print_exc()
        await x.edit(f"**__❌ {type(e).__name__}: {e}__**")


@Client.on_message(cmd(["revert"]) & filters.me, group=692)
async def revert_handler(c: Client, m: Message):
    if not OUR_IDENTITY["cloned"]:
        return await m.reply("**__Nothing to revert__**")
    x = await m.edit("**__Reverting...__**")
    try:
        await c.update_profile(
            first_name=OUR_IDENTITY["first_name"],
            last_name=OUR_IDENTITY["last_name"],
            bio=OUR_IDENTITY["bio"]
        )
        if OUR_IDENTITY["photos"]:
            ids = [p.file_id async for p in c.get_chat_photos("me", limit=OUR_IDENTITY["photos"])]
            await c.delete_profile_photos(ids)
        OUR_IDENTITY.update(first_name=None, last_name="", bio="", photos=0, cloned=False)
        await x.edit("**__✅ Identity restored__**")
    except Exception as e:
        traceback.print_exc()
        await x.edit(f"**__❌ {type(e).__name__}: {e}__**")