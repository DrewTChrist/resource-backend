import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL")
    jwt_signature: str = os.getenv("SIGNATURE")
    resource_directory: str = os.getenv("RESOURCE_DIRECTORY")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND")
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config():
    return Configuration()
