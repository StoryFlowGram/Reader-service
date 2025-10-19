from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol
from app.application.dto.user_book.user_book_dto import UserBookDTO



class AddBookToLibrary:
    def __init__(self, protocol: UserBookProtocol):
        self.protocol = protocol

    async def __call__(self, user_book: UserBook) -> None:
        check_exists = await self.protocol.get(user_book.user_id, user_book.book_id)

        if check_exists:
            raise ValueError("Книга уже в библиотеке")
        add_book = await self.protocol.add(user_book)
        
        return UserBookDTO(
            id=add_book.id,
            user_id=add_book.user_id,
            book_id=add_book.book_id,
            added_at=add_book.added_at,
            overall_progress=add_book.overall_progress
        )


