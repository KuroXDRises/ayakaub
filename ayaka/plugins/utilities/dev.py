import traceback
import aiohttp
import asyncio
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from config import Config

eval_helper = {
    "result":None,
    "code":None,
    "chat_id":None,
    'message_id':None,
    'sent_id':None,
    "paste_id":None,
    "googleit_url":None
}

async def aexec(code: str, client, msg):
    # Telegram formatting / copy-paste can inject invisible unicode chars
    # (non-breaking space, zero-width space, etc.) that break exec()'s parser.
    code = (
        code.replace("\u00a0", " ")   # non-breaking space
            .replace("\u200b", "")    # zero-width space
            .replace("\u200c", "")    # zero-width non-joiner
            .replace("\u200d", "")    # zero-width joiner
            .replace("\ufeff", "")    # BOM
    )

    local_vars = {
        "app": client,
        "msg": msg,
        "m": msg,
        "r": msg.reply_to_message,
        "p": print,
        "here": msg.chat.id,
        "me": msg.from_user.id,
        "__name__": __name__,
        "__package__": __package__
    }

    exec(
        "async def __ex():\n" +
        "\n".join(f"    {line}" for line in code.splitlines()),
        local_vars
    )

    return await local_vars["__ex"]()



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
    """Shared by eval and sh: paste to Pastebin if output is too long."""
    if final.count("\n") + 1 > 20:
        try:
            url = await paste_to_pastebin(final)
            eval_helper["paste_id"] = url.rsplit("/", 1)[-1]
            preview = "\n".join(final.splitlines()[:20])
            return f"{preview}\n\n... output too long, full result: {url}"
        except Exception:
            pass
    return final


async def get_output(parts, c, m):
    code = parts[1]

    buffer = StringIO()
    result = exception = None

    try:
        with redirect_stdout(buffer), redirect_stderr(buffer):
            result = await aexec(code, c, m)
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
    stdout, _ = await process.communicate()
    return stdout.decode(errors="ignore").strip()


async def get_sh_output(parts, c, m):
    cmd = parts[1]

    try:
        output = await sh_exec(cmd)
    except Exception:
        output = traceback.format_exc()

    final = output if output else "Done."
    return await finalize_output(final)