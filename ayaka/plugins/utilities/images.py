"""Helpers for retrieving image URLs from Bing Images.

Switched from Google Images: Google now redirects image searches to a
"udm=2" results format whose data isn't embedded in the raw HTML the same
way anymore (confirmed via debugging — the old regex matched only 2 URLs
in a 92KB page, none of them actual image data). Bing's image results page
still embeds each result's direct image URL in a stable, easily-parsed
`murl` field inside an HTML-escaped JSON blob on each result's <a> tag,
which has been reliable for years.
"""

from __future__ import annotations

import asyncio
from html import unescape
import re
from typing import Final
from urllib.parse import urlparse

from aiohttp import ClientSession


BING_IMAGES_URL: Final = "https://www.bing.com/images/search"
_MURL_PATTERN: Final = re.compile(r"murl&quot;:&quot;(.*?)&quot;")
_HEADERS: Final = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
}


def _decode_url(url: str) -> str:
    """Turn URLs embedded in Bing's escaped JSON into normal URLs."""
    url = re.sub(r"\\u([0-9a-fA-F]{4})", lambda match: chr(int(match.group(1), 16)), url)
    url = re.sub(r"\\x([0-9a-fA-F]{2})", lambda match: chr(int(match.group(1), 16)), url)
    return unescape(url.replace(r"\/", "/"))


_BLOCKED_HOST_KEYWORDS: Final = (
    "porn", "xxx", "hentai", "xnxx", "xvideos", "redtube", "pornhub",
    "xhamster", "rule34", "hqporner", "nhentai",
)


def _is_valid_image_url(url: str) -> bool:
    """Basic sanity check — real URL, not a Bing/Microsoft internal asset,
    and not from a known adult-content domain. This is a defense-in-depth
    check on top of adlt=strict in the request params — never rely on a
    single filter for content this sensitive."""
    parsed = urlparse(url)
    host = parsed.hostname
    if parsed.scheme not in {"http", "https"} or not host:
        return False
    if host.endswith("bing.com") or host.endswith("microsoft.com"):
        return False
    host_lower = host.lower()
    if any(keyword in host_lower for keyword in _BLOCKED_HOST_KEYWORDS):
        return False
    return True


async def _is_downloadable_image(client_session: ClientSession, url: str) -> bool:
    """Check that a candidate URL actually serves an image, not an HTML page."""
    try:
        async with client_session.get(
            url,
            headers={"Accept": "image/*"},
            allow_redirects=True,
        ) as response:
            if response.status != 200:
                return False
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0]
            return content_type.lower().startswith("image/")
    except Exception:
        return False


async def get_images(
    query: str,
    limit: int = 5,
    *,
    client_session: ClientSession | None = None,
) -> list[str]:
    """Return up to ``limit`` unique external image URLs from Bing Images.

    Args:
        query: Text to search for.
        limit: Maximum number of image URLs to return. Must be positive.
        client_session: Optional aiohttp session, useful for callers that manage
            their own session or for tests.

    Raises:
        ValueError: If ``query`` is empty or ``limit`` is not positive.
        aiohttp.ClientResponseError: If Bing returns an HTTP error response.
    """
    query = query.strip()
    if not query:
        raise ValueError("Image search query cannot be empty")
    if limit < 1:
        raise ValueError("Image search limit must be positive")

    if client_session is None:
        # Import lazily: this module is loaded during plugin discovery, before
        # the application's event loop starts.
        from .session import session

        client_session = session

    # The session is shared/reused across the whole bot for connection
    # pooling, so its cookie jar persists whatever Bing sets between calls.
    # Bing personalizes the "related searches" / explore widgets using that
    # cookie-tracked history — without clearing it, an earlier unrelated
    # query (e.g. "carrom board") can bleed its results into a later one
    # (e.g. "atoms"). Clearing bing.com cookies before each search keeps
    # every call isolated.
    if hasattr(client_session.cookie_jar, "clear_domain"):
        client_session.cookie_jar.clear_domain("bing.com")
        client_session.cookie_jar.clear_domain("www.bing.com")

    params = {"q": query, "form": "HDRSC2", "first": "1", "adlt": "strict"}
    request_headers = {**_HEADERS, "Cache-Control": "no-cache", "Pragma": "no-cache"}
    async with client_session.get(
        BING_IMAGES_URL, params=params, headers=request_headers
    ) as response:
        response.raise_for_status()
        page = await response.text()

    candidates: list[str] = []
    seen: set[str] = set()
    for match in _MURL_PATTERN.finditer(page):
        url = _decode_url(match.group(1))
        if url in seen or not _is_valid_image_url(url):
            continue
        seen.add(url)
        candidates.append(url)
        if len(candidates) >= limit * 3:
            break

    valid = await asyncio.gather(
        *(_is_downloadable_image(client_session, url) for url in candidates),
        return_exceptions=False,
    )
    return [url for url, is_image in zip(candidates, valid) if is_image][:limit]
