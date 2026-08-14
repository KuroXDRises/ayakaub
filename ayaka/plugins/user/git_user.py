from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters
from ..filters import ADMINS
from ayaka import cmd
from config import Config


@Client.on_message(cmd(["git_user"]) & ADMINS.message(), group=13)
async def git_user_command(userbot:Client, message:Message):
    if len(message.command)!=2:
        await message.reply("**Usage:** `.git_user {username}`\n**Example:** `.git_user @KuroXDRises`")
    else:
        query = message.command[1]
        results = await userbot.get_inline_bot_results(
            bot=Config.BOT_USERNAME,
            query=f"git_user {query}"
        )
        await userbot.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=results.query_id,
            result_id=results.results[0].id,
            reply_parameters=ReplyParameters(message_id=message.id)
        )