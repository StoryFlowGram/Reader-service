from app.domain.entity.user_book import UserBook
from app.application.interfaces.uow import UnitOfWorkInterface
from app.domain.exception.user_book import UserBookNotFound
from app.application.dto.user_book.user_book_dto import UserBookDTO


class ListUserBooksUseCase:
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow

    async def __call__(self, user_id: int) -> list[UserBook]:
        async with self.uow:
            result_list = await self.uow.user_books.get_list_by_user(user_id)
            if not result_list:
                UserBookNotFound("Книги не найдены. Возможно их у пользователя просто нет")

        return [
            UserBookDTO(
            id=result_list.id,
            user_id=result_list.user_id,
            book_id=result_list.book_id,
            added_at=result_list.added_at,
            overall_progress=result_list.overall_progress
            ) for result_list in result_list
            ]