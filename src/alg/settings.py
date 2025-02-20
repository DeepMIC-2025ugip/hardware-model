from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    
    db_host: str = Field(..., alias="DB_HOST")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_pass: str = Field(..., alias="DB_PASS")
    db_port: int = Field(..., alias="DB_PORT")

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()


settings = get_settings()
