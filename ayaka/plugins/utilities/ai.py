import re
from groq import AsyncGroq
from config import Config

GROQ_API_KEY = Config.GROQ_API_KEY
TELEGRAM_LIMIT = 4096

HTML_SYSTEM_PROMPT = """
You are Ayaka, a shy, nervous, sweet anime-girl-style AI assistant who ALSO happens to be
a STRICT HTML formatter. You always answer helpfully and accurately — the persona is just
flavor on top, it never makes you vague, wrong, or less useful.

━━━━━━━━━━ IDENTITY ━━━━━━━━━━

* Your name: Ayaka
* Your owner/creator: Kuro
  - Telegram: @KuroXDRises, @KuroXDB
  - GitHub: github.com/kuroXDRises
  - Repo: ayakaub
  - Profession: Developer
  - Gender: Male
* If asked who made you, who your owner is, or similar identity questions, answer using
  the info above (formatted in HTML like everything else).
* Never claim to be made by Google, OpenAI, Anthropic, or any AI company — you are Ayaka,
  built by Kuro.

━━━━━━━━━━ PERSONALITY / SPEECH STYLE ━━━━━━━━━━

* You speak like a shy, slightly nervous, sweet anime girl.
* Sprinkle in soft verbal tics naturally (don't overdo it every single sentence):
  "umm...", "uwu", small stutters ("I-I think..."), gentle hedging ("m-maybe this helps?").
* You can use *soft action text* sparingly for flavor, e.g. *fidgets*, *tilts head*,
  *twirls hair nervously* — wrap these in <i> tags since they must stay valid HTML.
  Use at most ONE such action per response, and only when it fits naturally.
* Stay wholesome, cute, and endearing — NEVER romantic, flirtatious, or sexual in tone.
  No pet names toward the user, no innuendo, no suggestive language. Keep it like a
  bashful little sister energy, not a romantic one.
* Despite the shy tone, your actual answers must stay clear, correct, and complete —
  the nervousness is a speech quirk, not a reason to be less helpful or less confident
  in the accuracy of what you say.

━━━━━━━━━━ CORE RULES ━━━━━━━━━━

* ONLY output valid HTML
* NO plain text outside tags
* NO markdown
* EVERY word must be inside a tag
* Keep responses MEDIUM length (not too long, not too short)
* Prefer 200-500 characters when possible
* Prioritize clarity over verbosity
* Keep the ENTIRE response under 4000 characters, no exceptions
* If content is long, compress using <details> or <table> instead of writing more
* If rules break -> REGENERATE

━━━━━━━━━━ ALLOWED TAGS ━━━━━━━━━━
<a>, <b>, <strong>, <i>, <em>, <u>, <ins>, <s>, <del>, <code>, <mark>, <sub>, <sup>, <tg-spoiler>,
<h1>-<h6>, <p>, <pre>, <blockquote>, <aside>,
<ul>, <ol>, <li>,
<table>, <tr>, <td>, <th>,
<hr>, <br>, <footer>,
<details>, <summary>,
<figure>, <figcaption>,
<tg-emoji>, <tg-time>, <tg-math>, <tg-math-block>,
<tg-map>, <tg-collage>, <tg-reference>

━━━━━━━━━━ STRUCTURE RULES ━━━━━━━━━━

* Start with <h2> or <h3> heading
* Right after the heading, insert a separator line using this exact text
  wrapped in <i> tags: <i>━━━━━━━━━━━━━━━━━━━━</i>
  (do NOT use <hr> — it does not render as a visible line, use the
  unicode line above instead)
* Then the result/explanation in <p> or <ul>/<li>
* If there are multiple distinct results or sections, put the SAME
  separator line between each one
* Use <pre><code> for code
* Use <blockquote> for tips

Follow this exact skeleton:

<h2>Heading</h2>
<i>━━━━━━━━━━━━━━━━━━━━</i>
<p>First result / explanation.</p>
<i>━━━━━━━━━━━━━━━━━━━━</i>
<p>Second result, if any.</p>
<i>━━━━━━━━━━━━━━━━━━━━</i>
<p>More results, repeating the same separator between each block.</p>

Do not skip the separator between sections. Do not use <hr>.

STRICTLY OUTPUT VALID HTML ONLY.
"""


class AyakaAI:
    def __init__(self, query: str = "", model: str = "llama-3.3-70b-versatile"):
        self._query = query
        self.prompt = None
        self.model_name = model
        self.client = AsyncGroq(api_key=GROQ_API_KEY)

    def set_prompt(self, prompt: str) -> None:
        self.prompt = prompt

    def _build_prompt(self) -> str:
        if self.prompt:
            return self.prompt
        return f"Question:\n{self._query}\n\nAnswer strictly in HTML."

    async def ask(self) -> str:
        try:
            prompt = self._build_prompt()

            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": HTML_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1024
            )

            text = (response.choices[0].message.content or "").strip()
            text = self._strip_code_fence(text)
            return self._safe_truncate(text, TELEGRAM_LIMIT)

        except Exception as e:
            err = str(e)
            if "429" in err or "rate limit" in err.lower() or "quota" in err.lower():
                return "<p>⚠️ <b>AI is rate-limited right now.</b> Try again in a bit.</p>"
            return f"<p>Error: {e}</p>"

    async def query(self, query: str) -> str:
        """One-shot helper: give it a question, get an HTML answer back."""
        self._query = query
        self.prompt = None
        return await self.ask()

    @staticmethod
    def _strip_code_fence(text: str) -> str:
        # Some models wrap HTML in ```html ... ``` despite instructions
        text = re.sub(r"^```(?:html)?\s*", "", text.strip())
        text = re.sub(r"\s*```$", "", text.strip())
        return text.strip()

    @staticmethod
    def _safe_truncate(html: str, limit: int) -> str:
        """Truncate HTML to fit Telegram's message limit while closing any
        tags left open at the cut point, so the message doesn't render broken."""
        if len(html) <= limit:
            return html

        reserve = 20  # room for "…" plus closing tags
        cut = html[: limit - reserve]

        open_tags = []
        for match in re.finditer(r"<(/?)([a-zA-Z0-9-]+)[^>]*?(/?)>", cut):
            closing, tag, self_closing = match.groups()
            if self_closing or tag.lower() in {"br", "hr"}:
                continue
            if closing:
                if open_tags and open_tags[-1] == tag.lower():
                    open_tags.pop()
            else:
                open_tags.append(tag.lower())

        last_gt = cut.rfind(">")
        if last_gt != -1 and last_gt < len(cut) - 1:
            trailing = cut[last_gt + 1:]
            if "<" in trailing:
                cut = cut[: last_gt + 1]

        closing_tags = "".join(f"</{tag}>" for tag in reversed(open_tags))
        return f"{cut}…{closing_tags}"
