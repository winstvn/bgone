import os
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.environ['DISCORD_TOKEN']
API_KEYS = os.environ['REMOVE_BG_API_KEY'].split(', ')
MSG_HISTORY_LIMIT = 10

API_URL = 'https://api.remove.bg/v1.0'
