from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud, schemas, elastic
from .database import get_db, engine
from .models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await elastic.create_index_if_not_exists()

    yield

    await elastic.es_client.close()


app = FastAPI(
    title="Simple Document Search Service",
    description="Поиск по документам: FastAPI + PostgreSQL + Elasticsearch",
    lifespan=lifespan
)


@app.get("/search", response_model=List[schemas.DocumentResponse])
async def search(
    query: str = Query(..., min_length=1, description="Поисковый запрос"),
    db: AsyncSession = Depends(get_db)
):
    doc_ids = await elastic.search_documents(query)
    if not doc_ids:
        return []

    documents = await crud.get_documents_by_ids(db, doc_ids)
    return documents


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    deleted_doc = await crud.delete_document(db, doc_id)
    if not deleted_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    await elastic.delete_document_from_index(doc_id)
    return {"message": f"Document {doc_id} deleted"}