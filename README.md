# DocSeek

Поисковик по текстовым документам. Принимает произвольный текстовый запрос,
ищет совпадения по тексту документов и возвращает первые 20 результатов,
отсортированных по дате создания. Также умеет удалять документы по ID.

## Стек

- **Backend**: Python 3.11, FastAPI
- **База данных**: PostgreSQL 15
- **Поисковый движок**: Elasticsearch 8.10.2
- **Оркестрация**: Docker, Docker Compose
- **Асинхронность**: `asyncpg`, `AsyncElasticsearch`, `SQLAlchemy[asyncio]`

## Требования

- Docker Desktop (или Docker Engine + Docker Compose)
- Свободные порты: `8000`, `5432`, `9200`

## Запуск

### 1. Клонируйте репозиторий

```
git clone https://github.com/GGGamzat/DocSeek
cd DocSeek
```

### 2. Запустите сервисы

```
docker-compose up --build
```

### 3. Откройте в браузере:

http://127.0.0.1:8000/docs