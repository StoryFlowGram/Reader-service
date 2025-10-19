from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy.types import Integer, Float, DateTime
from sqlalchemy import func, ForeignKey

from app.infrastructure.database.base import Base




class ReadingProgressModel(Base):
    __tablename__ = "reading_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_book_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_books.id"))
    chapter_id: Mapped[int] = mapped_column(Integer)
    position: Mapped[float] = mapped_column(Float, doc="прогресс пользователя по главе в книге")
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_book_rs = relationship("UserBookModel", back_populates="reading_progress")


    @validates("position")
    def validate_position(self,key, value):
        if not (0.0 <= value <= 1.0):
            raise ValueError("position должен быть между 0.0 и 1.0")
        return value
