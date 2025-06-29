import os
from dotenv import load_dotenv

load_dotenv(".python_env")

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

ADMIN_USERS = []
if os.getenv("ADMIN_USERS"):
    ADMIN_USERS = [
        user_id.strip() for user_id in os.getenv("ADMIN_USERS").split(",")
    ]
