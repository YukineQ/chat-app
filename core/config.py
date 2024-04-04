import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    JWT_SECRET: str = "efwfwepfkwe32324kewfwefwe"
    JWT_ALGORITHM: str = "HS256"
    WRITER_DB_URL: str = "sqlite+aiosqlite:///temp.db"
    READER_DB_URL: str = "sqlite+aiosqlite:///temp.db"


class LocalConfig(Config):
    ...


class ProductionConfig(Config):
    ...


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
