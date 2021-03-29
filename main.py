import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='./env')
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('REMOVE_BG_API_KEY')

