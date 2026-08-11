from app.application.interfaces.uow import UnitOfWorkInterface


class RemoveBookFromLibraryUseCase:
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow

    async def __call__(self, user_id: int, book_id: int) -> bool:
        async with self.uow:
            # Primary path: API receives book_id.
            check_exists = await self.uow.user_books.get(user_id, book_id)
            if check_exists:
                await self.uow.user_books.delete(user_id, check_exists.book_id)
                return True

            # Fallback path: some clients send user_book_id to DELETE /reader/{id}.
            user_book = await self.uow.user_books.get_by_user_book_id(book_id)
            if user_book and user_book.user_id == user_id:
                await self.uow.user_books.delete(user_id, user_book.book_id)
                return True

            # DELETE should be idempotent: not-found is treated as success.
            return False
