from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.repositories.user_book_repo import UserBookRepository
from app.infrastructure.repositories.reading_progress_repo import ReadingProgressRepository
from app.infrastructure.database.session import get_session



async def book_protocol(session:AsyncSession = Depends(get_session)):
    return UserBookRepository(session)



async def reading_progress_protocol(session:AsyncSession = Depends(get_session)):
    return ReadingProgressRepository(session)