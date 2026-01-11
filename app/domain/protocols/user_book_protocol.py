from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from app.domain.entity.user_book import UserBook


class UserBookProtocol(ABC):
    @abstractmethod
    async def add(self, user_book: UserBook) -> None:
        ...

    @abstractmethod
    async def get(self, user_id: int, book_id: int):
        ...

    @abstractmethod
    async def delete(self, user_id: int, book_id: int) -> None:
        ...

    @abstractmethod
    async def get_list_by_user(self, user_id: int) -> list[UserBook]:
        ...

    @abstractmethod
    async def update(self, user_book: UserBook) -> UserBook:
        ...
    
    @abstractmethod
    async def get_by_user_book_id(self, user_book_id) -> UserBook:
        ...