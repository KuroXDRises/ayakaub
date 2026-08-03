from dataclasses import dataclass, field


@dataclass
class AfkState:
    status: bool = False
    reason: str | None = None
    afk_time: float | None = None
    media_from_chat: int | None = None
    message_media_id: int | None = None
    users: list[int] = field(default_factory=list)


AFK_DATA = AfkState()
