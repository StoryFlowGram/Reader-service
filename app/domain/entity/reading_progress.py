from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReaddingProgress:
    id: int
    user_book_id: int
    chapter_id: int
    position: float
    updated_at: datetime