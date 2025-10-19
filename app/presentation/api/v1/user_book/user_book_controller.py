from fastapi import APIRouter, Depends, HTTPException

from app.presentation.api.depends import book_protocol
from app.application.usecase.user_book.add_user_book import AddBookToLibrary
from app.application.usecase.user_book.get_user_book import GetUserBook
from app.application.usecase.user_book.list_user_book import ListUserBooks
from app.application.usecase.user_book.remove_user_book import RemoveBookFromLibrary
from app.application.usecase.user_book.update_user_book import UpdateUserBook
from app.presentation.schemas.user_book.user_book_schemas import AddRequestSchema, AddResponseSchema, UpdateRequestSchema


user_book_router = APIRouter(
    prefix="/api/v1/user_book",
    tags=["user_book"]
)


@user_book_router.post("/add", response_model=AddResponseSchema)
async def add_user_book(add_schema: AddRequestSchema, protocol = Depends(book_protocol)):
    usecase = AddBookToLibrary(protocol)
    try:
        add_book = await usecase(add_schema)
        return add_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_book_router.get("/get_book", response_model=AddResponseSchema)
async def get_user_book(user_id: int,book_id: int,protocol = Depends(book_protocol)):
    usecase = GetUserBook(protocol)
    try:
        get_book = await usecase(user_id,book_id)
        return get_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_book_router.get("/list", response_model=list[AddResponseSchema])
async def list_user_book(user_id: int, protocol = Depends(book_protocol)):
    usecase = ListUserBooks(protocol)
    try:
        get_list_book = await usecase(user_id)
        return get_list_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_book_router.put("/update", response_model=AddResponseSchema)
async def update_user_book(user_id: int, book_id: int,  update_schema: UpdateRequestSchema, protocol = Depends(book_protocol)):
    usecase = UpdateUserBook(protocol)
    try:
        update_book = await usecase(user_id,book_id,update_schema.overall_progress)
        return update_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_book_router.delete("/delete")
async def remove_user_book(user_id: int, book_id: int,protocol = Depends(book_protocol)):
    usecase = RemoveBookFromLibrary(protocol)
    try:
        remove_book = await usecase(user_id,book_id)
        return remove_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))