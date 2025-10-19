from app.domain.entity.user_book import UserBook
from app.domain.protocols.user_book_protocol import UserBookProtocol

class ListUserBooks:
    def __init__(self, protocol: UserBookProtocol):
        self.protocol = protocol

    async def __call__(self, user: UserBook) -> list[UserBook]:
        return await self.protocol.get_list_by_user(user.user_id)