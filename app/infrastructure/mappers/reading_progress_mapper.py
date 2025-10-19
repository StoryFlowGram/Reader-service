from app.domain.entity.reading_progress import ReadingProgressDomain
from app.infrastructure.models.reading_progress import ReadingProgressModel


def orm_to_domain(orm: ReadingProgressModel):
    return ReadingProgressDomain(
        id = orm.id,
        user_book_id = orm.user_book_id,
        chapter_id = orm.chapter_id,
        position = orm.position,
        updated_at = orm.updated_at
    )


def domain_to_orm(domain: ReadingProgressDomain):
    return ReadingProgressModel(
        user_book_id = domain.user_book_id,
        chapter_id = domain.chapter_id,
        position = domain.position,
    )