from app.domain.entity.user_book import UserBook
from app.application.interfaces.uow import UnitOfWorkInterface
from app.domain.exception.user_book import UserBookNotFound
from app.application.dto.user_book.user_book_dto import UserBookDTO



class GetUserBookUseCase:
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow


    async def __call__(self, user_id: int, book_id: int) -> UserBook:
        async with self.uow:
            check_exists = await self.uow.user_books.get(user_id, book_id)
            if not check_exists:
                raise UserBookNotFound("Книги нет в библиотеке")
        
        return UserBookDTO(
            id=check_exists.id,
            user_id=check_exists.user_id,
            book_id=check_exists.book_id,
            added_at=check_exists.added_at,
            overall_progress=check_exists.overall_progress
        )