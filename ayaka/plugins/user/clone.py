import traceback
from pyrogram import Client, filters, raw
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
        photo_err = None
        try:
            fid = target.photo.big_file_id if target.photo else None
            if fid is None:
                async for p in c.get_chat_photos(target.id, limit=1):
                    fid = p.file_id
            if fid:
                buf = await c.download_media(fid, in_memory=True)
                await c.set_profile_photo(photo=buf)
                OUR_IDENTITY["photos"] += 1
            else:
                photo_err = "no photo visible"
        except Exception as e:
            photo_err = f"{type(e).__name__}: {e}"
        await x.edit(
            f"**__✅ Cloned {target.first_name}__**"
            + (f"\n**__⚠️ Photo: {photo_err}__**" if photo_err else "")
        )
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
            res = await c.invoke(
                raw.functions.photos.GetUserPhotos(
                    user_id=raw.types.InputUserSelf(),
                    offset=0,
                    max_id=0,
                    limit=OUR_IDENTITY["photos"]
                )
            )
            ids = [
                raw.types.InputPhoto(
                    id=p.id,
                    access_hash=p.access_hash,
                    file_reference=p.file_reference
                )
                for p in res.photos
            ]
            if ids:
                await c.invoke(raw.functions.photos.DeletePhotos(id=ids))
        OUR_IDENTITY.update(first_name=None, last_name="", bio="", photos=0, cloned=False)
        await x.edit("**__✅ Identity restored__**")
    except Exception as e:
        traceback.print_exc()
        await x.edit(f"**__❌ {type(e).__name__}: {e}__**")