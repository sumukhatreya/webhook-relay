import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Postgres — async URL for FastAPI, sync URL for Celery/Alembic
    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    REDIS_URL: str
    RABBITMQ_URL: str

    APP_NAME: str = "webhook-relay"
    DEBUG: bool = True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger


settings = Settings()
