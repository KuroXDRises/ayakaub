from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..utilities.image import upload_image
from ..utilities.session import session
from ..utilities.dev import eval_helper
from ayaka import cmd
from ..filters import ADMINS
from config import Config


@Client.on_message(cmd(["imbb"]) & ADMINS.message(), group=543)
async def imbb(c: Client, m: Message):
    if not m.reply_to_message or not m.reply_to_message.photo:
        return await m.reply("**__Reply to a photo to upload it to ImgBB__**")

    x = await m.edit("**__📷 Uploading...__**")

    buf = await c.download_media(m.reply_to_message.photo.file_id, in_memory=True)
    img_bytes = bytes(buf.getbuffer())

    data = await upload_image(
        session=session,
        img_bytes=img_bytes,
        api_key=Config.IMBB_IMAGE_API
    )

    if not data:
        return await x.edit("**__❌ Upload failed.__**")

    eval_helper["imbb_image"] = data

    await x.delete()

    results = await c.get_inline_bot_results(
        bot=Config.BOT_USERNAME,
        query="image"
    )
    await c.send_inline_bot_result(
        chat_id=m.chat.id,
        query_id=results.query_id,
        result_id=results.results[0].id,
        reply_parameters=ReplyParameters(message_id=m.reply_to_message.id)
    )