from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.reading_progress_repo import ReadingProgressRepository
from app.infrastructure.repositories.user_book_repo import UserBookRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        self.reading_progress = ReadingProgressRepository(session)
        self.user_books = UserBookRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.rollback()
            raise e

    async def rollback(self):
        await self.session.rollback()