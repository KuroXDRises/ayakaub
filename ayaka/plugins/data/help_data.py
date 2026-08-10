HELP_DATA = {
    "🤖 AI": {
        "callback": "cat_ai",
        "commands": {
            "ai": {
                "aliases": ["ask"],
                "usage": "/ai <question>",
                "description": "Ask AyakaAI a question — returns an HTML-formatted answer.",
                "callback": "help_ai"
            },
            "ayaka": {
                "aliases": [],
                "usage": "ayaka (bot_username) [query] (guest_mode)",
                "description": "Ask AyakaAI a question – returns an HTML formatted answer.",
                "callback": "help_ayaka_guest"
            },
            "anime": {
                "aliases": [],
                "usage": "anime [anime-name] (inline)",
                "description": "Search your desired anime – AI will search it for you.",
                "callback": "help_anime"
            }
        }
    },
    "🛠 Developer": {
        "callback": "cat_dev",
        "commands": {
            "eval": {
                "aliases": ["e"],
                "usage": "/eval <code>",
                "description": "Execute Python code — shows output/errors, or a Pastebin link if the output is too long.",
                "callback": "help_eval"
            },
            "sh": {
                "aliases": [],
                "usage": "/sh <command>",
                "description": "Run a shell command on the server.",
                "callback": "help_sh"
            },
            "logs": {
                "aliases": [],
                "usage": "/logs",
                "description": "View the bot's log file, with Clear/Refresh buttons.",
                "callback": "help_logs"
            },
            "type": {
                "aliases": [],
                "usage": "/type <text>",
                "description": "Send text with a typing animation effect.",
                "callback": "help_type"
            },
            "parse": {
                "aliases": [],
                "usage": "parse <html> (inline)",
                "description": "Send raw rich-text HTML as a formatted message.",
                "callback": "help_parse",
                "note": "Inline only — type it as @YourBot parse <html> in any chat."
            },
        }
    },
    "👥 Group Management": {
        "callback": "cat_group",
        "commands": {
            "ban": {
                "aliases": ["dban"],
                "usage": "/ban <reply|username|id>",
                "description": "Ban a user from the group. dban also deletes their message.",
                "callback": "help_ban",
                "note": "Reply to a user, or give their username/ID."
            },
            "unban": {
                "aliases": [],
                "usage": "/unban <reply|username|id>",
                "description": "Unban a user.",
                "callback": "help_unban",
                "note": "Reply to a user, or give their username/ID."
            },
            "mute": {
                "aliases": ["tmute"],
                "usage": "/mute <target> or /tmute <target> <duration>",
                "description": "Mute a user. tmute needs a duration — e.g. 10m, 2h, 1d.",
                "callback": "help_mute",
                "note": "Duration accepts s/m/h/d suffixes, e.g. 30m, 2h, 1d."
            },
            "unmute": {
                "aliases": [],
                "usage": "/unmute <target>",
                "description": "Unmute a user.",
                "callback": "help_unmute"
            },
            "promote": {
                "aliases": [],
                "usage": "/promote <target> <title>",
                "description": "Promote a user to admin with a custom title (max 16 characters).",
                "callback": "help_promote",
                "note": "Custom title is capped at 16 characters by Telegram."
            },
            "demote": {
                "aliases": [],
                "usage": "/demote <target>",
                "description": "Remove a user's admin rights.",
                "callback": "help_demote"
            },
            "delete": {
                "aliases": ["del"],
                "usage": "/delete (reply)",
                "description": "Delete the message being replied to.",
                "callback": "help_delete",
                "note": "Must be used as a reply."
            },
            "purge": {
                "aliases": [],
                "usage": "/purge (reply)",
                "description": "Delete every message from the reply up to the current one.",
                "callback": "help_purge",
                "note": "Must be used as a reply."
            },
        }
    },
    "🔒 Privacy": {
        "callback": "cat_privacy",
        "commands": {
            "pmpermit": {
                "aliases": [],
                "usage": "/pmpermit on|off",
                "description": "Turn PM Permit on or off.",
                "callback": "help_pmpermit"
            },
            "approve_pm": {
                "aliases": [],
                "usage": "/approve_pm (reply)",
                "description": "Approve a user to DM you.",
                "callback": "help_approve_pm",
                "note": "Must be used as a reply to the user."
            },
            "disapprove_pm": {
                "aliases": [],
                "usage": "/disapprove_pm (reply)",
                "description": "Revoke a user's approval to DM you.",
                "callback": "help_disapprove_pm",
                "note": "Must be used as a reply to the user."
            },
            "pmstatus": {
                "aliases": [],
                "usage": "/pmstatus",
                "description": "Check PM Permit status and the list of approved users.",
                "callback": "help_pmstatus"
            },
            "afk": {
                "aliases": [],
                "usage": "/afk [reason]",
                "description": "Mark yourself AFK, with an optional reason.",
                "callback": "help_afk"
            },
            "unafk": {
                "aliases": [],
                "usage": "/unafk",
                "description": "Clear AFK status.",
                "callback": "help_unafk"
            },
            "block": {
                "aliases": [],
                "usage": "/block (reply)",
                "description": "Block a user.",
                "callback": "help_block",
                "note": "Must be used as a reply."
            },
            "unblock": {
                "aliases": [],
                "usage": "/unblock (reply)",
                "description": "Unblock a user.",
                "callback": "help_unblock",
                "note": "Must be used as a reply."
            },
            "silent": {
                "aliases": [],
                "usage": "/silent",
                "description": "Silent a chat\'s messages, The userbot will read it for you.",
                "callback": "help_silent"
            },
            "unsilent": {
                "aliases": [],
                "usage": "/unsilent",
                "description": "Unsilent all chat\'s messages, The userbot will not read them.",
                "callback": "help_unsilent"
            },
            "unsilent_chat": {
                "aliases": [],
                "usage": "/unsilent_chat",
                "description": "Unsilent a chat\'s messages, The userbot will not read them.",
                "callback": "help_unsilent_chat"
            },
            "silent_status": {
                "aliases": [],
                "usage": "/silent_status",
                "description": "Check the Silent State status and the approved user\'s list.",
                "callback": "help_silent_status"
            },
        }
    },
    "💬 Misc": {
        "callback": "cat_misc",
        "commands": {
            "ping": {
                "aliases": [],
                "usage": "/ping",
                "description": "Check the bot's response speed.",
                "callback": "help_ping"
            },
            "alive": {
                "aliases": [],
                "usage": "/alive",
                "description": "Check whether the bot is online.",
                "callback": "help_alive"
            },
            "whisper": {
                "aliases": ["w"],
                "usage": "whisper @user <message> (inline)",
                "description": "Send a message only the intended recipient can read.",
                "callback": "help_whisper",
                "note": "Inline only — type it as @YourBot whisper @user <message>."
            },
            "q": {
                "aliases": ["quote"],
                "usage": "/q (reply)",
                "description": "Turn a message into a quote sticker (via Quotly).",
                "callback": "help_q",
                "note": "Must be used as a reply."
            },
            "start": {
                "aliases": [],
                "usage": "/start",
                "description": "Show the bot's intro message.",
                "callback": "help_start"
            },
        }
    },
    "🎮 Games": {
        "callback": "cat_games",
        "commands": {
            "rps": {
                "aliases": [],
                "usage": "rps (inline)",
                "description": "Play Rock-Paper-Scissors with your friends. (Computer mode comming soon)",
                "callback": "help_rps"
            },
            "xo": {
                "aliases": [],
                "usage": "xo (inline)",
                "description": "Play Tic-Tac-Toe with your friends. (Computer mode comming soon)",
                "callback": "help_xo"
            },
        }
    }
}
