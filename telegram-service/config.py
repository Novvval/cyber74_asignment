import os

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'XXXXXXXXXXXXXXXXXXXXXXXX')
    API_URL = os.getenv('API_URL', 'http://api:8000')