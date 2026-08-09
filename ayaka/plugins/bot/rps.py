import random
from pyrogram import Client, filters
from pyrogram import types
from pyrogram import enums
from ..data import RPS_STATE
from ..data.rps_data import SELECTIONS
from ..filters import ADMINS


def create_rps_user_structure(user_id: int) -> dict:
    return {"id": user_id, "selection": None}


def _emoji_for(selection_id: int | None) -> str:
    if selection_id is None:
        return "❔"
    for entry in SELECTIONS:
        for _, x in entry.items():
            if x["id"] == selection_id:
                return x["emoji"]
    return "❔"


def _determine_winner(s1: int, s2: int) -> int:
    # Returns 1 if p1 wins, 2 if p2 wins, 0 if draw
    # Assumes SELECTIONS has beats field per entry
    for entry in SELECTIONS:
        for _, x in entry.items():
            if x["id"] == s1:
                if s2 in x.get("beats", []):
                    return 1
                elif s1 == s2:
                    return 0
                else:
                    return 2
    return 0


def _build_board_text(p1: int, p2: int, reveal: bool = False) -> str:
    s1 = next((u["selection"] for u in RPS_STATE.players if u["id"] == p1), None)
    s2 = next((u["selection"] for u in RPS_STATE.players if u["id"] == p2), None)
    e1 = _emoji_for(s1) if reveal else ("✅" if s1 is not None else "❔")
    e2 = _emoji_for(s2) if reveal else ("✅" if s2 is not None else "❔")
    return (
        f"**「 Rock Paper Scissors 」**\n\n"
        f"**[Player 1](tg://user?id={p1})** » {e1}\n"
        f"**[Player 2](tg://user?id={p2})** » {e2}\n\n"
    )


def _build_selection_keyboard() -> types.InlineKeyboardMarkup:
    buttons = []
    for entry in SELECTIONS:
        for _, x in entry.items():
            buttons.append(types.InlineKeyboardButton(
                text=x["emoji"],
                callback_data=f"select_rps:{x['id']}",
                style=enums.ButtonStyle.PRIMARY
            ))
    return types.InlineKeyboardMarkup([buttons])


@Client.on_inline_query(filters.regex(r"^rps") & ADMINS.inline())
async def rps_inline(c: Client, q: types.InlineQuery):
    if RPS_STATE.status:
        return

    text = (
        f"**《 Rock Paper Scissors 》**\n"
        f"__[{q.from_user.first_name}](tg://user?id={q.from_user.id}) "
        f"hosted a `Rock Paper Scissors` game.__\n"
        f"__Press the button below to play.__"
    )
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(
            "⚔️ Play RPS",
            callback_data=f"play_rps:{q.from_user.id}",
            style=enums.ButtonStyle.PRIMARY
        )
    ]])
    await q.answer([
        types.InlineQueryResultArticle(
            title="Rock Paper Scissors",
            description="Play Rock Paper Scissors with friends.",
            input_message_content=types.InputTextMessageContent(message_text=text),
            reply_markup=keyboard
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^play_rps:(\d+)$"))
async def play_rps_button(c: Client, cq: types.CallbackQuery):
    p1 = int(cq.matches[0].group(1))
    p2 = cq.from_user.id

    if p1 == p2:
        return await cq.answer("You can't play against yourself.", show_alert=True)
    if RPS_STATE.status:
        return await cq.answer("A game is already in progress.", show_alert=True)

    RPS_STATE.status  = True
    RPS_STATE.p1_id   = p1
    RPS_STATE.p2_id   = p2
    RPS_STATE.players = [
        create_rps_user_structure(p1),
        create_rps_user_structure(p2),
    ]

    text = _build_board_text(p1, p2) + "__Make your moves!__"

    await c.edit_inline_text(
        inline_message_id=cq.inline_message_id,
        text=text,
        reply_markup=_build_selection_keyboard()
    )
    await cq.answer("Game started!")


@Client.on_callback_query(filters.regex(r"^select_rps:(\d+)$"))
async def select_rps_button(c: Client, cq: types.CallbackQuery):
    uid = cq.from_user.id

    if not RPS_STATE.status:
        return await cq.answer("No active game.", show_alert=True)

    player = next((u for u in RPS_STATE.players if u["id"] == uid), None)
    if not player:
        return await cq.answer("You are not a player in this game.", show_alert=True)

    if player["selection"] is not None:
        return await cq.answer("You already made your selection!", show_alert=True)

    player["selection"] = int(cq.matches[0].group(1))
    await cq.answer("✅ Selection saved!")

    p1_id = RPS_STATE.p1_id
    p2_id = RPS_STATE.p2_id
    s1    = next((u["selection"] for u in RPS_STATE.players if u["id"] == p1_id), None)
    s2    = next((u["selection"] for u in RPS_STATE.players if u["id"] == p2_id), None)

    if s1 is None or s2 is None:
        # Still waiting for the other player
        text = _build_board_text(p1_id, p2_id) + "__Waiting for the other player...__"
        await c.edit_inline_text(
            inline_message_id=cq.inline_message_id,
            text=text,
            reply_markup=_build_selection_keyboard()
        )
        return

    # Both selected — resolve
    winner = _determine_winner(s1, s2)

    if winner == 0:
        result_text = "🤝 **It's a Draw!**"
    elif winner == 1:
        result_text = f"🏆 **[Player 1](tg://user?id={p1_id}) Wins!**"
    else:
        result_text = f"🏆 **[Player 2](tg://user?id={p2_id}) Wins!**"

    text = _build_board_text(p1_id, p2_id, reveal=True) + result_text

    await c.edit_inline_text(
        inline_message_id=cq.inline_message_id,
        text=text,
        reply_markup=None
    )

    RPS_STATE.status  = False
    RPS_STATE.players = []
    RPS_STATE.p1_id   = None
    RPS_STATE.p2_id   = None