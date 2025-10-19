from dataclasses import dataclass


@dataclass
class ReadingProgressVO:
    
    chapter_id: int
    position: float

    def __post_init__(self):
        if not isinstance(self.position, float):
            raise ValueError("position должен быть числом с плавающей точкой")
        
        if not (0.0 <= self.position <= 1.0):
            raise ValueError("position  в диапазоне от 0.0 до 1.0")
        
    @property
    def as_percentage(self) -> float:
        return round(self.position * 100, 2)