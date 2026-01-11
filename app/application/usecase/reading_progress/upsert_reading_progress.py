from datetime import datetime, timezone

from app.domain.exception.user_book import (
    UserBookNotFound, ProgressError
)

from app.application.interfaces.uow import UnitOfWorkInterface
from app.domain.entity.reading_progress import ReadingProgressDomain
from app.application.dto.reading_progress.reading_progress_dto import ReadingProgressDTO
from app.application.interfaces.get_book_service import IBookServiceProtocol 

class UpsertReadingProgressUseCase:
    def __init__(self, uow: UnitOfWorkInterface, book_service: IBookServiceProtocol): 
        self.uow = uow
        self.book_service = book_service

    async def __call__(self, user_id: int, progress_entity: ReadingProgressDomain) -> ReadingProgressDTO:
        async with self.uow:
            user_book = await self.uow.user_books.get_by_user_book_id(progress_entity.user_book_id)
            if not user_book:
                raise UserBookNotFound("Книга не найдена в библиотеке")
            
            if user_book.user_id != user_id:
                raise UserBookNotFound("У вас нет доступа к этой книге") 
            
            check_exist_progress = await self.uow.reading_progress.get_by_user_book(progress_entity.user_book_id)         
            if check_exist_progress:
                check_exist_progress.position = progress_entity.position
                check_exist_progress.chapter_id = progress_entity.chapter_id
                
                check_exist_progress.updated_at = datetime.now(timezone.utc)
                
                saved_progress = await self.uow.reading_progress.update(check_exist_progress)
            else:
                if not progress_entity.updated_at:
                    progress_entity.updated_at = datetime.now(timezone.utc)
                    
                saved_progress = await self.uow.reading_progress.add(progress_entity)
            
            if not saved_progress:
                raise ProgressError("Не удалось сохранить прогресс")

            book_info = await self.book_service.get_book(
                book_id=user_book.book_id, 
                target_chapter_id=progress_entity.chapter_id
            )
            
            total = book_info.total_chapters
            order = book_info.current_chapter_order

            if total > 0:
                raw_progress = (order - 1) + progress_entity.position
                overall = raw_progress / total
                
                if overall > 1.0: overall = 1.0
                if overall < 0.0: overall = 0.0
                
                user_book.overall_progress = overall 
            else:
                user_book.overall_progress = 0.0
            
            await self.uow.user_books.update(user_book) 
            await self.uow.commit()
        
            return ReadingProgressDTO(
                id=saved_progress.id,
                user_book_id=saved_progress.user_book_id,
                chapter_id=saved_progress.chapter_id,
                position=saved_progress.position,
                updated_at=saved_progress.updated_at
            )