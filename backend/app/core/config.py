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


settings = Settings()