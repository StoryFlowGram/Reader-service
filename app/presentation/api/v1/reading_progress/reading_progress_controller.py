from fastapi import APIRouter, Depends, HTTPException, status

from app.application.usecase.reading_progress.upsert_reading_progress import UpsertReadingProgress 
from app.domain.entity.reading_progress import ReadingProgressDomain
from app.presentation.schemas.reading_progress.reading_progress_schemas import RequestSchema, ResponseSchema
from app.presentation.api.depends import reading_progress_protocol, book_protocol

reading_progress_router = APIRouter(
    prefix="/api/v1/reading_progress",
    tags=["reading_progress"]
)

@reading_progress_router.put("/update", response_model=ResponseSchema)
async def upsert_reading_progress(
    schema: RequestSchema, 
    progress_repo=Depends(reading_progress_protocol), 
    user_book_repo=Depends(book_protocol)
):
    usecase = UpsertReadingProgress(progress_repo, user_book_repo)

    progress_entity = ReadingProgressDomain(
        user_book_id=schema.user_book_id,
        chapter_id=schema.chapter_id,
        position=schema.position
    )
    try:
        updated_progress = await usecase(progress_entity)
        return updated_progress
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Внутрішня помилка: {e}")