from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "LearnIt"
    max_file_size: int = 5 * 1024 * 1024  # 5 MB in bytes
    env: str = "local"

    # SQL Settings
    sql_username: str
    sql_address: str
    sql_port: str
    sql_database: str

    #LLM
    gemini_api_key: str

    class Config:
        env_file = "../../.env"




settings = Settings()
