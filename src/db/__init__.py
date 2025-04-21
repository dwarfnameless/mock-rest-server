from collections.abc import AsyncGenerator

from src.settings import config

from .db_manager import DBManager


async def initialize_db() -> DBManager:
    db = DBManager()
    await db.initialize(config.DB_HOST)
    return db


async def session() -> AsyncGenerator[DBManager, None]:
    db = DBManager()
    async with db.session():
        yield db


__all__ = ["initialize_db", "session"]
