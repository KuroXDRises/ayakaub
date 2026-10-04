import traceback
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
    data = await upload_image(
        session=session,
        img_bytes=bytes(buf.getbuffer()),
        api_key=Config.IMBB_IMAGE_API
    )

    if not data:
        return await x.edit("**__❌ ImgBB upload returned nothing__**")

    eval_helper["imbb_image"] = data

    try:
        results = await c.get_inline_bot_results(
            bot=Config.BOT_USERNAME,
            query="image"
        )

        if not results.results:
            return await x.edit("**__❌ Inline bot returned no results__**")

        await c.send_inline_bot_result(
            chat_id=m.chat.id,
            query_id=results.query_id,
            result_id=results.results[0].id,
            reply_parameters=ReplyParameters(message_id=m.reply_to_message.id)
        )
        await x.delete()
    except Exception:
        traceback.print_exc()
        await x.edit("**__❌ Inline send failed, check logs__**")