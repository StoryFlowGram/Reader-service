from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AddRequestSchema(BaseModel):
    book_id: int
    overall_progress: float = 0.0

    model_config = ConfigDict(from_attributes=True)



class AddResponseSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    added_at: datetime
    overall_progress: float = 0.0


    model_config = ConfigDict(from_attributes=True)

class UpdateRequestSchema(BaseModel):
    book_id: int
    overall_progress: float