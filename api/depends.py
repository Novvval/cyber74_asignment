from sqlalchemy.ext.asyncio import create_async_engine

from app.repository import Repository
from config import Config
from db import Database

engine = create_async_engine(
    Config.PG_URL, **Config.ENGINE_KWARGS
)

db = Database(engine)

def get_repository() -> Repository:
    return Repository(db)