from dataclasses import dataclass


@dataclass
class UserBookVO:
    user_id: int  
    book_id: int 


    def __post_init__(self):
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValueError("user_idт должен быть положительным целым числом")
        if not isinstance(self.book_id, int) or self.book_id <= 0:
            raise ValueError("book_id должен быть положительным целым числом")