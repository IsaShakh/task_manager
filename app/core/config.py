from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    RABBITMQ_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()