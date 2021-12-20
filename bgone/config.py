import os
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEYS = os.getenv('REMOVE_BG_API_KEY').split(', ')
MSG_HISTORY_LIMIT = 10
