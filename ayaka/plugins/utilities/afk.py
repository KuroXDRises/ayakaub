import time
from ..data import AFK_DATA

NOTIFY_COOLDOWN = 300  # 5 minutes — one notice per user per this window


def set_afk(
    reason: str = "Not Provided",
    media_from_chat: int | None = None,
    message_media_id: int | None = None
) -> None:
    AFK_DATA.status = True
    AFK_DATA.reason = reason
    AFK_DATA.afk_time = time.time()
    AFK_DATA.media_from_chat = media_from_chat
    AFK_DATA.message_media_id = message_media_id
    AFK_DATA.users.clear()


def remove_afk() -> None:
    AFK_DATA.status = False
    AFK_DATA.reason = None
    AFK_DATA.afk_time = None
    AFK_DATA.media_from_chat = None
    AFK_DATA.message_media_id = None
    AFK_DATA.users.clear()


def is_afk() -> bool:
    return AFK_DATA.status


def get_afk_duration() -> float:
    """Seconds since AFK was set. Returns 0 if not currently AFK."""
    if not AFK_DATA.status or not AFK_DATA.afk_time:
        return 0.0
    return time.time() - AFK_DATA.afk_time


def format_afk_duration() -> str:
    seconds = int(get_afk_duration())
    if seconds < 60:
        return f"{seconds}s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {minutes}m"
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h"


def has_been_notified(user_id: int) -> bool:
    """True if this user was already notified within the cooldown window."""
    last = AFK_DATA.users.get(user_id)
    if last is None:
        return False
    return (time.time() - last) < NOTIFY_COOLDOWN


def mark_notified(user_id: int) -> None:
    AFK_DATA.users[user_id] = time.time()


def has_afk_media() -> bool:
    return AFK_DATA.media_from_chat is not None and AFK_DATA.message_media_id is not None
