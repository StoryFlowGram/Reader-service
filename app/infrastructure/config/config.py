from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    user: str = Field(alias="READER_DB_USER")
    password: str = Field(alias="READER_DB_PASSWORD")
    db_name: str = Field(alias="READER_DB_NAME")
    
    host: str = Field(default="reader-db", alias="READER_DB_HOST")
    port: int = 5432

    def sqlalchemy_database_url(self, DB_API: str) -> URL:
        return URL.create(
            drivername=f"postgresql+{DB_API}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        )

class URLConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    book_service_url: str = Field(alias="READER_BOOK_SERVICE_URL")

class Config:
    def __init__(self):
        self.db = DatabaseConfig()
        self.url = URLConfig()