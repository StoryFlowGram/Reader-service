from dataclasses import dataclass


@dataclass
class BookServiceDTO:
    id: int
    total_chapters: int