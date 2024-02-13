import unicodedata
import re
from pyrogram import Client, filters
from config import

# Initialize Pyrogram client
app = Client("zoney", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load blacklist from file
def load_blacklist():
    with open("blacklist.txt", "r") as file:
        return [normalize_text(line.strip()) for line in file]

# Normalize text for comparison
def normalize_text(text):
    return unicodedata.normalize('NFKD', text)

# Check if text contains blacklisted word
def contains_blacklisted_word(text, blacklist):
    return any(word.lower() in text.lower() for word in blacklist)

# Check if text has special font
def has_special_font(text):
    # Define your font library here or import it from another module
    font_library = {...}
    for char in text:
        for font_style in font_library.values():
            if char in font_style:
                return True
    return False

# Delete mode (True by default)
delete_mode = True

# Load blacklist
blacklist = load_blacklist()

# Message handler for deleting blacklisted messages
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

# Message handler for deleting edited messages
@app.on_edited_message(filters.all)
async def delete_edited(_, message):
    await message.delete()

# Start the Pyrogram client
print("Bot started")
app.run()
