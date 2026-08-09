from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputRichMessageContent, InputRichMessage
from ..utilities.anime import fetch_anime
from ..filters import ADMINS


def build_rich_html(anime_id, status, episodes, score, genres, description, en_name, native_name) -> str:

    clean_desc = (description or "N/A") \
        .replace("<br><br>\n", "\n\n") \
        .replace("<br>", " ") \
        .strip()

    genre_list = "".join(f"<li>{g}</li>" for g in genres)
    status_fmt = status.replace("_", " ").title()

    return f"""<img src="https://img.anili.st/media/{anime_id}"/>

<h1>{en_name}</h1>
<p><i>{native_name}</i></p>

<hr/>

<table bordered striped>
<tr><th align="left">📺 Episodes</th><td><code>{episodes}</code></td></tr>
<tr><th align="left">⭐ Score</th><td><code>{score}/100</code></td></tr>
<tr><th align="left">📌 Status</th><td><code>{status_fmt}</code></td></tr>
</table>

<hr/>

<details><summary><b>🎭 Genres</b></summary>
<ul>{genre_list}</ul>
</details>

<hr/>

<details><summary><b>📖 Synopsis</b></summary>
<blockquote>{clean_desc}<cite>AniList</cite></blockquote>
</details>"""


@Client.on_inline_query(filters.regex(r"anime (.+)") & ADMINS.message())
async def inline_ani(c: Client, q: InlineQuery):
    name      = q.matches[0].group(1)
    result    = await fetch_anime(name)
    rich_text = build_rich_html(*result)

    await q.answer([
        InlineQueryResultArticle(
            title="send anime",
            input_message_content=InputRichMessageContent(
                InputRichMessage(html=rich_text)
            )
        )
    ], cache_time=0)