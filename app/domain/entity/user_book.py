from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserBook:
    user_id: int #из identity-service
    book_id: int # из book-service
    overall_progress: float
    id: Optional[int] = None
    added_at: Optional[datetime] = None