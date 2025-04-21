from src.settings import config

from .db_manager import DBManager


async def initialize_db() -> DBManager:
    db = DBManager()
    await db.initialize(config.DB_HOST)
    return db


__all__ = ["initialize_db", "DBManager"]
