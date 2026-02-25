import logging
from pyrogram import Client, enums, types
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
logging.getLogger("telethon").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# --------------------------
# Custom Pyro Client
# --------------------------
class Pyro(Client):
    def __init__(self):
        super().__init__(
            name="StringSession",
            api_id=config.API_ID,               # Use your config API_ID
            api_hash=config.API_HASH,           # Use your config API_HASH
            bot_token=config.BOT_TOKEN,         # Bot token from config
            lang_code="en",
            parse_mode=enums.ParseMode.HTML,    # ✅ Pyrogram v2.x
            link_preview_options=types.LinkPreviewOptions(is_disabled=True)
        )
        self.OWNER = config.OWNER_ID
        self.id = None
        self.name = None
        self.username = None
        self.mention = None

    async def _start(self):
        """Start the bot and initialize user info."""
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