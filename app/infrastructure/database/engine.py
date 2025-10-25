from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.infrastructure.config.config import Config
from app.infrastructure.database.base import Base

config = Config(env_file=".env")


engine: AsyncEngine = create_async_engine(
    config.db.sqlalchemy_database_url("asyncpg"),
    echo=True,
)
