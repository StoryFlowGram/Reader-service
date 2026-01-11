from fastapi import HTTPException, Header


async def book_protocol():
    raise NotImplementedError("Должен быть переопределён в инфра слое")


async def reading_progress_protocol():
    raise NotImplementedError("Должен быть переопределён в инфра слое")

async def uow_dependency():
    raise NotImplementedError("Должен быть переопределён в инфра слое")

async def book_service_provider():
    raise NotImplementedError("Должен быть переопределён в инфра слое")


async def get_id_from_header(x_user_id: str = Header(None, alias="X-User-Id")) -> int:
    if x_user_id is None:
        raise HTTPException(400, "Отсутствует заголовок X-Id-User")
    return int(x_user_id)