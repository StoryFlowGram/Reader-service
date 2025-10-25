from app.domain.entity.user_book import UserBook
from app.domain.exception.user_book import UserBookNotFound
from app.application.interfaces.uow import UnitOfWorkInterface



class RemoveBookFromLibraryUseCase:
    def __init__(self, uow:UnitOfWorkInterface):
        self.uow = uow

    async def __call__(self, user_id: int, book_id: int) -> None:
        async with self.uow:
            check_exists = await self.uow.user_books.get(user_id, book_id)
            if not check_exists:
                raise UserBookNotFound("Книги нет в библиотеке")
            await self.uow.user_books.delete(user_id, book_id)