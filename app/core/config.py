from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "LearnIt"
    max_file_size: int = 5 * 1024 * 1024  # 5 MB in bytes
    env: str = os.getenv("ENV", "local")

    # SQL Settings
    sql_username: str = os.getenv("SQL_USERNAME", "data_admin")
    sql_address: str = os.getenv("SQL_ADDRESS", "34.121.59.245")
    sql_port: str = os.getenv("SQL_PORT", "3306")
    sql_database: str = os.getenv("SQL_DATABASE", "doc_data")


settings = Settings()
