from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения.

    Использует pydantic для валидации и загрузки переменных окружения.

    Атрибуты:
        APP_TITLE (str): Название приложения.
        APP_VERSION (str): Версия приложения.
        APP_DESCRIPTION (str): Описание приложения.
        SERVER_HOST (str): Хост сервера.
        SERVER_PORT (int): Порт сервера.
        SERVER_RELOAD (bool): Перезапускать сервер при изменениях.
        SERVER_WORKERS (int): Количество воркеров сервера.
        DB_TYPE (str): Тип используемой базы данных.
        DB_HOST (str): Строка подключения к базе данных.
    """

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Настройки приложения
    APP_TITLE: str = Field(default="MyApp", description="Название приложения.")
    APP_VERSION: str = Field(default="0.2.0", description="Версия приложения.")
    APP_DESCRIPTION: str = Field(default="My application description", description="Описание приложения.")

    # Настройки сервера
    SERVER_HOST: str = Field(default="localhost", description="Хост, на котором запускается сервер.")
    SERVER_PORT: int = Field(default=8000, description="Порт, на котором запускается сервер.")
    SERVER_RELOAD: bool = Field(default=True, description="Перезапускать сервер при изменениях кода.")
    SERVER_WORKERS: int = Field(default=4, description="Количество воркеров для обработки запросов.")

    # Настройки базы данных
    DB_TYPE: str = Field(default="sqlite3", description="Тип используемой базы данных.")
    DB_HOST: str = Field(default="sqlite+aiosqlite:///:memory:", description="Строка подключения к базе данных.")
