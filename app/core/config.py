import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_DIR: str = os.getcwd()
    app_name: str = "LearnIt"
    max_file_size: int = 5 * 1024 * 1024  # 5 MB in bytes
    env: str = "local"

    # SQL Settings
    sql_username: str
    sql_address: str
    sql_port: int = 3306
    sql_database: str

    # LLM
    gemini_api_key: str




settings = Settings()
# print(settings.model_dump())
