import base64
from aiohttp import ClientSession


async def upload_image(session: ClientSession, img_bytes: bytes, api_key: str) -> dict | None:
    b64 = base64.b64encode(img_bytes).decode()

    async with session.post(
        "https://api.imgbb.com/1/upload",
        data={"key": api_key, "image": b64}
    ) as r:
        res = await r.json()

    if not res.get("success"):
        return None

    d = res["data"]
    return {
        "url":        d["url"],
        "thumb":      d["thumb"]["url"],
        "delete_url": d["delete_url"],
        "width":      d["width"],
        "height":     d["height"],
        "size":       d["size"],
        "mime":       d["mime"],
        "name":       d["image"]["name"],
    }