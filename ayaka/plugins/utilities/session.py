import aiohttp

session = aiohttp.ClientSession(
    headers={
        "User-agent": "AyakaUserBot/1.0 (https://github.com/KuroxdRises; contact: test@email.com)"
    }
)