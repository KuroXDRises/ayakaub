from dataclasses import dataclass, field

@dataclass
class AfkState:
    status: bool = False
    reason: str | None = None
    afk_time: float | None = None
    media_from_chat: int | None = None
    message_media_id: int | None = None
    users: dict[int, float] = field(default_factory=dict)  # user_id -> last_notified_at

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

@dataclass
class SilentState:
    status: bool = False
    chat_ids = set()

SILENT_STATE = SilentState()

@dataclass
class RPSState:
    status: bool = False
    players = []
    p1_id: int | None = None
    p2_id: int | None = None

RPS_STATE = RPSState()