import base64
from aiohttp import ClientSession


async def upload_image(session: ClientSession, img_bytes: bytes, api_key: str) -> dict | None:
    async with session.post(
        "https://api.imgbb.com/1/upload",
        data={"key": api_key, "image": base64.b64encode(img_bytes).decode()}
    ) as r:
        res = await r.json(content_type=None)

    if not res.get("success"):
        print(res)
        return None

    d = res["data"]
    return {
        "url": d["url"],
        "thumb": d["thumb"]["url"],
        "delete_url": d["delete_url"],
        "width": d["width"],
        "height": d["height"],
        "size": d["size"],
        "mime": d["image"].get("mime", "image/jpeg"),
        "name": d["image"]["name"],
    }