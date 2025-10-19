from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy.types import DateTime, Float, Integer
from sqlalchemy import func, CheckConstraint, UniqueConstraint, Index

from app.infrastructure.database.base import Base



class UserBookModel(Base):
    __tablename__ = "user_books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    overall_progress: Mapped[float] = mapped_column(Float, default=0.0, doc="общий прогресс пользователя по книге")
    reading_progress = relationship("ReadingProgressModel", back_populates="user_book_rs", cascade="all, delete-orphan")

    @validates("overall_progress")
    def validate_overall_progress(self, key, value):
        if not (0.0 <= value <= 1.0):
            raise ValueError("overall_progress должен быть между 0 и 1")
        return value
    
    __table_args__ = (
        CheckConstraint('overall_progress >= 0.0 AND overall_progress <= 1.0', name='check_overall_progress_range'),
        UniqueConstraint('user_id', 'book_id', name='uq_user_book'), 
        Index('ix_user_book_user_id', 'user_id'),
    )
