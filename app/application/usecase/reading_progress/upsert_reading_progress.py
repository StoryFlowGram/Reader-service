from app.domain.exception.user_book import (
    UserBookNotFound, ProgressError
)

from app.application.interfaces.uow import UnitOfWorkInterface
from app.domain.entity.reading_progress import ReadingProgressDomain
from app.application.dto.reading_progress.reading_progress_dto import ReadingProgressDTO

class UpsertReadingProgressUseCase:
    def __init__(self, uow: UnitOfWorkInterface): 
        self.uow = uow

    async def __call__(self, progress_entity: ReadingProgressDomain) -> ReadingProgressDTO:
        async with self.uow:
            user_book = await self.uow.user_books.get_by_user_book_id(progress_entity.user_book_id)
            if not user_book:
                raise UserBookNotFound("Книга не найдена ")
            
            check_exist_progress = await self.uow.reading_progress.get_by_user_book(progress_entity.user_book_id)
            if check_exist_progress:
                check_exist_progress.position = progress_entity.position
                check_exist_progress.chapter_id = progress_entity.chapter_id
            
                saved_progress = await self.uow.reading_progress.update(check_exist_progress)
            else:
                saved_progress = await self.uow.reading_progress.add(progress_entity)
            
            if not saved_progress:
                raise ProgressError("Не удалось сохранить объект")
        
            user_book.overall_progress = saved_progress.position

            await self.uow.user_books.update(user_book.user_id, user_book.book_id)
        
        return ReadingProgressDTO(
            id=saved_progress.id,
            user_book_id=saved_progress.user_book_id,
            chapter_id=saved_progress.chapter_id,
            position=saved_progress.position,
            updated_at=saved_progress.updated_at
        )