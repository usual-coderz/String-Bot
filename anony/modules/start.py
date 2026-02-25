from pyrogram import filters, types
from anony.must_join import must_join
from anony import app, buttons, db


@app.on_message(filters.command("start") & filters.private)
async def f_start(_, m):

    joined = await must_join(app, m.from_user.id)

    if joined != True:
        await m.reply_text(
            "⚡ Join required channels to continue.",
            reply_markup=joined
        )
        return

    await m.reply_text(
    f"""
✨ <b>Wᴇʟᴄᴏᴍᴇ {m.from_user.mention} !</b>

ɪ'ᴍ <b>{app.mention}</b> ⚡

🔐 A Pᴏᴡᴇʀғᴜʟ <b>Tᴇʟᴇɢʀᴀᴍ Sᴛʀɪɴɢ Sᴇssɪᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ</b>
Bᴜɪʟᴛ Tᴏ Cʀᴇᴀᴛᴇ Sᴇᴄᴜʀᴇ Pʏʀᴏɢʀᴀᴍ & Tᴇʟᴇᴛʜᴏɴ Sᴇssɪᴏɴs Eᴀsɪʟʏ.

━━━━━━━━━━━━━━━━━━
⚙️ <b>Fᴇᴀᴛᴜʀᴇs</b>
• Gᴇɴᴇʀᴀᴛᴇ Sᴇssɪᴏɴ Sᴀғᴇʟʏ
• Fᴀsᴛ Lᴏɢɪɴ Sʏsᴛᴇᴍ
• Oᴛᴘ Pʀᴏᴛᴇᴄᴛɪᴏɴ
• Pʀɪᴠᴀᴛᴇ & Sᴇᴄᴜʀᴇ
━━━━━━━━━━━━━━━━━━

🚀 Cʟɪᴄᴋ <b>Gᴇɴᴇʀᴀᴛᴇ</b> Bᴇʟᴏᴡ Tᴏ Sᴛᴀʀᴛ Cʀᴇᴀᴛɪɴɢ Yᴏᴜʀ Sᴇssɪᴏɴ.
""",
    reply_markup=buttons.start_key(),
    parse_mode="html",
    disable_web_page_preview=True
)

    await db.add_user(m.from_user.id)

@app.on_callback_query(filters.regex("check_join"))
async def check_join_cb(client, cb):

    joined = await must_join(client, cb.from_user.id)

    if joined != True:
        await cb.answer(
            "Join all channels first!",
            show_alert=True
        )
        return

    await cb.message.edit_text(
        "✅ Verification Successful!\nSend /start again."
    )
