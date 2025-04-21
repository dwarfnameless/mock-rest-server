from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Настройки приложения
    APP_TITLE: str = Field(default="MyApp")
    APP_VERSION: str = Field(default="0.1.0")
    APP_DESCRIPTION: str = Field(default="My application description")

    # Настройки сервера
    SERVER_HOST: str = Field(default="localhost")
    SERVER_PORT: int = Field(default=8000)
    SERVER_RELOAD: bool = Field(default=True)
    SERVER_WORKERS: int = Field(default=4)

    # Настройки базы данных
    DB_TYPE: str = Field(default="sqlite3")
    DB_HOST: str = Field(default="memory")
