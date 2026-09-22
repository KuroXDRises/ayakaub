import asyncio
import json
import os
import re
import base64
import random
from pyrogram import Client, filters, types
from groq import AsyncGroq

COUNTRIES = {
    "🇦🇫": "Afghanistan",
    "🇦🇱": "Albania",
    "🇩🇿": "Algeria",
    "🇦🇩": "Andorra",
    "🇦🇴": "Angola",
    "🇦🇬": "Antigua and Barbuda",
    "🇦🇷": "Argentina",
    "🇦🇲": "Armenia",
    "🇦🇺": "Australia",
    "🇦🇹": "Austria",
    "🇦🇿": "Azerbaijan",
    "🇧🇸": "Bahamas",
    "🇧🇭": "Bahrain",
    "🇧🇩": "Bangladesh",
    "🇧🇧": "Barbados",
    "🇧🇾": "Belarus",
    "🇧🇪": "Belgium",
    "🇧🇿": "Belize",
    "🇧🇯": "Benin",
    "🇧🇹": "Bhutan",
    "🇧🇴": "Bolivia",
    "🇧🇦": "Bosnia and Herzegovina",
    "🇧🇼": "Botswana",
    "🇧🇷": "Brazil",
    "🇧🇳": "Brunei",
    "🇧🇬": "Bulgaria",
    "🇧🇫": "Burkina Faso",
    "🇧🇮": "Burundi",
    "🇨🇻": "Cabo Verde",
    "🇰🇭": "Cambodia",
    "🇨🇲": "Cameroon",
    "🇨🇦": "Canada",
    "🇨🇫": "Central African Republic",
    "🇹🇩": "Chad",
    "🇨🇱": "Chile",
    "🇨🇳": "China",
    "🇨🇴": "Colombia",
    "🇰🇲": "Comoros",
    "🇨🇬": "Republic of the Congo",
    "🇨🇩": "Democratic Republic of the Congo",
    "🇨🇷": "Costa Rica",
    "🇨🇮": "Côte d'Ivoire",
    "🇭🇷": "Croatia",
    "🇨🇺": "Cuba",
    "🇨🇾": "Cyprus",
    "🇨🇿": "Czechia",
    "🇩🇰": "Denmark",
    "🇩🇯": "Djibouti",
    "🇩🇲": "Dominica",
    "🇩🇴": "Dominican Republic",
    "🇪🇨": "Ecuador",
    "🇪🇬": "Egypt",
    "🇸🇻": "El Salvador",
    "🇬🇶": "Equatorial Guinea",
    "🇪🇷": "Eritrea",
    "🇪🇪": "Estonia",
    "🇸🇿": "Eswatini",
    "🇪🇹": "Ethiopia",
    "🇫🇯": "Fiji",
    "🇫🇮": "Finland",
    "🇫🇷": "France",
    "🇬🇦": "Gabon",
    "🇬🇲": "Gambia",
    "🇬🇪": "Georgia",
    "🇩🇪": "Germany",
    "🇬🇭": "Ghana",
    "🇬🇷": "Greece",
    "🇬🇩": "Grenada",
    "🇬🇹": "Guatemala",
    "🇬🇳": "Guinea",
    "🇬🇼": "Guinea-Bissau",
    "🇬🇾": "Guyana",
    "🇭🇹": "Haiti",
    "🇭🇳": "Honduras",
    "🇭🇺": "Hungary",
    "🇮🇸": "Iceland",
    "🇮🇳": "India",
    "🇮🇩": "Indonesia",
    "🇮🇷": "Iran",
    "🇮🇶": "Iraq",
    "🇮🇪": "Ireland",
    "🇮🇱": "Israel",
    "🇮🇹": "Italy",
    "🇯🇲": "Jamaica",
    "🇯🇵": "Japan",
    "🇯🇴": "Jordan",
    "🇰🇿": "Kazakhstan",
    "🇰🇪": "Kenya",
    "🇰🇮": "Kiribati",
    "🇰🇼": "Kuwait",
    "🇰🇬": "Kyrgyzstan",
    "🇱🇦": "Laos",
    "🇱🇻": "Latvia",
    "🇱🇧": "Lebanon",
    "🇱🇸": "Lesotho",
    "🇱🇷": "Liberia",
    "🇱🇾": "Libya",
    "🇱🇮": "Liechtenstein",
    "🇱🇹": "Lithuania",
    "🇱🇺": "Luxembourg",
    "🇲🇬": "Madagascar",
    "🇲🇼": "Malawi",
    "🇲🇾": "Malaysia",
    "🇲🇻": "Maldives",
    "🇲🇱": "Mali",
    "🇲🇹": "Malta",
    "🇲🇭": "Marshall Islands",
    "🇲🇷": "Mauritania",
    "🇲🇺": "Mauritius",
    "🇲🇽": "Mexico",
    "🇫🇲": "Micronesia",
    "🇲🇩": "Moldova",
    "🇲🇨": "Monaco",
    "🇲🇳": "Mongolia",
    "🇲🇪": "Montenegro",
    "🇲🇦": "Morocco",
    "🇲🇿": "Mozambique",
    "🇲🇲": "Myanmar",
    "🇳🇦": "Namibia",
    "🇳🇷": "Nauru",
    "🇳🇵": "Nepal",
    "🇳🇱": "Netherlands",
    "🇳🇿": "New Zealand",
    "🇳🇮": "Nicaragua",
    "🇳🇪": "Niger",
    "🇳🇬": "Nigeria",
    "🇰🇵": "North Korea",
    "🇲🇰": "North Macedonia",
    "🇳🇴": "Norway",
    "🇴🇲": "Oman",
    "🇵🇰": "Pakistan",
    "🇵🇼": "Palau",
    "🇵🇸": "Palestine",
    "🇵🇦": "Panama",
    "🇵🇬": "Papua New Guinea",
    "🇵🇾": "Paraguay",
    "🇵🇪": "Peru",
    "🇵🇭": "Philippines",
    "🇵🇱": "Poland",
    "🇵🇹": "Portugal",
    "🇶🇦": "Qatar",
    "🇷🇴": "Romania",
    "🇷🇺": "Russia",
    "🇷🇼": "Rwanda",
    "🇰🇳": "Saint Kitts and Nevis",
    "🇱🇨": "Saint Lucia",
    "🇻🇨": "Saint Vincent and the Grenadines",
    "🇼🇸": "Samoa",
    "🇸🇲": "San Marino",
    "🇸🇹": "São Tomé and Príncipe",
    "🇸🇦": "Saudi Arabia",
    "🇸🇳": "Senegal",
    "🇷🇸": "Serbia",
    "🇸🇨": "Seychelles",
    "🇸🇱": "Sierra Leone",
    "🇸🇬": "Singapore",
    "🇸🇰": "Slovakia",
    "🇸🇮": "Slovenia",
    "🇸🇧": "Solomon Islands",
    "🇸🇴": "Somalia",
    "🇿🇦": "South Africa",
    "🇰🇷": "South Korea",
    "🇸🇸": "South Sudan",
    "🇪🇸": "Spain",
    "🇱🇰": "Sri Lanka",
    "🇸🇩": "Sudan",
    "🇸🇷": "Suriname",
    "🇸🇪": "Sweden",
    "🇨🇭": "Switzerland",
    "🇸🇾": "Syria",
    "🇹🇯": "Tajikistan",
    "🇹🇿": "Tanzania",
    "🇹🇭": "Thailand",
    "🇹🇱": "Timor-Leste",
    "🇹🇬": "Togo",
    "🇹🇴": "Tonga",
    "🇹🇹": "Trinidad and Tobago",
    "🇹🇳": "Tunisia",
    "🇹🇷": "Türkiye",
    "🇹🇲": "Turkmenistan",
    "🇹🇻": "Tuvalu",
    "🇺🇬": "Uganda",
    "🇺🇦": "Ukraine",
    "🇦🇪": "United Arab Emirates",
    "🇬🇧": "United Kingdom",
    "🇺🇸": "United States",
    "🇺🇾": "Uruguay",
    "🇺🇿": "Uzbekistan",
    "🇻🇺": "Vanuatu",
    "🇻🇦": "Vatican City",
    "🇻🇪": "Venezuela",
    "🇻🇳": "Vietnam",
    "🇾🇪": "Yemen",
    "🇿🇲": "Zambia",
    "🇿🇼": "Zimbabwe",
}

