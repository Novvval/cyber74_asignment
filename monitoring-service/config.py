import os


class Config:
    BROWSER_BIN = os.getenv('BROWSER_BIN', '/usr/bin/google-chrome-stable')
    BROKER_URL = os.getenv('BROKER_URL', 'redis://redis:6379')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379')
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')
    API_URL =  os.getenv('API_URL', 'http://api:8000')
