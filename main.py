from fastapi import FastAPI


from app.presentation.api.v1.user_book.user_book_controller import user_book_router
from app.presentation.api.v1.reading_progress.reading_progress_controller import reading_progress_router
from app.infrastructure import di
from app.presentation.api import depends
from app.infrastructure.database.engine import flush_database, engine



app = FastAPI()

app.include_router(user_book_router)
app.include_router(reading_progress_router)



app.dependency_overrides[depends.book_protocol] = di.book_protocol
app.dependency_overrides[depends.reading_progress_protocol] = di.reading_progress_protocol

@app.on_event("startup")
async def startup_event():
    await flush_database(engine)
    pass