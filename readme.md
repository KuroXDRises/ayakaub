# 🌸 Ayaka

A dual-client Telegram **userbot + bot** combo built on [Kurigram](https://docs.kurigram.icu) (Pyrogram fork), pairing a personal account (userbot) with a companion bot for inline features, AI, and group management.

---

## ✨ Features

### 🤖 AI Assistant
- **AyakaAI** — Gemini-powered (`gemini-2.0-flash`) assistant with a custom shy/nervous anime-girl persona
- Structured HTML output (heading + separator + result blocks) built for Telegram's rich formatting
- Auto-truncates to Telegram's message limit while keeping HTML tags valid
- Available via `/ai`, `/ask`, or inline (`@YourBot ai <question>`)

### 🛠 Developer Tools
- **Calculator** — inline arithmetic and symbolic equations: `@YourBot calc 2*(4+3)` or `@YourBot calc x^2-5*x+6=0`
- `/eval`, `/e` — Python eval with sandboxed output, execution timeout, and Pastebin fallback for long output
- `/sh` — Shell command execution, same timeout + Pastebin handling
- `/logs` — Fetch bot logs, with Clear/Refresh buttons
- `/type` — Animated "typing" text effect
- `/parse` — Send raw rich-text HTML as a formatted message (inline)

### 👥 Group Management
- `/ban`, `/dban`, `/unban` — ban / ban+delete / unban, by reply, username, or ID
- `/mute`, `/tmute`, `/unmute` — permanent or timed mute (`10m`, `2h`, `1d`)
- `/promote`, `/demote` — promote with a custom admin title, or demote
- `/delete`, `/purge` — message cleanup

### 🔒 Privacy & Utility
- **PM Permit** — `/pmpermit on|off`, `/approve_pm`, `/disapprove_pm`, `/pmstatus` for controlling who can DM you
- **AFK** — `/afk [reason]`, `/unafk` with one-reply-per-user auto-notify (text or media)
- **Block/Unblock** — `/block`, `/unblock`, works in groups (reply) or DMs
- **Whisper** — send a message only its intended recipient can read, inline
- **Quote** — turn a message into a sticker via Quotly integration

### 💬 Misc
- `/alive`, `/ping` — status checks
- `/start` — bot introduction, inline mode too

---

## 🧱 Tech Stack

- **[Kurigram](https://github.com/KurimuzonAkuma/kurigram)** — Pyrogram fork, MTProto client
- **tgcrypto** — fast crypto for Pyrogram
- **uvloop** — faster asyncio event loop
- **aiohttp** — async HTTP (Pastebin uploads, etc.)
- **python-dotenv** — `.env` config loading
- **google-genai** — AI inference (Gemini 2.0 Flash)

---

## ⚙️ Setup

### 1. Clone
```bash
git clone https://github.com/KuroXDRises/ayakaub
cd ayakaub
```

### 2. Install dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

### 3. Configure environment
Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
api_id=your_api_id            # optional
api_hash=your_api_hash        # optional
bot_token=your_bot_token
bot_username=your_bot_username # optional
session=your_session_string
admin_id=your_telegram_account_id
paste_bin_api=your_paste_bin_account_api
gemini_api_key=your_gemini_api_key
```

> Generate `session` with a Pyrogram session-string generator using the same `api_id`/`api_hash` you configure — mismatched pairs will fail to authenticate.
> Get a free Gemini key at [AIStudio](https://aistudio.google.com/app/api-keys?) — no billing required.

### 4. Run
```bash
python -m ayaka
```

---

## 🏗 Architecture

Ayaka runs **two Pyrogram clients** in the same process:

- **`bot`** (`bot_token`) — handles inline queries and public-facing features (`ayaka/plugins/bot/`)
- **`userbot`** (`session`) — handles admin commands run from your own account (`ayaka/plugins/user/`)

Commands that need to show up "via @YourBot" with buttons (like `/eval`, `/sh`, `/logs`) run on the userbot client, then relay through `get_inline_bot_results` / `send_inline_bot_result` to post the result using the bot's identity.

---

## 👤 Credits

- **Owner:** Kuro — [@KuroXDRises](https://t.me/KuroXDRises) · [@KuroXDB](https://t.me/KuroXDB)
- **GitHub:** [github.com/KuroXDRises](https://github.com/KuroXDRises)
- **Repo:** [ayakaub](https://github.com/KuroXDRises/ayakaub)

---

## 📄 License

This project is provided as-is. Check the repository for license details.
