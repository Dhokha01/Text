import unicodedata
import re
from pyrogram import Client, filters
from font import font_library
from config import API_ID, API_HASH, BOT_TOKEN, BLACKLIST_FILE, OWNER_ID

app = Client(
    "zoney",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def get_admins(chat_id: int):
    return [
        member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

def load_blacklist():
    with open("blacklist.txt", "r") as file:
        return [normalize_text(line.strip()) for line in file]

def contains_blacklisted_word(text, blacklist):
    return any(word.lower() in text.lower() for word in blacklist)

def normalize_text(text):
    return unicodedata.normalize('NFKD', text)

def has_special_font(text):
    for char in text:
        for font_style in font_library.values():
            if char in font_style:
                return True
    return False

blacklist = load_blacklist()
delete_mode = True

@app.on_message(filters.group)
async def delete_blacklisted_messages(client, message):
    try:
        if message.text:
            normalized_text = normalize_text(message.text)
            if contains_blacklisted_word(normalized_text, blacklist) and delete_mode:
                await message.delete()
            elif has_special_font(normalized_text) and delete_mode:
                await message.delete()
        elif message.caption:
            normalized_caption = normalize_text(message.caption)
            if contains_blacklisted_word(normalized_caption, blacklist) and delete_mode:
                await message.delete()
            elif has_special_font(normalized_caption) and delete_mode:
                await message.delete()
    except Exception as e:
        print(f"Error processing message: {e}")

print("Bot started")
app.run()

from telegram.ext import Updater, CommandHandler
from telegram import Update
from threading import Timer

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = 'YOUR_TOKEN'

def delete_message(context: CallbackContext, update: Updates, message_id: int):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)

def edit_and_delete(update: Update, context: CallbackContext):
    message = update.message.reply_text("This message will be deleted in 5 seconds.")
    # Edit the message after 2 seconds
    Timer(2, message.edit_text, args=("This message has been edited.",)).start()
    # Delete the message after 5 seconds
    Timer(5, delete_message, args=(context, update, message.message_id)).start()

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the command handler
    dispatcher.add_handler(CommandHandler("edit_and_delete", edit_and_delete))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
