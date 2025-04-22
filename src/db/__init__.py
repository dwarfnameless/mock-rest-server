"""Модуль инициализации базы данных.

Содержит функции и классы для инициализации и управления соединением с базой данных.
"""

from src.settings import config

from .db_manager import DBManager


async def initialize_db() -> DBManager:
    """Инициализирует соединение с базой данных.

    Возвращает:
        DBManager: Экземпляр менеджера базы данных с установленным соединением.
    """
    db = DBManager()
    await db.initialize(config.DB_HOST)
    return db


__all__ = ["initialize_db", "DBManager"]
