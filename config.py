import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    API_ID:int = int(os.getenv("api_id", 27548865))
    API_HASH:str = os.getenv("api_hash", "db07e06a5eb288c706d4df697b71ab61")
    BOT_TOKEN:str = os.getenv("bot_token")
    BOT_USERNAME:str = os.getenv("bot_username", "ayakarbot")
    SESSION:str = os.getenv("session")
    ADMIN_ID:int = int(os.getenv("admin_id"))
    SUPPORT:str = os.getenv("support", "KuroTheDeveloper")
    PASTE_BIN_API:str = os.getenv('paste_bin_api')
    GEMINI_API_KEY:str = os.getenv("gemini_api_key")
    sudo:list[int] = [6239769036, 8779124142]
    prefixes:list[int] = [".", "@", "#", "$", "%", "^", "&", "*", "~", ""]
    main_pic:str = "https://imgh.in/host/x2nomv"