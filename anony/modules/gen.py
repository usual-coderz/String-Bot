import asyncio
from pyrogram import Client, errors, filters, types, enums, StopPropagation
from telethon import errors as telerror, TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from config import SUPPORT_CHAT, API_ID, API_HASH
from anony import app, buttons


async def listen(cq: types.CallbackQuery, text: str, timeout: int = 120) -> str:
    """Waits for user input with a timeout."""
    try:
        await cq.message.reply_text(text)
        message = await app.listen.Message(
            filters.text, id=filters.user(cq.from_user.id), timeout=timeout
        )
        return message.text
    except asyncio.TimeoutError:
        await cq.message.reply_text(
            "Timed out.\n\nPlease try again.", reply_markup=buttons.retry_key()
        )
        raise StopPropagation


@app.on_callback_query(filters.regex("generate"))
async def _generate(_, cq: types.CallbackQuery):
    await cq.answer()
    await cq.message.reply_text(
        "Please choose which session you want to generate:",
        reply_markup=buttons.gen_key()
    )


@app.on_callback_query(filters.regex(r"(pyrogram|telethon)"))
async def _gen_session(_, cq: types.CallbackQuery):
    sgen = cq.data
    pyrogram_mode = sgen == "pyrogram"
    await cq.answer()

    # Single prompt with /skip info
    api_id_text = await listen(
        cq,
        f"Starting {sgen} session generator...\n\n"
"Please enter your <b>API ID</b> or /skip:"
    )

    if api_id_text.strip() == "/skip":
        api_id = API_ID
        api_hash = API_HASH
    else:
        try:
            api_id = int(api_id_text)
        except ValueError:
            return await cq.message.reply_text(
                "The API ID you sent is invalid.\nPlease start again.",
                reply_markup=buttons.retry_key()
            )
        api_hash_text = await listen(cq, "Please enter your <b>API HASH</b>:")
        if len(api_hash_text) < 30:
            return await cq.message.reply_text(
                "The API HASH you sent is invalid.\nPlease start again.",
                reply_markup=buttons.retry_key()
            )
        api_hash = api_hash_text

    # Ask for phone number
    phone_number = await listen(cq, "Please enter your <b>phone number</b> to proceed:")
    await cq.message.reply_text("Trying to send OTP to the given number...")

    # Initialize client
    client = (
        Client(name="Anony", api_id=api_id, api_hash=api_hash, in_memory=True)
        if pyrogram_mode
        else TelegramClient(StringSession(), api_id, api_hash)
    )
    await client.connect()

    # Send OTP
    try:
        code = (
            await client.send_code(phone_number)
            if pyrogram_mode
            else await client.send_code_request(phone_number)
        )
        await asyncio.sleep(1)
    except errors.FloodWait as f:
        return await cq.message.reply_text(
            f"Failed to send code. Wait {f.value} seconds.", reply_markup=buttons.retry_key()
        )
    except (errors.ApiIdInvalid, telerror.ApiIdInvalidError):
        return await cq.message.reply_text(
            "API ID or API HASH invalid.\nPlease start again.", reply_markup=buttons.retry_key()
        )
    except (errors.PhoneNumberInvalid, telerror.PhoneNumberInvalidError):
        return await cq.message.reply_text(
            "Phone number invalid.\nPlease start again.", reply_markup=buttons.retry_key()
        )
    except Exception as ex:
        return await cq.message.reply_text(f"Error: <code>{str(ex)}</code>")

    # Ask for OTP
    otp = await listen(
        cq,
        f"Enter the OTP sent to {phone_number}.\n"
        "If OTP is <code>12345</code>, send it as <code>1 2 3 4 5</code>",
        timeout=600
    )
    otp = otp.replace(" ", "")

    # Sign in
    try:
        if pyrogram_mode:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
        else:
            await client.sign_in(phone_number, otp)
    except (errors.PhoneCodeInvalid, telerror.PhoneCodeInvalidError):
        return await cq.message.reply_text(
            "OTP is wrong.\nPlease start again.", reply_markup=buttons.retry_key()
        )
    except (errors.PhoneCodeExpired, telerror.PhoneCodeExpiredError):
        return await cq.message.reply_text(
            "OTP expired.\nPlease start again.", reply_markup=buttons.retry_key()
        )
    except (errors.SessionPasswordNeeded, telerror.SessionPasswordNeededError):
        pwd = await listen(cq, "Enter your two-step verification password:")
        try:
            if pyrogram_mode:
                await client.check_password(password=pwd)
            else:
                await client.sign_in(password=pwd)
        except (errors.PasswordHashInvalid, telerror.PasswordHashInvalidError):
            return await cq.message.reply_text(
                "Password wrong.\nPlease start again.", reply_markup=buttons.retry_key()
            )
    except Exception as ex:
        return await cq.message.reply_text(f"Error: <code>{str(ex)}</code>")

    # Export session string
    try:
        txt = (
            "Here is your {0} session\n\n<code>{1}</code>\n\n"
            "A session generator bot by <a href={2}>Veron Updates</a>\n"
            "☠ <b>Note:</b> Don't share the session with anyone."
        )

        if pyrogram_mode:
            string_session = await client.export_session_string()
            # ✅ FIX: Use enums.ParseMode.HTML instead of string "html"
            await client.send_message(
                "me",
                txt.format(sgen, string_session, SUPPORT_CHAT),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            string_session = client.session.save()
            await client.send_message(
                "me",
                txt.format(sgen, string_session, SUPPORT_CHAT),
                link_preview=False,
                parse_mode="html"
            )

        # Join channel
        try:
            if pyrogram_mode:
                await client.join_chat("NexaCoders")
            else:
                await client(JoinChannelRequest("@NexaCoders"))
        except:
            pass

    except Exception as ex:
        await cq.message.reply_text(f"⚠️ Failed to export session: <code>{str(ex)}</code>")

    # Disconnect and notify user
    try:
        await client.disconnect()
        await cq.message.reply_text(
            f"✅ Successfully generated your {sgen} string session.\n\n"
            "Check your Saved Messages to get it.\n\n"
            f"A string generator bot by <a href={SUPPORT_CHAT}>Veron Updates</a>.",
            reply_markup=buttons.pm_key(cq.from_user.id),
            parse_mode=enums.ParseMode.HTML
        )
    except:
        pass