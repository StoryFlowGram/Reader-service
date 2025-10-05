from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserBook:
    id: int
    user_id: int #из identity-service
    book_id: int # из book-service
    added_at: datetime
    overall_progress: float