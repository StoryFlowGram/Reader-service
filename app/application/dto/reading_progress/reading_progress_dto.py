from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ReadingProgressDTO:
    id: int
    user_book_id: int
    chapter_id: int
    position: float
    updated_at: datetime