import asyncio
import json
import os


class PremiumEmojiMethods:
    def __init__(self, path: str = None):
        self.path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "emojis.json")
        self.lock = asyncio.Lock()
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def _write(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    async def _save(self):
        await asyncio.to_thread(self._write)

    async def is_premium_emoji(self, key: str) -> bool:
        return key.lower() in self.data

    async def get_premium_emoji(self, key: str):
        key = key.lower()
        doc = self.data.get(key)
        return {"key": key, **doc} if doc else None

    async def add_premium_emoji(self, emoji_id: int, key: str) -> bool:
        key = key.lower()
        async with self.lock:
            self.data[key] = {
                "emoji_id": emoji_id,
                "html": f'<tg-emoji emoji-id="{emoji_id}">{key}</tg-emoji>'
            }
            await self._save()
        return True

    async def remove_premium_emoji(self, key: str) -> bool:
        key = key.lower()
        async with self.lock:
            if key not in self.data:
                return False
            del self.data[key]
            await self._save()
        return True

    async def get_all_premium_emojis(self) -> list:
        return [{"key": k, "html": v["html"]} for k, v in self.data.items()]

    async def generate_premium_text(self, text: str) -> str:
        emojis = sorted(await self.get_all_premium_emojis(), key=lambda e: len(e["key"]), reverse=True)
        if not emojis:
            return text
        result = []
        i = 0
        n = len(text)
        while i < n:
            matched = False
            for e in emojis:
                key = e["key"]
                klen = len(key)
                if klen and text[i:i + klen].lower() == key:
                    result.append(e["html"])
                    i += klen
                    matched = True
                    break
            if not matched:
                result.append(text[i])
                i += 1
        return "".join(result)

    async def migrate_all_emojis(self) -> dict:
        summary = {"updated": 0, "skipped": 0, "failed": []}
        async with self.lock:
            migrated = {}
            for raw_key, doc in self.data.items():
                emoji_id = doc.get("emoji_id") if isinstance(doc, dict) else None
                if emoji_id is None:
                    summary["failed"].append(raw_key)
                    migrated[raw_key] = doc
                    continue
                new_key = str(raw_key).lower()
                new_html = f'<tg-emoji emoji-id="{emoji_id}">{new_key}</tg-emoji>'
                if new_key == raw_key and doc.get("html") == new_html:
                    summary["skipped"] += 1
                else:
                    summary["updated"] += 1
                migrated[new_key] = {"emoji_id": emoji_id, "html": new_html}
            self.data = migrated
            await self._save()
        return summary

premiumEmojiMethods = PremiumEmojiMethods()