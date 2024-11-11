import os
import logging
from dotenv import load_dotenv
from pyrogram import Client
from run import bot 
load_dotenv()

# Set up logging to track potential issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bot = Client(
    "Channel Message Editor Bot",
    bot_token=os.environ.get("BOT_TOKEN", "6240482331:AAHEnRNj-XmNOIXSgOeZc8i1cbqiyTB1AkE"),
    api_id=int(os.environ.get("API_ID", "28374181")),
    api_hash=os.environ.get("API_HASH", "00b7ca7f535e816590db39e76f85d0c7")
)

if __name__ == "__main__":
    try:
        logger.info("Bot is starting...")
        Bot.run()
        logger.info("Bot is running...")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
      
