from fastapi import APIRouter, Depends, HTTPException


from app.presentation.api.depends import uow_dependency, get_id_from_header
from app.domain.entity.user_book import UserBook
from app.domain.exception.user_book import BookAlreadyInLibrary
from app.application.interfaces.uow import UnitOfWorkInterface
from app.application.usecase.user_book.add_user_book import AddBookToLibraryUseCase
from app.application.usecase.user_book.get_user_book import GetUserBookUseCase
from app.application.usecase.user_book.list_user_book import ListUserBooksUseCase
from app.application.usecase.user_book.remove_user_book import RemoveBookFromLibraryUseCase
from app.application.usecase.user_book.update_user_book import UpdateUserBookUseCase
from app.presentation.schemas.user_book.user_book_schemas import AddRequestSchema, AddResponseSchema, UpdateRequestSchema


user_book_router = APIRouter(tags=["user_book"])


@user_book_router.post("/", response_model=AddResponseSchema)
async def add_user_book(
    add_schema: AddRequestSchema, 
    uow: UnitOfWorkInterface = Depends(uow_dependency),
    user_id: int = Depends(get_id_from_header)
):
    usecase = AddBookToLibraryUseCase(uow)
    user_book_entity = UserBook(user_id=user_id, **add_schema.model_dump())
    try:
        add_book = await usecase(user_id, user_book_entity) 
        return add_book
    except BookAlreadyInLibrary as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_book_router.get("/{book_id}", response_model=AddResponseSchema)
async def get_user_book(
    book_id: int,
    uow: UnitOfWorkInterface = Depends(uow_dependency),
    user_id: int = Depends(get_id_from_header)
    ):
    usecase = GetUserBookUseCase(uow)
    try:
        get_book = await usecase(user_id,book_id)
        return get_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_book_router.get("/", response_model=list[AddResponseSchema])
async def list_user_book(
    uow: UnitOfWorkInterface = Depends(uow_dependency),
    user_id: int = Depends(get_id_from_header)
    ):
    usecase = ListUserBooksUseCase(uow)
    try:
        get_list_book = await usecase(user_id)
        return get_list_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_book_router.delete("/{book_id}")
async def remove_user_book(
    book_id: int,
    uow: UnitOfWorkInterface = Depends(uow_dependency),
    user_id: int = Depends(get_id_from_header)
    ):
    usecase = RemoveBookFromLibraryUseCase(uow)
    try:
        remove_book = await usecase(user_id,book_id)
        return remove_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))