from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_URL = getenv("MONGO_URL")
OWNER_ID = int(getenv("OWNER_ID", 1356469075))
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/VeronMeetup")

# Add these lines
API_ID = int(getenv("API_ID", 0))           # Telegram API ID
API_HASH = getenv("API_HASH", "")          # Telegram API Hash