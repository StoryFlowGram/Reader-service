from fastapi import APIRouter, Depends, HTTPException, status

from app.application.interfaces.get_book_service import IBookServiceProtocol
from app.application.usecase.reading_progress.upsert_reading_progress import UpsertReadingProgressUseCase
from app.domain.entity.reading_progress import ReadingProgressDomain

from app.application.interfaces.uow import UnitOfWorkInterface
from app.presentation.schemas.reading_progress.reading_progress_schemas import RequestSchema, ResponseSchema
from app.presentation.api.depends import get_id_from_header, book_service_provider, uow_dependency 

reading_progress_router = APIRouter(tags=["reading_progress"])

@reading_progress_router.put("/update", response_model=ResponseSchema)
async def upsert_reading_progress(
    schema: RequestSchema, 
    uow: UnitOfWorkInterface = Depends(uow_dependency),
    user_id: int = Depends(get_id_from_header),
    book_service: IBookServiceProtocol = Depends(book_service_provider)
):
    usecase = UpsertReadingProgressUseCase(uow, book_service)
    progress_entity = ReadingProgressDomain(**schema.model_dump())
    try:
        return await usecase(user_id, progress_entity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))