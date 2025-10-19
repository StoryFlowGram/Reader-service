from dataclasses import dataclass
from datetime import datetime



@dataclass
class UserBookDTO:
    id: int
    user_id: int
    book_id: int
    added_at: datetime
    overall_progress: float