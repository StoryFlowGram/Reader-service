
from app.application.interfaces.get_book_service import IBookServiceProtocol
from app.application.dto.book_service_dto import BookServiceDTO



# TODO: rewrite when i will do binding all microservices together
class BookService(IBookServiceProtocol):
    async def get_book_details(self, book_id: int) -> BookServiceDTO:
        return BookServiceDTO(id=book_id, total_chapters=10) 