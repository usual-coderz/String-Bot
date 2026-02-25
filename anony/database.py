# anony/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL
from anony import logger


# =====================================
# DATABASE CLASS
# =====================================

class Database:

    def __init__(self):
        self.mongo = AsyncIOMotorClient(MONGO_URL)
        self.db = self.mongo["AnonyBot"]

        # collections
        self.users = self.db.users
        self.settings = self.db.settings

    async def connect(self):
        try:
            await self.mongo.admin.command("ping")
            logger.info("✅ MongoDB Connected Successfully")
        except Exception as e:
            raise SystemExit(f"MongoDB Connection Failed: {e}")

    async def close(self):
        self.mongo.close()
        logger.info("MongoDB connection closed")

    # ==========================
    # USER SYSTEM
    # ==========================

    async def is_user(self, user_id: int):
        return await self.users.find_one({"_id": user_id})

    async def add_user(self, user_id: int):
        if not await self.is_user(user_id):
            await self.users.insert_one({"_id": user_id})

    async def get_users(self):
        users = []
        async for user in self.users.find():
            users.append(user["_id"])
        return users


# Global DB Object
db = Database()


# =====================================
# FORCE JOIN SYSTEM
# =====================================

async def get_forcejoin_channels():
    data = await db.settings.find_one({"_id": "forcejoin"})

    if not data:
        return []

    return data.get("channels", [])


async def add_forcejoin_channel(channel: str):
    await db.settings.update_one(
        {"_id": "forcejoin"},
        {"$addToSet": {"channels": channel}},
        upsert=True
    )


async def remove_forcejoin_channel(channel: str):
    await db.settings.update_one(
        {"_id": "forcejoin"},
        {"$pull": {"channels": channel}}
    )