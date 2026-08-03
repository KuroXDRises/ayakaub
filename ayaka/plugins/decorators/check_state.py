import time
import functools
from ..data import AFK_DATA
from ..utilities.afk import remove_afk

# how long AFK can stay active before it's considered stale and auto-cleared
AFK_EXPIRY_SECONDS = 24 * 60 * 60  # 24h, change as needed


def is_afk_expired() -> bool:
    """True if AFK is currently on but has been active longer than the expiry window."""
    if not AFK_DATA.status or not AFK_DATA.afk_time:
        return False
    return (time.time() - AFK_DATA.afk_time) > AFK_EXPIRY_SECONDS


def check_afk_expiry(func):
    """Decorator for handlers: auto-clears AFK state if it has expired, then runs the handler as normal."""
    @functools.wraps(func)
    async def wrapper(c, m, *args, **kwargs):
        if is_afk_expired():
            remove_afk()
        return await func(c, m, *args, **kwargs)
    return wrapper


def require_afk_active(func):
    """Decorator for handlers that should only run while AFK is actually on (and not expired)."""
    @functools.wraps(func)
    async def wrapper(c, m, *args, **kwargs):
        if is_afk_expired():
            remove_afk()
        if not AFK_DATA.status:
            return
        return await func(c, m, *args, **kwargs)
    return wrapper


def require_afk_inactive(func):
    """Decorator for handlers that should only run while AFK is off (e.g. the /afk command itself,
    to avoid double-setting)."""
    @functools.wraps(func)
    async def wrapper(c, m, *args, **kwargs):
        if is_afk_expired():
            remove_afk()
        if AFK_DATA.status:
            return
        return await func(c, m, *args, **kwargs)
    return wrapper
