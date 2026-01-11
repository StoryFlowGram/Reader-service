from fastapi import FastAPI


from app.presentation.api.v1.user_book.user_book_controller import user_book_router
from app.presentation.api.v1.reading_progress.reading_progress_controller import reading_progress_router
from app.infrastructure import di
from app.presentation.api import depends



app = FastAPI()

app.include_router(user_book_router)
app.include_router(reading_progress_router)



app.dependency_overrides[depends.book_protocol] = di.book_protocol
app.dependency_overrides[depends.reading_progress_protocol] = di.reading_progress_protocol
app.dependency_overrides[depends.uow_dependency] = di.uow_dependency
app.dependency_overrides[depends.book_service_provider] = di.get_book_service_provider
