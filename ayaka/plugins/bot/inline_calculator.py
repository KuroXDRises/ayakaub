"""Admin-only inline calculator and symbolic equation solver."""

import html
import re

from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputRichMessage,
    InputRichMessageContent,
)
from sympy import E, I, pi, Eq, N, factor, simplify, solve, sympify
from sympy.abc import _clash1
from sympy.core.sympify import SympifyError

from ..filters import ADMINS


SEP = "━━━━━━━━━━━━━━━━━━━━"
MAX_QUERY_LENGTH = 500
SAFE_CHARACTERS = re.compile(r"^[0-9A-Za-z_+\-*/%^().,=;\s]+$")
LOCALS = {
    **_clash1,
    "pi": pi,
    "e": E,
    "I": I,
    "sqrt": __import__("sympy").sqrt,
    "sin": __import__("sympy").sin,
    "cos": __import__("sympy").cos,
    "tan": __import__("sympy").tan,
    "log": __import__("sympy").log,
    "ln": __import__("sympy").log,
    "exp": __import__("sympy").exp,
    "abs": __import__("sympy").Abs,
    "factor": factor,
    "simplify": simplify,
}


def _parse(expression: str):
    expression = expression.strip().replace("^", "**")
    if not expression or len(expression) > MAX_QUERY_LENGTH:
        raise ValueError("Enter a calculation up to 500 characters long.")
    if not SAFE_CHARACTERS.fullmatch(expression) or "__" in expression:
        raise ValueError("Use only mathematical numbers, variables, operators, and functions.")
    return expression


def calculate(query: str) -> str:
    """Evaluate an expression or solve equations separated by semicolons."""
    expression = _parse(query)
    equations = [part.strip() for part in expression.split(";") if part.strip()]

    if any("=" in equation for equation in equations):
        parsed = []
        for equation in equations:
            if equation.count("=") != 1:
                raise ValueError("Each equation must contain exactly one `=`.")
            left, right = equation.split("=", 1)
            parsed.append(Eq(sympify(left, locals=LOCALS), sympify(right, locals=LOCALS)))
        variables = sorted(set().union(*(equation.free_symbols for equation in parsed)), key=str)
        if not variables:
            return "True" if all(bool(equation) for equation in parsed) else "False"
        result = solve(parsed, variables, dict=True)
        return str(result) if result else "No solution found."

    value = sympify(expression, locals=LOCALS)
    # Keep exact results useful (e.g. pi/2), while evaluating ordinary decimals.
    return str(N(value) if value.is_number and value.is_Float else simplify(value))


def result_card(query: str, result: str) -> str:
    return (
        "<h3>🧮 Calculator</h3>\n"
        f"<i>{SEP}</i>\n"
        f"<p><b>Input</b></p><pre><code>{html.escape(query)}</code></pre>\n"
        f"<i>{SEP}</i>\n"
        f"<p><b>Result</b></p><pre><code>{html.escape(result)}</code></pre>"
    )


@Client.on_inline_query(filters.regex(r"^(?:calc|calculate)\s+(.+)") & ADMINS.inline())
async def calculator_inline(c: Client, q: InlineQuery):
    query = q.matches[0].group(1).strip()
    try:
        result = calculate(query)
        title = f"🧮 {result[:55]}"
    except (SympifyError, SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        result = f"Error: {error}"
        title = "❌ Invalid calculation"

    await q.answer([
        InlineQueryResultArticle(
            title=title,
            description="Calculate expressions or solve equations",
            input_message_content=InputRichMessageContent(
                rich_message=InputRichMessage(html=result_card(query, result))
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑 Close", callback_data="close_calculator", style=ButtonStyle.DANGER)]
            ]),
        )
    ], cache_time=0)


@Client.on_callback_query(filters.regex(r"^close_calculator$") & ADMINS.callback())
async def close_calculator(c: Client, cq: CallbackQuery):
    if cq.inline_message_id:
        await c.edit_inline_text(cq.inline_message_id, "<b>🧮 Calculator closed.</b>")
    elif cq.message:
        await cq.message.edit_text("<b>🧮 Calculator closed.</b>")
    await cq.answer("Closed.")
