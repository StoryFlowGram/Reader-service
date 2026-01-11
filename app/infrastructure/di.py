from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.database.uow import UnitOfWork
from app.infrastructure.repositories.user_book_repo import UserBookRepository
from app.infrastructure.repositories.reading_progress_repo import ReadingProgressRepository
from app.infrastructure.service.book_service import HttpBookService
from app.infrastructure.database.session import get_session



async def book_protocol(session:AsyncSession = Depends(get_session)):
    return UserBookRepository(session)



async def reading_progress_protocol(session:AsyncSession = Depends(get_session)):
    return ReadingProgressRepository(session)


def get_book_service_provider() :
    return HttpBookService()


async def uow_dependency():
    session: AsyncSession = await get_session()
    uow = UnitOfWork(session)
    
    try:
        return uow
    finally:
        await session.close()