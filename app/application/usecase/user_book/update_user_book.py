from app.domain.exception.user_book import UserBookNotFound
from app.application.interfaces.uow import UnitOfWorkInterface
from app.application.dto.user_book.user_book_dto import UserBookDTO



class UpdateUserBookUseCase:
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow

    async def __call__(self, user_id: int, book_id: int, overall_progress: float):
        async with self.uow:
            check_exists = await self.uow.user_books.get(user_id, book_id)

            if not check_exists:
                raise UserBookNotFound("Книги нет в библиотеке")

            if overall_progress < 0 or overall_progress > 1:
                raise ValueError("overall_progress должен быть между 0 и 1")

            update_book = await self.uow.user_books.update(book_id, user_id, overall_progress)

        return UserBookDTO(
            id=update_book.id,
            user_id=update_book.user_id,
            book_id=update_book.book_id,
            added_at=update_book.added_at,
            overall_progress=update_book.overall_progress
        )