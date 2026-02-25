from pymongo import AsyncMongoClient

from anony import logger
from config import MONGO_URL


class Database:
    def __init__(self):

        self.mongo = AsyncMongoClient(MONGO_URL)

        # DATABASE
        self.db = self.mongo.StringGen

        # COLLECTIONS
        self.users = self.db.users
        self.settings = self.db.settings   # ✅ ADD THIS

    async def connect(self) -> None:
        try:
            await self.mongo.aconnect()
            await self.mongo.admin.command("ping")
            logger.info("Database connection completed.")
        except Exception as e:
            raise SystemExit(f"Database connection failed: {e}")

    async def close(self) -> None:
        await self.mongo.close()
        logger.info("Database connection closed.")

    # ================= USERS =================

    async def is_user(self, user_id: int):
        return await self.users.find_one({"user_id": user_id})

    async def add_user(self, user_id: int) -> None:
        if not await self.is_user(user_id):
            await self.users.insert_one({"user_id": user_id})

    async def get_users(self) -> list:
        return [doc["user_id"] async for doc in self.users.find()]

    # =====================================
    # FORCE JOIN DATABASE
    # =====================================

    async def get_forcejoin_channels(self):

        data = await self.settings.find_one(
            {"_id": "forcejoin"}
        )

        if not data:
            return []

        return data.get("links", [])

    async def add_forcejoin_channel(self, link: str):

        await self.settings.update_one(
            {"_id": "forcejoin"},
            {"$addToSet": {"links": link}},
            upsert=True
        )

    async def remove_forcejoin_channel(self, link: str):

        await self.settings.update_one(
            {"_id": "forcejoin"},
            {"$pull": {"links": link}}
        )