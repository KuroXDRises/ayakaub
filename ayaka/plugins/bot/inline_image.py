from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputRichMessageContent,
    InputRichMessage,
)
from ..filters import ADMINS
from ..utilities.dev import eval_helper


@Client.on_inline_query(filters.regex("^image$") & ADMINS.inline())
async def imbb_inline(c: Client, q: InlineQuery):
    data = eval_helper.get("imbb_image")

    if not data:
        return await q.answer([], cache_time=0)

    html = (
        f'<img src="{data["url"]}">'
        f"<h3>📷 Uploaded Image</h3>"
        f"<table bordered striped>"
        f"<tr><th>Field</th><th>Value</th></tr>"
        f"<tr><td>URL</td><td><a href=\"{data['url']}\">Open</a></td></tr>"
        f"<tr><td>Size</td><td><code>{round(data['size'] / 1024, 1)} KB</code></td></tr>"
        f"<tr><td>Dimensions</td><td><code>{data['width']} × {data['height']}</code></td></tr>"
        f"<tr><td>Type</td><td><code>{data['mime']}</code></td></tr>"
        f"<tr><td>Name</td><td><code>{data['name']}</code></td></tr>"
        f"</table>"
        f'<footer><a href="{data["delete_url"]}">🗑 Delete</a></footer>'
    )

    await q.answer([
        InlineQueryResultArticle(
            title="📷 ImgBB Upload",
            description=f"{data['width']}×{data['height']} · {round(data['size']/1024, 1)} KB",
            input_message_content=InputRichMessageContent(
                InputRichMessage(html)
            ),
        )
    ], cache_time=0)
