from pyrogram import types, __version__ as pv
from telethon import __version__ as tv

from config import SUPPORT_CHAT

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def gen_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=f"Pʏʀᴏɢʀᴀᴍ", callback_data="pyrogram"),
                    self.ikb(text=f"Tᴇʟᴇᴛʜᴏɴ", callback_data="telethon"),
                ]
            ]
        )

    def pm_key(self, user_id: int) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs",
                        url=f"tg://openmessage?user_id={user_id}",
                    )
                ]
            ]
        )

    def retry_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[self.ikb(text="Tʀʏ Aɢᴀɪɴ", callback_data="generate")]]
        )

    def start_key(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [self.ikb(text="Gᴇɴᴇʀᴀᴛᴇ Sᴇssɪᴏɴ Sᴛʀɪɴɢ", callback_data="generate")],
                [
                    self.ikb(text="Sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
                    self.ikb(text="Cʜᴀɴɴᴇʟ", url="https://t.me/VeronUpdates"),
                ],
            ]
        )
