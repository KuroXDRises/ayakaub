import traceback
import aiohttp
import asyncio
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from config import Config

EXEC_TIMEOUT = 60  # seconds, applies to both eval and sh

eval_helper = {
    "result": None,
    "code": None,
    "chat_id": None,
    'message_id': None,
    'sent_id': None,
    "paste_id": None,
    "googleit_url": None,
    # set by a command handler right before relaying through
    # get_inline_bot_results, so the inline handler (which otherwise only
    # sees the bot's own identity when the bot queries itself) can pick up
    # the REAL user who ran the command instead.
    "pending_user": None,
    "pending_chat_id": None,
    "pending_reply": None
}


async def aexec(code: str, c, m):
    code = (
        code.replace("\u00a0", " ")
            .replace("\u200b", "")
            .replace("\u200c", "")
            .replace("\u200d", "")
            .strip()
    )

    # Indent every line so blank lines cannot terminate the async function
    # body.  This is important for multiline/triple-quoted source blocks.
    import textwrap
    indented = textwrap.indent(code, "    ", lambda _line: True)

    local_vars = {
        "c": c,
        "m": m,
        "app": c,
        "r": m.reply_to_message,
        "r_user": m.reply_to_message.from_user,
        "user": m.from_user,
    }
    buffer = StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = buffer
        exec(
            f"async def __ex():\n{indented}",
            local_vars
        )
        result = await local_vars["__ex"]()
    finally:
        sys.stdout = old_stdout
    printed = buffer.getvalue()

    if result is not None:
        return printed + str(result) if printed else str(result)
    return printed or "Done."


async def paste_to_pastebin(content: str) -> str:
    async with aiohttp.ClientSession() as session:
        data = {
            "api_dev_key": Config.PASTE_BIN_API,
            "api_option": "paste",
            "api_paste_code": content,
            "api_paste_private": 1,
            "api_paste_expire_date": "1D"
        }
        async with session.post("https://pastebin.com/api/api_post.php", data=data) as resp:
            res = await resp.text()
            if not res.startswith("http"):
                raise RuntimeError(f"Pastebin error: {res}")
            return res


async def finalize_output(final: str) -> str:
    char_limit = 4000  # Telegram message limit
    if len(final) > char_limit:
        try:
            url = await paste_to_pastebin(final)
            eval_helper["paste_id"] = url.rsplit("/", 1)[-1]
            preview = final[:1000]
            return f"{preview}\n\n... output too long, full result: {url}"
        except Exception:
            pass
        return final[:char_limit]
    return final


async def get_output(parts, c, m):
    code = parts[1]

    buffer = StringIO()
    result = exception = None

    try:
        with redirect_stdout(buffer), redirect_stderr(buffer):
            result = await asyncio.wait_for(aexec(code, c, m), timeout=EXEC_TIMEOUT)
    except asyncio.TimeoutError:
        exception = f"⏱ Execution timed out (>{EXEC_TIMEOUT}s). Possible infinite loop or blocking call."
    except Exception:
        exception = traceback.format_exc()

    output = buffer.getvalue()

    if exception:
        final = exception
    elif output:
        final = output
    elif result is not None:
        final = str(result)
    else:
        final = "Done."

    return await finalize_output(final)


async def sh_exec(cmd: str) -> str:
    cmd = (
        cmd.replace("\u00a0", " ")
           .replace("\u200b", "")
           .replace("\u200c", "")
           .replace("\u200d", "")
           .replace("\ufeff", "")
    )

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    try:
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout=EXEC_TIMEOUT)
        return stdout.decode(errors="ignore").strip()
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return f"⏱ Command timed out (>{EXEC_TIMEOUT}s) and was killed."


async def get_sh_output(parts, c, m):
    cmd = parts[1]

    try:
        output = await sh_exec(cmd)
    except Exception:
        output = traceback.format_exc()

    final = output if output else "Done."
    return await finalize_output(final)
