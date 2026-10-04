import asyncio
import ast
import pandas as pd
from datetime import datetime
from sqlalchemy.future import select

from .database import AsyncSessionLocal, engine
from .models import Base, Document
from . import elastic


async def wait_for_elasticsearch(max_attempts: int = 30, delay: float = 2.0):
    for attempt in range(1, max_attempts + 1):
        try:
            await elastic.es_client.indices.exists(index=elastic.ES_INDEX)
            print("Elasticsearch готов.")
            return
        except Exception as e:
            print(f"Попытка {attempt}/{max_attempts}: ES не готов ({type(e).__name__}), ждем {delay}с...")
            await asyncio.sleep(delay)
    raise RuntimeError("Elasticsearch так и не стал доступен")


async def populate_data():
    await wait_for_elasticsearch()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await elastic.create_index_if_not_exists()

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Document).limit(1))
        if result.scalar_one_or_none():
            print("БД уже заполнена, пропускаем.")
            return

    print("Загружаем данные из posts.csv...")
    df = pd.read_csv("posts.csv")

    documents = []
    for _, row in df.iterrows():
        try:
            rubrics_list = ast.literal_eval(row["rubrics"])
            doc = Document(
                text=row["text"],
                created_date=datetime.strptime(
                    row["created_date"], "%Y-%m-%d %H:%M:%S"
                ),
                rubrics=rubrics_list
            )
            documents.append(doc)
        except Exception as e:
            print(f"Ошибка в строке: {e}")

    async with AsyncSessionLocal() as db:
        db.add_all(documents)
        await db.commit()

        for doc in documents:
            await elastic.index_document(doc.id, doc.text)

    print(f"Загружено {len(documents)} документов.")


if __name__ == "__main__":
    asyncio.run(populate_data())