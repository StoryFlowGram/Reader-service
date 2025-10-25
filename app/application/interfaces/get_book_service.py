from typing import Protocol


class IBookServiceProtocol(Protocol):
    def get_book(self, book_id: int) -> dict:
        pass