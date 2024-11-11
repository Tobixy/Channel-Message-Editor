import os
import logging
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

# Set up logging to track potential issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bot = Client(
    "Channel Message Editor Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

if __name__ == "__main__":
    try:
        logger.info("Bot is starting...")
        Bot.run()
        logger.info("Bot is running...")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
      
