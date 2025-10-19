from pydantic_settings import BaseSettings
from sqlalchemy import URL


class DatabaseConfig(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str


    def sqlalchemy_database_url(self, DB_API: str) -> URL:
        return URL.create(
            drivername=f"postgresql+{DB_API}",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            database=self.DB_NAME,
        )
    
    model_config = {
        "extra": "ignore",
        "env_file_encoding": "utf-8"
    }


class Config:
    def __init__(self, env_file: str | None = None):
        self.db = DatabaseConfig(_env_file=env_file)
