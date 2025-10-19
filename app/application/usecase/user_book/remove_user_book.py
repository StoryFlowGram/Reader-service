from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol



class RemoveBookFromLibrary:
    def __init__(self, protocol: UserBookProtocol):
        self.protocol = protocol

    async def __call__(self, user_id: int, book_id: int) -> None:
        check_exists = await self.protocol.get(user_id, book_id)
        if not check_exists:
            raise ValueError("Книги нет в библиотеке")
        await self.protocol.delete(user_id, book_id)