from math import log
from fastapi import HTTPException
from httpx import AsyncClient, RequestError
from loguru import logger

from app.infrastructure.config.config import Config
from app.application.interfaces.get_book_service import IBookServiceProtocol
from app.application.dto.book_service_dto import BookServiceDTO

config = Config()

class HttpBookService(IBookServiceProtocol):
    def __init__(self):
        self.base_url = config.url.BOOK_SERVICE_URL 

    async def get_book(self, book_id: int, target_chapter_id: int = None) -> BookServiceDTO:
        url = f"{self.base_url}/{book_id}/chapters"

        async with AsyncClient() as client:
            try:
                logger.info(f"Запрос к Book Service: {url}")
                response = await client.get(url)

                if response.status_code == 404:
                    logger.warning(f"Книга {book_id} не найдена в Book Service")
                    raise HTTPException(status_code=404, detail="Книга не найдена")
                
                if response.status_code != 200:
                    logger.error(f"Book Service ответил: {response.status_code}")
                    raise HTTPException(status_code=503, detail="Сервер книг вернул ошибку")
                
                data = response.json() 
                total_chapters = len(data) if isinstance(data, list) else 0
                
                current_order = 1
                if target_chapter_id and isinstance(data, list):

                    found_chapter = next((item for item in data if item.get('id') == target_chapter_id), None)
                    if found_chapter:
                        current_order = found_chapter.get('order_number', 1)
                    else:
                        logger.warning(f"Глава {target_chapter_id} не найдена в списке глав книги {book_id}")

                return BookServiceDTO(
                    id=book_id,
                    total_chapters=total_chapters,
                    current_chapter_order=current_order 
                )

            except RequestError as e:
                logger.critical(f"Не удалось подключиться к Book Service: {e}")
                raise HTTPException(status_code=503, detail="Book Service недоступен") from e