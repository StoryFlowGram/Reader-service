from datetime import datetime
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol
from app.infrastructure.models.user_book import UserBookModel
from app.infrastructure.mappers.user_book_mapper import domain_to_orm, orm_to_domain




class UserBookRepository(UserBookProtocol):
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    
    async def add(self, user_book: UserBook):
        orm = domain_to_orm(user_book)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return orm_to_domain(orm)
    
    async def get(self, user_id: int, book_id: int):
        stmt = select(UserBookModel).where(UserBookModel.user_id == user_id).where(UserBookModel.book_id == book_id)
        result = await self.session.execute(stmt)
        orm = result.scalars().one_or_none()
        if not orm:
            return None
        return orm_to_domain(orm)
    
    async def delete(self, user_id: int, book_id: int):
        stmt = delete(UserBookModel).where(UserBookModel.user_id == user_id).where(UserBookModel.book_id == book_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, user_id: int, book_id: int,  overall_progress: Optional[float]) -> UserBook:
        stmt = update(UserBookModel).where(UserBookModel.user_id == user_id).where(UserBookModel.book_id == book_id).values(
            overall_progress=overall_progress
        )
        await self.session.execute(stmt)
        await self.session.commit()
        stmt_select = select(UserBookModel).where(UserBookModel.user_id == user_id).where(UserBookModel.book_id == book_id)
        result = await self.session.execute(stmt_select)
        orm = result.scalars().one_or_none()
        return orm_to_domain(orm)

    async def get_list_by_user(self, user_id: int):
        stmt = select(UserBookModel).where(UserBookModel.user_id == user_id)
        result = await self.session.execute(stmt)
        orm = result.scalars().all()
        if not orm:
            return None
        return orm_to_domain(orm)
    
    async def get_by_user_book_id(self, user_book_id):
        stmt = select(UserBookModel).where(UserBookModel.id == user_book_id)
        result = await self.session.execute(stmt)
        orm = result.scalars().one_or_none()
        if not orm:
            return None
        return orm_to_domain(orm)
    