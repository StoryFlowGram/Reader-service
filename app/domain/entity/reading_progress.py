from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReadingProgressDomain:
    user_book_id: int
    chapter_id: int
    position: float
    id: int | None = None
    updated_at: datetime | None = None