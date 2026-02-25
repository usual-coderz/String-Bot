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
        f"Hey {m.from_user.first_name},\n\n"
        f"This is {app.mention},\n"
        "An open source session generator bot.",
        reply_markup=buttons.start_key()
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
