from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.protocols.reading_progress_protocol import ReadingProgressProtocol
from app.domain.entity.reading_progress import ReadingProgressDomain

from app.infrastructure.models.reading_progress import ReadingProgressModel
from app.infrastructure.mappers.reading_progress_mapper import orm_to_domain, domain_to_orm

class ReadingProgressRepository(ReadingProgressProtocol):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_book(self, user_book_id: int) -> Optional[ReadingProgressDomain]:
        stmt = select(ReadingProgressModel).where(ReadingProgressModel.user_book_id == user_book_id)
        result = await self.session.execute(stmt)
        orm_model = result.scalar_one_or_none()
        return orm_to_domain(orm_model) if orm_model else None

    async def add(self, progress: ReadingProgressDomain) -> ReadingProgressDomain:
        orm_model = domain_to_orm(progress)
        self.session.add(orm_model)
        await self.session.flush()
        await self.session.refresh(orm_model)

        return orm_to_domain(orm_model)

    async def update(self, progress: ReadingProgressDomain) -> ReadingProgressDomain:
        stmt = update(ReadingProgressModel).where(ReadingProgressModel.id == progress.id).values(
            position=progress.position,
            chapter_id=progress.chapter_id,
            updated_at=progress.updated_at 
        ).returning(ReadingProgressModel)
        
        result = await self.session.execute(stmt)
        orm_model = result.scalar_one_or_none()
        
        if not orm_model:
             raise ValueError(f"ReadingProgress with id {progress.id} not found for update")

        return orm_to_domain(orm_model)