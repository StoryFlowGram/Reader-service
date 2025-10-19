from app.domain.protocols.user_book_protocol import UserBookProtocol
from app.domain.protocols.reading_progress_protocol import ReadingProgressProtocol
from app.domain.entity.reading_progress import ReadingProgressDomain
from app.domain.entity.user_book import UserBook
from app.application.dto.reading_progress.reading_progress_dto import ReadingProgressDTO

class UpsertReadingProgress:
    def __init__(self, progress_repo: ReadingProgressProtocol, user_book_repo: UserBookProtocol) -> None:
        self.progress_repo = progress_repo
        self.user_book_repo = user_book_repo

    async def __call__(self, reading_progress: ReadingProgressDomain) -> ReadingProgressDTO:

        user_book: UserBook = await self.user_book_repo.get_by_user_book_id(reading_progress.user_book_id)
        
        if not user_book:
            raise ValueError(f"Книга з user_book_id={reading_progress.user_book_id} не знайдена в бібліотеці.")

        existing_progress = await self.progress_repo.get_by_user_book(reading_progress.user_book_id)
        
        saved_progress: ReadingProgressDomain

        if existing_progress:
            existing_progress.position = reading_progress.position
            existing_progress.chapter_id = reading_progress.chapter_id
            
            saved_progress = await self.progress_repo.update(existing_progress)
            
        else:
            saved_progress = await self.progress_repo.add(reading_progress)

        if not saved_progress:
            raise Exception("Не вдалося зберегти прогрес читання. Репозиторій повернув None.")
        
        await self.user_book_repo.update(
            user_id=user_book.user_id,      
            book_id=user_book.book_id,       
            overall_progress=saved_progress.position  
        )

        return ReadingProgressDTO(
            id=saved_progress.id,
            user_book_id=saved_progress.user_book_id,
            chapter_id=saved_progress.chapter_id,
            position=saved_progress.position,
            updated_at=saved_progress.updated_at
        )