from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrogram.enums import ButtonStyle
from ..data.help_data import HELP_DATA
from ayaka import cmd

SEP = "━━━━━━━━━━━━━━━━━━━━"


# ───────────────────────── message builders ─────────────────────────

def build_help_message() -> str:
    return (
        "<b>❀ 𝑨𝒚𝒂𝒌𝒂 • 𝑯𝒆𝒍𝒑 ❀</b>\n"
        f"{SEP}\n"
        "<i>Welcome!</i> Browse Ayaka's commands by selecting a category below.\n"
        f"{SEP}\n"
        "<b>⌬ Choose A Category ⌬</b>\n"
        "Tap any button below to view its commands and usage.\n"
        f"{SEP}"
    )


def build_category_message(category_name: str, cat_info: dict) -> str:
    lines = [f"<b>{category_name}</b>", SEP]
    for cmd_name in cat_info["commands"]:
        lines.append(f"➤ **{cmd_name}**")
    lines.append(SEP)
    return "\n".join(lines)


def build_command_message(cmd_name: str, info: dict) -> str:
    text = (
        f"<b>{cmd_name.capitalize()}</b>\n"
        f"{SEP}\n"
        f"<b>Description</b> > {info['description']}\n"
        f"{SEP}\n"
        f"<pre><code>{info['usage']}</code></pre>\n"
        f"{SEP}"
    )
    if info.get("note"):
        text += f"\n<b>[Note]</b>: {info['note']}"
    if info.get("aliases"):
        aliases = ", ".join(f"/{a}" for a in info["aliases"])
        text += f"\n<b>[Aliases]</b>: {aliases}"
    return text


# ───────────────────────── keyboard builders ─────────────────────────

def build_home_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for category_name, cat_info in HELP_DATA.items():
        row.append(InlineKeyboardButton(category_name, callback_data=cat_info["callback"], style=ButtonStyle.PRIMARY))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="help_close", style=ButtonStyle.DANGER)])
    return InlineKeyboardMarkup(buttons)


def build_category_keyboard(cat_info: dict) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for cmd_name, info in cat_info["commands"].items():
        row.append(InlineKeyboardButton(f"/{cmd_name}", callback_data=info["callback"], style=ButtonStyle.PRIMARY))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="help_home", style=ButtonStyle.DANGER)])
    return InlineKeyboardMarkup(buttons)


def build_command_keyboard(category_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data=category_callback, style=ButtonStyle.DANGER)]
    ])


# ───────────────────────── lookups ─────────────────────────

def find_category(callback_data: str):
    for category_name, cat_info in HELP_DATA.items():
        if cat_info["callback"] == callback_data:
            return category_name, cat_info
    return None


def find_command(callback_data: str):
    """Returns (category_name, cat_info, cmd_name, info) or None."""
    for category_name, cat_info in HELP_DATA.items():
        for cmd_name, info in cat_info["commands"].items():
            if info["callback"] == callback_data:
                return category_name, cat_info, cmd_name, info
    return None


# ───────────────────────── edit helper ─────────────────────────

async def _edit(c: Client, cq: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    """Try editing via inline_message_id first (the direct path for
    inline-originated messages); fall back to cq.message.edit_text for
    regular (command-originated) messages where inline_message_id is None
    or the inline edit otherwise fails."""
    try:
        await c.edit_inline_text(
            inline_message_id=cq.inline_message_id,
            text=text,
            reply_markup=reply_markup
        )
    except Exception:
        await cq.message.edit_text(text, reply_markup=reply_markup)


# ───────────────────────── handlers ─────────────────────────

async def _send_help(m: Message):
    await m.reply_text(build_help_message(), reply_markup=build_home_keyboard())


@Client.on_message(cmd(["help"]), group=869)
async def help_command(c: Client, m: Message):
    await _send_help(m)


@Client.on_business_message(cmd(["help"]), group=869)
async def help_business_command(c: Client, m: Message):
    await _send_help(m)


@Client.on_callback_query(filters.regex(r"^cat_"))
async def help_category_callback(c: Client, cq: CallbackQuery):
    result = find_category(cq.data)
    if not result:
        await cq.answer("Category not found.", show_alert=True)
        return
    category_name, cat_info = result
    await _edit(
        c, cq,
        build_category_message(category_name, cat_info),
        build_category_keyboard(cat_info)
    )
    await cq.answer()


@Client.on_callback_query(filters.regex(r"^help_(?!home$|close$)"))
async def help_command_callback(c: Client, cq: CallbackQuery):
    result = find_command(cq.data)
    if not result:
        await cq.answer("Command not found.", show_alert=True)
        return
    category_name, cat_info, cmd_name, info = result
    await _edit(
        c, cq,
        build_command_message(cmd_name, info),
        build_command_keyboard(cat_info["callback"])
    )
    await cq.answer()


@Client.on_callback_query(filters.regex(r"^help_home$"))
async def help_home_callback(c: Client, cq: CallbackQuery):
    await _edit(c, cq, build_help_message(), build_home_keyboard())
    await cq.answer()


@Client.on_callback_query(filters.regex(r"^help_close$"))
async def help_close_callback(c: Client, cq: CallbackQuery):
    # inline-sent messages can't be deleted via the Bot API (Telegram has no
    # such method) — only edited. Regular messages CAN be deleted, so only
    # do that when cq.message actually exists.
    if cq.message:
        await cq.message.delete()
    else:
        await _edit(c, cq, "❌ <b>Closed.</b>")
    await cq.answer("Closed.")
