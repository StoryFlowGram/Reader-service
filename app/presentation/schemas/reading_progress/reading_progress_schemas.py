from pydantic import BaseModel, ConfigDict
from datetime import datetime



class RequestSchema(BaseModel):
    user_book_id: int
    chapter_id: int
    position: float

    model_config = ConfigDict(from_attributes=True)

class ResponseSchema(BaseModel):
    id: int
    user_book_id: int
    chapter_id: int
    position: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)