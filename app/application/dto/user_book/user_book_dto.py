from dataclasses import dataclass
from datetime import datetime




@dataclass
class UserBookDTO:
    id: int
    user_id: int
    book_id: int
    overall_progress: float
    added_at: datetime