GROQ_API_KEY = "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"  # get one from https://console.groq.com/keys
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

DATA_FILE = os.path.join(os.path.dirname(__file__), "coins_data.json")


def load_coin_data() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"total": 0}


def save_coin_data():
    with open(DATA_FILE, "w") as f:
        json.dump(coin_data, f)


coin_data = load_coin_data()
session_coins = 0

COIN_RE = re.compile(r'(\d+(?:\.\d+)?)\s*coins?', re.IGNORECASE)


def get_country(text: str):
    FLAG_RE = re.compile(r'[\U0001F1E6-\U0001F1FF]{2}')
    match = FLAG_RE.search(text or "")
    if match:
        flag = match.group()
        return COUNTRIES.get(flag)
    return None


async def solve_captcha(image_bytes: bytes) -> str:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    completion = await groq_client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "This image contains a captcha code. Read it and reply with ONLY "
                            "the code, preserving the exact letter casing (uppercase/lowercase) "
                            "exactly as shown in the image. No explanation, no punctuation, "
                            "nothing else — just the code itself."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        temperature=0,
        max_completion_tokens=20,
    )
    return completion.choices[0].message.content.strip()


BOT_ID = 8790267038
ACTIVE: bool = False


@Client.on_message(filters.command("maze", prefixes=[""]) & filters.me, group=755)
async def maze_on_of(c: Client, m: types.Message):
    global ACTIVE
    if len(m.command) < 2:
        return await m.reply("maze on|off")
    if m.command[1] == "on":
        ACTIVE = True
        await m.reply("Maze Auto On")
    if m.command[1] == "off":
        ACTIVE = False
        await m.reply("Maze Auto Off")


