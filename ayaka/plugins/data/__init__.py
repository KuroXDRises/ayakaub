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

@dataclass
class QuoteState:
    status: bool = False
    chat_id: int | None = None
    message_id: int | None = None
    topic_id: int | None = None

QUOTE_STATE = QuoteState()

@dataclass
class PrivateChatState:
    status: bool = False
    time_limit: int = 120
    approved = set()

PRIVATE_CHAT_STATE = PrivateChatState()