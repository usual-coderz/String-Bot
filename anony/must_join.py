from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

from config import FORCE_JOIN
from anony.database import get_forcejoin_channels


# ===============================
# USERNAME EXTRACTOR
# ===============================
def extract_username(link):

    if "t.me/" in link and "+" not in link:
        return "@" + link.split("t.me/")[1]

    return None


# ===============================
# FORCE JOIN CHECK
# ===============================
async def must_join(client, user_id):

    db_links = await get_forcejoin_channels()

    all_links = list(set(FORCE_JOIN + db_links))

    if not all_links:
        return True

    not_joined = []

    for link in all_links:

        username = extract_username(link)

        if username:
            try:
                member = await client.get_chat_member(
                    username,
                    user_id
                )

                if member.status in ["left", "kicked"]:
                    raise UserNotParticipant

            except UserNotParticipant:
                not_joined.append(link)

        else:
            # private invite links
            not_joined.append(link)

    if not not_joined:
        return True

    # ===============================
    # 2 BUTTON ROW UI
    # ===============================
    buttons = []
    row = []

    for link in not_joined:

        name = link.split("/")[-1].replace("+", "")

        row.append(
            InlineKeyboardButton(
                name,
                url=link
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            "✅ Joined",
            callback_data="check_join"
        )
    ])

    return InlineKeyboardMarkup(buttons)