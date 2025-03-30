from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "LearnIt"
    max_file_size: int = 5 * 1024 * 1024  # 5 MB in bytes
    env: str = os.getenv("ENV", "local")


settings = Settings()
