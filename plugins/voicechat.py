
from pyrogram import filters
from pyrogram.enums import ChatType
from strings import get_string
from SungJinwoo import app
from SungJinwoo.utils import ANNIEbin

from SungJinwoo.utils.database import get_assistant, get_lang
import asyncio
from os import getenv
from dotenv import load_dotenv
from pyrogram import Client
from dotenv import load_dotenv
import config

from SungJinwoo.logging import LOGGER
from SungJinwoo.utils.database import (
    delete_filter,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
    set_loop,
)
from SungJinwoo.core.call import ANNIE
"""
from pyrogram import filters
from SungJinwoo import app
from SungJinwoo.utils.database import get_assistant
import asyncio

async def continuous_check():
    monitored_chat_id = config.LOG  # Replace with your target group chat ID
    prev_members = set()

    while True:
        userbot = await get_assistant(config.LOG)
        current_members = set()

        async for m in userbot.get_call_members(monitored_chat_id):
            if not m.is_left:
                current_members.add(m.user.id)

        new_joiners = current_members - prev_members
        leavers = prev_members - current_members

        for user_id in new_joiners:
            user = await app.get_users(user_id)
            await app.send_message(monitored_chat_id, f"{user.mention} has joined the voice chat.")

        for user_id in leavers:
            user = await app.get_users(user_id)
            await app.send_message(monitored_chat_id, f"{user.mention} has left the voice chat.")

        prev_members = current_members
        await asyncio.sleep(1)

asyncio.create_task(continuous_check())


"""









@app.on_message(
    filters.command(["vcuser", "vcusers", "vcmember", "vcmembers"])
)
async def vc_members(client, message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    msg = await message.reply_text(_["V_C_1"])
    userbot = await get_assistant(message.chat.id)
    TEXT = ""
    try:
        async for m in userbot.get_call_members(message.chat.id):
            chat_id = m.chat.id
            username = m.chat.username
            is_hand_raised = m.is_hand_raised
            is_video_enabled = m.is_video_enabled
            is_left = m.is_left
            is_screen_sharing_enabled = m.is_screen_sharing_enabled
            is_muted = bool(m.is_muted and not m.can_self_unmute)
            is_speaking = not m.is_muted

            if m.chat.type != ChatType.PRIVATE:
                title = m.chat.title
            else:
                try:
                    title = (await client.get_users(chat_id)).mention
                except:
                    title = m.chat.first_name

            TEXT += _["V_C_2"].format(
                title,
                chat_id,
                username,
                is_video_enabled,
                is_screen_sharing_enabled,
                is_hand_raised,
                is_muted,
                is_speaking,
                is_left,
            )
            TEXT += "\n\n"
        if len(TEXT) < 4000:
            await msg.edit(TEXT or _["V_C_3"])
        else:
            link = await ANNIEbin(TEXT)
            await msg.edit(
                _["V_C_4"].format(link),
                disable_web_page_preview=True,
            )
    except ValueError as e:
        await msg.edit(_["V_C_5"])
        
from pyrogram import *
from pyrogram import filters
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from SungJinwoo import app



@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    text = f"➻ {message.from_user.mention}\n\n**๏ ɪɴᴠɪᴛɪɴɢ ɪɴ ᴠᴄ ᴛᴏ :**\n\n**➻ **"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"
        userbot = await get_assistant(message.chat.id)
        await message.reply(reply_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="๏ ᴊᴏɪɴ ᴠᴄ ๏", url=add_link)]]))
        
    except Exception as e:
        print(f"Error: {e}")




@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            prev_and_next_btns = [
                Button.inline("▶️Next▶️", data=f"next {start+10} {event.text.split()[1]}")
            ]
            await msg.edit(result, link_preview=False, buttons=prev_and_next_btns)
            await session.close()



