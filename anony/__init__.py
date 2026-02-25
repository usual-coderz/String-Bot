import logging
import pyrogram
from pyrogram import Client
import config

# --------------------------
# Logging setup
# --------------------------
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# --------------------------
# Version & feature checks
# --------------------------
PYRO_VERSION = tuple(map(int, pyrogram.__version__.split(".")))
logger.info(f"Pyrogram version: {pyrogram.__version__}")

# ParseMode fallback
try:
    from pyrogram import enums
    PARSE_MODE = enums.ParseMode.HTML
except (ImportError, AttributeError):
    PARSE_MODE = "html"

# LinkPreviewOptions fallback
try:
    from pyrogram import types
    LINK_PREVIEW = types.LinkPreviewOptions(is_disabled=True)
except (ImportError, AttributeError):
    LINK_PREVIEW = None

# --------------------------
# Custom Pyro Client
# --------------------------
class Pyro(Client):
    def __init__(self):
        kwargs = {
            "name": "StringSession",
            "api_id": config.API_ID,
            "api_hash": config.API_HASH,
            "bot_token": config.BOT_TOKEN,
            "lang_code": "en",
            "parse_mode": PARSE_MODE,
        }
        if LINK_PREVIEW:
            kwargs["link_preview_options"] = LINK_PREVIEW

        super().__init__(**kwargs)

        self.OWNER = config.OWNER_ID
        self.id = None
        self.name = None
        self.username = None
        self.mention = None

    async def _start(self):
        """Start the bot and initialize info."""
        await super().start()
        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name
        self.username = me.username
        self.mention = me.mention
        logger.info(f"@{self.username} started.")

    async def _stop(self):
        """Stop the bot gracefully."""
        await super().stop()
        logger.info("Bot stopped.")

# --------------------------
# Instantiate bot
# --------------------------
app = Pyro()

# --------------------------
# Initialize other modules
# --------------------------
from convopyro import Conversation
Conversation(app)

from anony.database import Database
db = Database()

from anony.utils import Inline
buttons = Inline()