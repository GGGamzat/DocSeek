import os
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

ES_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ES_INDEX = "documents"

es_client = AsyncElasticsearch(hosts=[ES_URL])


async def create_index_if_not_exists() -> None:
    if not await es_client.indices.exists(index=ES_INDEX):
        await es_client.indices.create(index=ES_INDEX)


async def index_document(doc_id: int, text: str) -> None:
    await es_client.index(
        index=ES_INDEX,
        id=doc_id,
        document={"text": text}
    )


async def delete_document_from_index(doc_id: int) -> None:
    try:
        await es_client.delete(index=ES_INDEX, id=doc_id)
    except NotFoundError:
        pass


async def search_documents(query: str, size: int = 100) -> list[int]:
    response = await es_client.search(
        index=ES_INDEX,
        query={"match": {"text": query}},
        size=size,
        _source=False
    )
    return [int(hit["_id"]) for hit in response["hits"]["hits"]]