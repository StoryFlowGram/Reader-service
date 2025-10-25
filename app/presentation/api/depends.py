async def book_protocol():
    raise NotImplementedError("Должен быть переопределён в инфра слое")


async def reading_progress_protocol():
    raise NotImplementedError("Должен быть переопределён в инфра слое")

async def uow_dependency():
    raise NotImplementedError("Должен быть переопределён в инфра слое")

async def book_service_provider():
    raise NotImplementedError("Должен быть переопределён в инфра слое")