# API-сервис для вопросов и ответов

REST API сервис для управления вопросами и ответами, построенный на FastAPI с использованием PostgreSQL и SQLAlchemy ORM.

## Описание проекта

Сервис предоставляет API для создания и управления вопросами и ответами.

### Запуск через Docker Compose

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd AQtest
```

2. Запустите приложение:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: `http://localhost:8000`

API документация (Swagger UI): `http://localhost:8000/docs`

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения (создайте `.env` файл):
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/qa_db
```

4. Запустите PostgreSQL (через Docker):
```bash
docker-compose up db -d
```

5. Примените миграции:
```bash
alembic upgrade head
```

6. Запустите приложение:
```bash
uvicorn app.main:app --reload
```


## Тестирование

Запуск тестов:

```bash
pytest
```

## Технологии

- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Alembic**
- **Pydantic**
- **Pytest** 
- **Docker** 
