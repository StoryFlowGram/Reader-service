from typing import Protocol

from app.application.dto.book_service_dto import BookServiceDTO

class IBookServiceProtocol(Protocol):
    async def get_book(self, book_id: int, target_chapter_id: int | None = None) -> BookServiceDTO:
        pass
