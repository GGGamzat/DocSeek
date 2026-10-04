from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models


async def get_documents_by_ids(
    db: AsyncSession, doc_ids: list[int]
) -> list[models.Document]:
    if not doc_ids:
        return []

    result = await db.execute(
        select(models.Document)
        .where(models.Document.id.in_(doc_ids))
        .order_by(models.Document.created_date.desc())
        .limit(20)
    )
    return list(result.scalars().all())


async def delete_document(db: AsyncSession, doc_id: int) -> models.Document | None:
    doc = await db.get(models.Document, doc_id)
    if doc:
        await db.delete(doc)
        await db.commit()
    return doc