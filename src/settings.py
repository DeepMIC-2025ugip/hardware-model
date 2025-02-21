from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    backend_url: str = Field(..., alias="BACKEND_URL")

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()


settings = get_settings()
