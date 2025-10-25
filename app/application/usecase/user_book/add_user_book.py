from app.domain.entity.user_book import UserBook
from app.application.interfaces.uow import UnitOfWorkInterface
from app.application.dto.user_book.user_book_dto import UserBookDTO

from app.domain.exception.user_book import BookAlreadyInLibrary



class AddBookToLibraryUseCase:
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow

    async def __call__(self, user_book: UserBook) -> None:
        async with self.uow:
            check_exists = await self.uow.user_books.get(user_book.user_id, user_book.book_id)

            if check_exists:
                raise BookAlreadyInLibrary("Книга уже в библиотеке")
            add_book = await self.uow.user_books.add(user_book)
        
        return UserBookDTO(
            id=add_book.id,
            user_id=add_book.user_id,
            book_id=add_book.book_id,
            added_at=add_book.added_at,
            overall_progress=add_book.overall_progress
        )


