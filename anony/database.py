# anony/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# ===============================
# MONGODB CONNECTION
# ===============================
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["AnonyBot"]

# Collections
users_col = db.users
forcejoin_col = db.forcejoin


# =====================================================
# FORCE JOIN SYSTEM
# =====================================================

# Get all force join channels
async def get_forcejoin_channels():
    data = await forcejoin_col.find_one({"_id": "forcejoin"})

    if not data:
        return []

    return data.get("channels", [])


# Add channel to forcejoin
async def add_forcejoin_channel(channel: str):
    data = await forcejoin_col.find_one({"_id": "forcejoin"})

    if not data:
        await forcejoin_col.insert_one({
            "_id": "forcejoin",
            "channels": [channel]
        })
        return True

    if channel in data.get("channels", []):
        return False

    await forcejoin_col.update_one(
        {"_id": "forcejoin"},
        {"$push": {"channels": channel}}
    )
    return True


# Remove channel from forcejoin
async def remove_forcejoin_channel(channel: str):
    await forcejoin_col.update_one(
        {"_id": "forcejoin"},
        {"$pull": {"channels": channel}}
    )
    return True


# =====================================================
# USER SYSTEM (Optional but useful)
# =====================================================

async def add_user(user_id: int):
    user = await users_col.find_one({"_id": user_id})

    if not user:
        await users_col.insert_one({"_id": user_id})


async def get_users():
    users = []
    async for user in users_col.find():
        users.append(user["_id"])
    return users