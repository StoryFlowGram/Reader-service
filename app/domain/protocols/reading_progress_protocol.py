from abc import ABC , abstractmethod
from app.domain.entity.reading_progress import ReadingProgressDomain




class ReadingProgressProtocol(ABC):

    @abstractmethod
    async def add(self, reading_progress:ReadingProgressDomain) -> ReadingProgressDomain:
        ...

    @abstractmethod
    async def update(self, progress: ReadingProgressDomain) -> ReadingProgressDomain:
        ...


    @abstractmethod
    async def get_by_user_book(self, user_book_id: int):
        ...

    