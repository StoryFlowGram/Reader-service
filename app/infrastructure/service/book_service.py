from fastapi import HTTPException
from httpx import AsyncClient, RequestError
from loguru import logger

from app.application.dto.book_service_dto import BookServiceDTO
from app.application.interfaces.get_book_service import IBookServiceProtocol
from app.infrastructure.config.config import Config

config = Config()


class HttpBookService(IBookServiceProtocol):
    def __init__(self):
        self.base_url = config.url.book_service_url
        self.gateway_token = config.security.internal_gateway_token

    async def get_book(self, book_id: int, target_chapter_id: int = None) -> BookServiceDTO:
        url = f"{self.base_url}/{book_id}/chapters"
        headers = {"X-Gateway-Token": self.gateway_token}

        async with AsyncClient() as client:
            try:
                logger.info(f"Requesting Book Service URL: {url}")
                response = await client.get(url, headers=headers)

                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Книгу не знайдено")

                if response.status_code != 200:
                    logger.error(f"Book Service responded with status {response.status_code}")
                    raise HTTPException(
                        status_code=503,
                        detail="Сервіс книг тимчасово недоступний",
                    )

                data = response.json()
                total_chapters = len(data) if isinstance(data, list) else 0

                current_order = 1
                if target_chapter_id and isinstance(data, list):
                    found_chapter = next(
                        (item for item in data if item.get("id") == target_chapter_id),
                        None,
                    )
                    if found_chapter:
                        current_order = found_chapter.get("order_number", 1)
                    else:
                        logger.warning(
                            f"Chapter {target_chapter_id} not found in book {book_id} chapter list"
                        )

                return BookServiceDTO(
                    id=book_id,
                    total_chapters=total_chapters,
                    current_chapter_order=current_order,
                )

            except RequestError as error:
                logger.critical(f"Book Service request failed: {error}")
                raise HTTPException(
                    status_code=503,
                    detail="Сервіс книг тимчасово недоступний",
                ) from error
