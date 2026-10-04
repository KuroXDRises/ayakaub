from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from ..filters import ADMINS
from ..utilities.dev import eval_helper


@Client.on_inline_query(filters.regex("^image$") & ADMINS.inline())
async def imbb_inline(c: Client, q: InlineQuery):
    data = eval_helper.get("imbb_image")

    if not data:
        return await q.answer([], cache_time=0)

    caption = (
        f"<b>📷 Uploaded Image</b>\n"
        f"<b>URL:</b> <a href=\"{data['url']}\">Open</a>\n"
        f"<b>Size:</b> <code>{round(data['size'] / 1024, 1)} KB</code>\n"
        f"<b>Dimensions:</b> <code>{data['width']} × {data['height']}</code>\n"
        f"<b>Type:</b> <code>{data['mime']}</code>\n"
        f"<b>Name:</b> <code>{data['name']}</code>\n"
        f"<a href=\"{data['delete_url']}\">🗑 Delete</a>"
    )

    await q.answer([
        InlineQueryResultPhoto(
            photo_url=data["url"],
            thumb_url=data["thumb"],
            photo_width=data["width"],
            photo_height=data["height"],
            title="📷 ImgBB Upload",
            description=f"{data['width']}×{data['height']} · {round(data['size'] / 1024, 1)} KB",
            caption=caption,
            parse_mode=ParseMode.HTML
        )
    ], cache_time=0)