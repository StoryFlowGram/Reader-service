from app.domain.entity.user_book import UserBook
from app.infrastructure.models.user_book import UserBookModel


def orm_to_domain(orm: UserBookModel) -> UserBook:
    return UserBook(
        id=orm.id,
        user_id=orm.user_id,
        book_id=orm.book_id,
        added_at=orm.added_at,
        overall_progress=orm.overall_progress
    )

def domain_to_orm(domain: UserBook) -> UserBookModel:
    return UserBookModel(
        user_id=domain.user_id,
        book_id=domain.book_id,
        overall_progress=domain.overall_progress
    )