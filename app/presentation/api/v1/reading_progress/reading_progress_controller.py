from fastapi import APIRouter, Depends, HTTPException, status

from app.application.usecase.reading_progress.upsert_reading_progress import UpsertReadingProgressUseCase
from app.domain.entity.reading_progress import ReadingProgressDomain

from app.application.interfaces.uow import UnitOfWorkInterface
from app.presentation.schemas.reading_progress.reading_progress_schemas import RequestSchema, ResponseSchema
from app.presentation.api.depends import reading_progress_protocol, book_protocol, uow_dependency

reading_progress_router = APIRouter(
    prefix="/api/v1/reading_progress",
    tags=["reading_progress"]
)

@reading_progress_router.put("/update", response_model=ResponseSchema)
async def upsert_reading_progress(
    schema: RequestSchema, 
    uow: UnitOfWorkInterface = Depends(uow_dependency)
):
    usecase = UpsertReadingProgressUseCase(uow)
    progress_entity = ReadingProgressDomain(**schema.model_dump())
    try:
        return await usecase(progress_entity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))