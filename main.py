import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load environment variables
load_dotenv()

# Set up logging to track potential issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot client
Bot = Client(
    "Channel Message Editor Bot",
    bot_token=os.environ.get("BOT_TOKEN", "6240482331:AAHEnRNj-XmNOIXSgOeZc8i1cbqiyTB1AkE"),
    api_id=int(os.environ.get("API_ID", "28374181")),
    api_hash=os.environ.get("API_HASH", "00b7ca7f535e816590db39e76f85d0c7")
)

# Authorized users
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "5715764478").split())

# Bot messages and buttons
START_TEXT = """Hello {},
I am a channel message editor bot.

Made by @FayasNoushad"""

HELP_TEXT = """**More Help**

- I am a channel message editor bot.
- I can edit and post messages in a channel.
- Use /post command with channel ID while replying to a message to post.
- Use /edit command with message link while replying to edit.

Made by @FayasNoushad"""

ABOUT_TEXT = """**About Me**

- **Bot:** `Channel Message Editor Bot`
- **Developer:** [Fayas](https://github.com/FayasNoushad)
- **Channel:** [Fayas Noushad](https://telegram.me/FayasNoushad)
- **Source:** [Click here](https://github.com/FayasNoushad/Channel-Message-Editor)
- **Language:** [Python3](https://python.org)
- **Library:** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Channel', url='https://telegram.me/FayasNoushad'),
            InlineKeyboardButton('Feedback', url='https://telegram.me/TheFayas')
        ],
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

logger.info("Bot is starting...")

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.from_user.id not in AUTH_USERS:
        return
    
    await update.answer("Processing")

    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
        logger.info("Sent home message")

    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
        logger.info("Sent help message")
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
        logger.info("Sent about message")
    
    else:
        await update.message.delete()

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if update.from_user.id not in AUTH_USERS:
        logger.info(f"Unauthorized user: {update.from_user.id}")
        return
    
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )
    logger.info("Sent start message")

@Bot.on_message(filters.private & filters.reply & filters.command(["post"]), group=1)
async def post(bot, update):
    if ((update.text == "post") or (" " not in update.text)) or (update.from_user.id not in AUTH_USERS):
        return
    
    if " " in update.text:
        chat_id = int(update.text.split()[1])
    
    try:
        user = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=update.from_user.id
        )
        if not user.can_post_messages:
            await update.reply_text("You can't do that")
            return
    except Exception as e:
        logger.error(f"Error getting chat member: {e}")
        return
    
    try:
        post = await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=update.reply_to_message.chat.id,
            message_id=update.reply_to_message.message_id,
            reply_markup=update.reply_to_message.reply_markup
        )
        post_link = f"https://telegram.me/c/{post.chat.id}/{post.message_id}"
        await update.reply_text(
            text="Posted Successfully",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Post", url=post_link)]]
            )
        )
        logger.info("Message posted successfully")
    except Exception as e:
        logger.error(f"Error posting message: {e}")
        await update.reply_text(str(e))

@Bot.on_message(filters.private & filters.reply & filters.command(["edit"]), group=2)
async def edit(bot, update):
    if (update.text == "/edit") or (update.from_user.id not in AUTH_USERS):
        return
    
    if " " in update.text:
        command, link = update.text.split(" ", 1)
    else:
        return
    
    if "/" in link:
        ids = link.split("/")
        chat_id = -100 + int(ids[-2])
        message_id = int(ids[-1])
    else:
        return
    
    try:
        user = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=update.from_user.id
        )
        if not user.can_be_edited:
            await update.reply_text("You can't do that, User needed can_be_edited permission.")
            return
    except Exception as e:
        logger.error(f"Error getting chat member: {e}")
        await update.reply_text(str(e))
        return
    
    if update.reply_to_message.text:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=update.reply_to_message.text,
                reply_markup=update.reply_to_message.reply_markup,
                disable_web_page_preview=True
            )
            logger.info("Message edited successfully")
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            await update.reply_text(str(e))
    else:
        await update.reply_text("I can edit text only")

# Run the bot
if __name__ == "__main__":
    try:
        logger.info("Running bot...")
        Bot.run()
    except Exception as e:
        logger.error(f"Error occurred: {e}")

