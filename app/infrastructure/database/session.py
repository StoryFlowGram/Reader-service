from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.infrastructure.database.engine import engine


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        return session