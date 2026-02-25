from pyrogram import filters
from pyrogram.enums import ParseMode
from anony.must_join import must_join
from anony import app, buttons, db


# ==========================================
# START COMMAND
# ==========================================
@app.on_message(filters.command("start") & filters.private)
async def f_start(_, message):

    user_id = message.from_user.id

    joined = await must_join(app, user_id)

    if joined is not True:
        await message.reply_text(
            "⚡ Join required channels to continue.",
            reply_markup=joined
        )
        return

    text = f"""
✨ <b>Wᴇʟᴄᴏᴍᴇ {message.from_user.mention} !</b>

ɪ'ᴍ <b>{app.mention}</b> ⚡

🔐 A Pᴏᴡᴇʀғᴜʟ <b>Tᴇʟᴇɢʀᴀᴍ Sᴛʀɪɴɢ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ</b>
Bᴜɪʟᴛ Tᴏ Cʀᴇᴀᴛᴇ Sᴇᴄᴜʀᴇ Pʏʀᴏɢʀᴀᴍ & Tᴇʟᴇᴛʜᴏɴ Sᴇssɪᴏɴs Eᴀsɪʟʏ.

━━━━━━━━━━━━━━━━━━
<b>⚙️ Fᴇᴀᴛᴜʀᴇs</b>
• Gᴇɴᴇʀᴀᴛᴇ Sᴇssɪᴏɴ Sᴀғᴇʟʏ
• Fᴀsᴛ Lᴏɢɪɴ Sʏsᴛᴇᴍ
• Oᴛᴘ Pʀᴏᴛᴇᴄᴛɪᴏɴ
• Pʀɪᴠᴀᴛᴇ & Sᴇᴄᴜʀᴇ
━━━━━━━━━━━━━━━━━━

🚀 Cʟɪᴄᴋ <b>Gᴇɴᴇʀᴀᴛᴇ</b> Bᴇʟᴏᴡ Tᴏ Sᴛᴀʀᴛ Cʀᴇᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ.
"""

    await message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=buttons.start_key(),
        disable_web_page_preview=True
    )

    await db.add_user(user_id)


# ==========================================
# FORCE JOIN CHECK
# ==========================================
@app.on_callback_query(filters.regex("check_join"))
async def check_join_cb(client, callback):

    joined = await must_join(client, callback.from_user.id)

    if joined is not True:
        await callback.answer(
            "Join all channels first!",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "✅ <b>Verification Successful!</b>\nSend /start again.",
        parse_mode=ParseMode.HTML
    )