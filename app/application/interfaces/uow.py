from typing import Protocol
from app.domain.protocols.reading_progress_protocol import ReadingProgressProtocol
from app.domain.protocols.user_book_protocol import UserBookProtocol

class UnitOfWorkInterface(Protocol):
    reading_progress: ReadingProgressProtocol
    user_books: UserBookProtocol

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def commit(self):
        ...
    
    async def rollback(self):
        ...