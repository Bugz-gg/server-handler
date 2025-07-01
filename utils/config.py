import os
from dotenv import load_dotenv

load_dotenv(".python_env")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

ADMIN_USERS = []
if os.getenv("ADMIN_USERS"):
    ADMIN_USERS = [user_id.strip() for user_id in os.getenv("ADMIN_USERS").split(",")]

YES = os.getenv("YES")
PICTURES = os.getenv("PICTURES").split("|")
