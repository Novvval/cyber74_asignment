import os


class Config:
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    PG_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    ENGINE_KWARGS = {
        'echo': False,
        'isolation_level': 'REPEATABLE READ',
        'max_overflow': 0,
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10
    }

    BROWSER_BIN = os.getenv('BROWSER_BIN', '/usr/bin/google-chrome-stable')
    MONITORING_URL = os.getenv('MONITORING_URL', 'http://monitoring:8001')
