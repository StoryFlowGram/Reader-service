from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol
from app.application.dto.user_book.user_book_dto import UserBookDTO



class UpdateUserBook:
    def __init__(self, protocol: UserBookProtocol):
        self.protocol = protocol

    async def __call__(self, user_id: int, book_id: int, overall_progress: float) -> UserBookDTO:
        check_exists = await self.protocol.get(user_id, book_id)

        if not check_exists:
            raise ValueError("Книги нет в библиотеке")
        
        if overall_progress < 0 or overall_progress > 1:
            raise ValueError("overall_progress должен быть между 0 и 1")

        update_book = await self.protocol.update(book_id, user_id, overall_progress)

        return UserBookDTO(
            id=update_book.id,
            user_id=update_book.user_id,
            book_id=update_book.book_id,
            added_at=update_book.added_at,
            overall_progress=update_book.overall_progress
        )