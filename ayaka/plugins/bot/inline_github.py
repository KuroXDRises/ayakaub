from html import escape

from aiohttp import ClientError, ClientResponseError
from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputRichMessage,
    InputRichMessageContent,
)

from ..filters import ADMINS
from ..utilities.github import Github


@Client.on_inline_query(filters.regex(r"^git_user\s+(.+)") & ADMINS.inline())
async def git_user_inline(_: Client, query: InlineQuery) -> None:
    """Show a GitHub profile card for ``git_user <username>``."""
    username = query.matches[0].group(1).strip()

    if not username:
        await query.answer([
            InlineQueryResultArticle(
                title="❌ No GitHub username given",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(
                        html="<b>Usage:</b> <code>git_user &lt;username&gt;</code>"
                    )
                ),
            )
        ], cache_time=0)
        return

    try:
        rich_html = await Github().rich_setup(username)
    except ClientResponseError as error:
        if error.status == 404:
            message = f"<b>❌ GitHub user not found:</b> <code>{escape(username)}</code>"
        else:
            message = "<b>❌ GitHub is unavailable right now.</b> Please try again later."
    except (ClientError, ValueError, OSError, TimeoutError):
        message = "<b>❌ GitHub is unavailable right now.</b> Please try again later."
    else:
        await query.answer([
            InlineQueryResultArticle(
                title="🐙 GitHub User Search",
                description=f"GitHub profile for {username}",
                input_message_content=InputRichMessageContent(
                    rich_message=InputRichMessage(html=rich_html)
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🗑 Close", callback_data="close_git", style=ButtonStyle.DANGER)]
                ]),
            )
        ], cache_time=0)
        return

    await query.answer([
        InlineQueryResultArticle(
            title="❌ GitHub lookup failed",
            description="Could not load this GitHub profile",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=message)
            ),
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^close_git$") & ADMINS.callback())
async def close_git_callback(client: Client, callback: CallbackQuery) -> None:
    """Replace an inline GitHub result with a closed-state message."""
    if callback.inline_message_id:
        await client.edit_inline_text(
            callback.inline_message_id,
            rich_message=InputRichMessage(html="<b>GitHub profile closed.</b>"),
            reply_markup=None,
        )
    elif callback.message:
        await callback.message.delete()

    await callback.answer("Closed.")
