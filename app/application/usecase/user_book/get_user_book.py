from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol



class GetUserBook:
    def __init__(self, protocol: UserBookProtocol):
        self.protocol = protocol


    async def __call__(self, user_id: int, book_id: int) -> UserBook:
        return await self.protocol.get(user_id, book_id)