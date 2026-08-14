from typing import Any
from html import escape
from urllib.parse import quote


from aiohttp import ClientSession


BASE_URL: str = "https://api.github.com/users"


class Github:
    """Small async client for GitHub's public user API."""

    def __init__(self, client_session: ClientSession | None = None) -> None:
        self.session = client_session

    async def get_user(self, name: str) -> dict[str, Any]:
        """Return the public profile for *name*.

        ``aiohttp.ClientResponseError`` is raised for GitHub errors, including
        an unknown user (404) or a rate-limited request (403).
        """
        username = name.strip().lstrip("@")
        if not username:
            raise ValueError("GitHub username cannot be empty")

        if self.session is None:
            # Importing session creates an aiohttp ClientSession, which must
            # happen while the bot's event loop is running.
            from .session import session
            client_session = session
        else:
            client_session = self.session

        url = f"{BASE_URL}/{quote(username, safe='')}"
        async with client_session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def rich_setup(self, name: str) -> str:
        """Return a Telegram HTML profile card for a GitHub user."""
        user = await self.get_user(name)

        login = str(user.get("login") or name.strip().lstrip("@"))
        display_name = str(user.get("name") or login)
        profile_url = str(user.get("html_url") or f"https://github.com/{login}")
        bio = str(user.get("bio") or "No bio provided.")
        location = str(user.get("location") or "Not specified")
        company = str(user.get("company") or "Not specified")
        created_at = str(user.get("created_at") or "Unknown").replace("T", " ").replace("Z", " UTC")

        website = user.get("blog")
        if website:
            website = str(website)
            website_url = website if website.startswith(("https://", "http://")) else f"https://{website}"
            website_html = f'<a href="{escape(website_url, quote=True)}">{escape(website)}</a>'
        else:
            website_html = "Not specified"

        return (
            "<h1>🐙 GitHub Profile</h1>\n"
            "<i>━━━━━━━━━━━━━━━━━━━━</i>\n"
            f'<p><a href="{escape(profile_url, quote=True)}"><b>{escape(display_name)}</b></a> '
            
            f"(<code>@{escape(login)}</code>)</p>\n"
            f"<blockquote>{escape(bio)}</blockquote>\n"
            "<i>━━━━━━━━━━━━━━━━━━━━</i>\n"
            "<p>"
            f"<b>📦 Repositories:</b> {int(user.get('public_repos') or 0)}\n<br>"
            f"<b>👥 Followers:</b> {int(user.get('followers') or 0)} · <br>"
            f"<b>👥Following:</b> {int(user.get('following') or 0)}\n<br>"
            f"<b>📍 Location:</b> {escape(location)}\n<br>"
            f"<b>🏢 Company:</b> {escape(company)}\n<br>"
            f"<b>🌐 Website:</b> {website_html}\n<br>"
            f"<b>📅 Joined:</b> {escape(created_at)}"
            "</p>"
        )
