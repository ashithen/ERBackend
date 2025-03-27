from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "LearnIt"
    max_file_size: int = 5 * 1024 * 1024  # 5 MB in bytes
    env = os.getenv("ENV", "local")

settings = Settings()