@Client.on_message(filters.command("coins", prefixes=[""]) & filters.me, group=756)
async def coins_stat(c: Client, m: types.Message):
    await m.reply(
        f"🪙 **Coins**\n\nThis session: `{session_coins}`\nTotal (all-time): `{coin_data.get('total', 0)}`"
    )


RAIN_SOURCE_FILTER = (
    filters.user([BOT_ID, 8966963895, 8649620813])
    & filters.chat([8649620813, 8903449862, -1003929450754])
    & (filters.text | filters.photo)
)
async def _handle_rain_message(c: Client, m: types.Message):
    global session_coins

    if not ACTIVE:
        return

    text = m.text or m.caption or ""

    if text.startswith("🌧 RAIN!"):
        result = await m.click()
        await m.reply(random.choice(["HII", "HI", "yo", "Sup", "Let me grab this."]))

        alert_text = getattr(result, "message", None) or ""
        match = COIN_RE.search(alert_text)
        if match:
            amount = float(match.group(1))
            session_coins += amount
            coin_data["total"] = coin_data.get("total", 0) + amount
            save_coin_data()

    elif text.startswith("🎯 CLOSEST GUESS"):
        await asyncio.sleep(random.uniform(0.2, 0.6))
        await m.reply(f" {random.randint(10, 100)}")

    elif text.startswith("🏳 GUESS THE FLAG"):
        country = get_country(text)
        await asyncio.sleep(random.uniform(0.2, 0.6))
        await m.reply(str(country))

    elif m.photo and text.startswith("🏳 @uniquee_dev got the flag."):
        # treat this specific captioned photo from the bot as a captcha challenge
        photo_bytes = await c.download_media(m.photo.file_id, in_memory=True)
        code = await solve_captcha(photo_bytes.getvalue())
        await m.reply(code)


@Client.on_message(RAIN_SOURCE_FILTER, group=474)
async def rain_catch(c: Client, m: types.Message):
    await _handle_rain_message(c, m)


@Client.on_edited_message(RAIN_SOURCE_FILTER, group=474)
async def rain_catch_edited(c: Client, m: types.Message):
    # the bot often edits a "get ready" placeholder into the actual
    # "🌧 RAIN!" trigger instead of sending a brand-new message — catch that too
    await _handle_rain_message(c, m)
