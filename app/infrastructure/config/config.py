from pydantic_settings import BaseSettings
from sqlalchemy import URL


class DatabaseConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_NAME: str


    def sqlalchemy_database_url(self, DB_API: str) -> URL:
        return URL.create(
            drivername=f"postgresql+{DB_API}",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_DB,
            database=self.DB_NAME,
        )
    
    model_config = {
        "extra": "ignore",
        "env_file_encoding": "utf-8"
    }

class URLConfig(BaseSettings):
    BOOK_SERVICE_URL: str

    model_config = {
        "extra": "ignore",
        "env_file_encoding": "utf-8"
    }

class Config:
    def __init__(self, env_file: str | None = None):
        self.db = DatabaseConfig(_env_file=env_file)
        self.url = URLConfig(_env_file=env_file)
