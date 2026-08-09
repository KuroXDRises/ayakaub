from pyrogram import Client, filters
from pyrogram import types, enums
from ..data.xo_state import XO_GAME
from ..filters import ADMINS
from config import Config

SYMBOLS = {" ": "⬜", "X": "❌", "O": "⭕"}


def build_board_keyboard() -> types.InlineKeyboardMarkup:
    rows = []
    for r in range(3):
        row = []
        for c in range(3):
            idx = r * 3 + c
            row.append(types.InlineKeyboardButton(
                SYMBOLS[XO_GAME.board[idx]],
                callback_data=f"xo_move:{idx}"
            ))
        rows.append(row)
    rows.append([types.InlineKeyboardButton("❌ Quit", callback_data="xo_quit", style=enums.ButtonStyle.DANGER)])
    return types.InlineKeyboardMarkup(rows)


def build_status_text() -> str:
    x_mention = f"[❌ Player](tg://user?id={XO_GAME.player_x})"
    o_mention = f"[⭕ Player](tg://user?id={XO_GAME.player_o})"

    winner = XO_GAME.winner()
    if winner:
        winner_mention = x_mention if winner == "X" else o_mention
        return f"**「 Tic Tac Toe 」**\n{x_mention} vs {o_mention}\n\n🏆 {winner_mention} wins!"

    if XO_GAME.is_draw():
        return f"**「 Tic Tac Toe 」**\n{x_mention} vs {o_mention}\n\n🤝 It's a draw!"

    turn_mention = x_mention if XO_GAME.turn == XO_GAME.player_x else o_mention
    return f"**「 Tic Tac Toe 」**\n{x_mention} vs {o_mention}\n\n▶️ Turn: {turn_mention}"


@Client.on_inline_query(filters.regex(r"^xo") & ADMINS.inline())
async def xo_inline(c: Client, q: types.InlineQuery):
    if XO_GAME.active:
        return

    text = (
        "**《 Tic Tac Toe 》**\n"
        f"__[{q.from_user.first_name}](tg://user?id={q.from_user.id}) hosted a `Tic Tac Toe` game.__\n"
        "__Press the button below to play with them.__"
    )
    keyboard = types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("Play XO", callback_data=f"join_xo:{q.from_user.id}", style=enums.ButtonStyle.PRIMARY)]
    ])
    await q.answer([
        types.InlineQueryResultArticle(
            title="Tic Tac Toe",
            description="Play Tic Tac Toe with friends.",
            input_message_content=types.InputTextMessageContent(message_text=text),
            reply_markup=keyboard
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^join_xo:"))
async def join_xo_button(c: Client, cq: types.CallbackQuery):
    host_id = int(cq.data.split(":", 1)[1])
    joiner_id = cq.from_user.id

    if host_id == joiner_id:
        await cq.answer("You can't challenge yourself.")
        return

    if XO_GAME.active:
        await cq.answer("A game already started.")
        return

    XO_GAME.start(x_id=host_id, o_id=joiner_id)

    await cq.edit_message_text(
        build_status_text(),
        reply_markup=build_board_keyboard()
    )
    await cq.answer()


@Client.on_callback_query(filters.regex(r"^xo_move:"))
async def xo_move_button(c: Client, cq: types.CallbackQuery):
    if not XO_GAME.active:
        await cq.answer("No game in progress.")
        return

    user_id = cq.from_user.id
    if user_id not in (XO_GAME.player_x, XO_GAME.player_o):
        await cq.answer("You're not in this game.")
        return

    if XO_GAME.is_over():
        await cq.answer("The game already ended.")
        return

    cell = int(cq.data.split(":", 1)[1])

    if user_id != XO_GAME.turn:
        await cq.answer("It's not your turn.")
        return

    if not XO_GAME.play(user_id, cell):
        await cq.answer("That cell is taken.")
        return

    await cq.edit_message_text(build_status_text(), reply_markup=build_board_keyboard())

    if XO_GAME.is_over():
        XO_GAME.reset()

    await cq.answer()


@Client.on_callback_query(filters.regex(r"^xo_quit$"))
async def xo_quit_button(c: Client, cq: types.CallbackQuery):
    if not XO_GAME.active:
        await cq.answer("No game in progress.")
        return

    user_id = cq.from_user.id
    if user_id not in (XO_GAME.player_x, XO_GAME.player_o):
        await cq.answer("You're not in this game.")
        return

    quitter = "❌ Player" if user_id == XO_GAME.player_x else "⭕ Player"
    XO_GAME.reset()

    await cq.edit_message_text(f"**「 Tic Tac Toe 」**\n\n🚪 {quitter} left the game.")
    await cq.answer()
