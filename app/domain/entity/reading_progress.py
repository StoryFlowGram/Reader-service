from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ReadingProgressDomain:
    user_book_id: int
    chapter_id: int
    position: float
    id: Optional[int] = None
    updated_at: Optional[datetime] = None