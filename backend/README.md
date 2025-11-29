# HR SaaS Backend

FastAPI backend для платформы HR-автоматизации с AI-скринингом.

## Структура проекта

```
backend/
├── app/
│   ├── main.py              # Точка входа FastAPI
│   ├── config.py            # Конфигурация
│   ├── database.py          # Database setup
│   ├── dependencies.py      # FastAPI dependencies
│   ├── models/              # SQLModel модели
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API endpoints
│   │   ├── auth.py
│   │   ├── vacancies.py
│   │   ├── candidates.py
│   │   ├── pipeline.py
│   │   └── matching.py
│   ├── modules/             # Бизнес-логика
│   │   ├── auth/
│   │   ├── users/
│   │   ├── vacancies/
│   │   ├── candidates/
│   │   ├── resume_parser/
│   │   ├── ai_screening/
│   │   ├── pipeline/
│   │   ├── integrations/
│   │   ├── notifications/
│   │   └── storage/
│   └── utils/               # Утилиты
├── alembic/                 # Database migrations
├── tests/                   # Pytest tests
├── requirements.txt
└── README.md
```

## Основные зависимости

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.14
alembic>=1.12.0
psycopg2-binary>=2.9.9
redis>=5.0.0
rq>=1.15.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
openai>=1.3.0
langchain>=0.1.0
pgvector>=0.2.0
minio>=7.2.0
pdfminer.six>=20221105
python-docx>=1.1.0
pillow>=10.1.0
pytesseract>=0.3.10
pytest>=7.4.0
httpx>=0.25.0
```

## API Endpoints

### Authentication
- `POST /auth/login` — Вход
- `POST /auth/refresh` — Обновление токена
- `POST /auth/register` — Регистрация

### Vacancies
- `GET /vacancies` — Список вакансий
- `POST /vacancies` — Создание вакансии
- `GET /vacancies/{id}` — Детали вакансии
- `PUT /vacancies/{id}` — Обновление вакансии
- `DELETE /vacancies/{id}` — Удаление вакансии
- `POST /vacancies/{id}/generate` — AI-генерация описания

### Candidates
- `GET /candidates` — Список кандидатов (+ фильтры)
- `POST /candidates/upload` — Загрузка резюме
- `GET /candidates/{id}` — Карточка кандидата
- `PUT /candidates/{id}` — Обновление кандидата
- `POST /candidates/{id}/move-stage` — Перемещение по этапу

### Matching
- `GET /vacancies/{id}/matches` — Список совпадений для вакансии
- `POST /matching/calculate` — Пересчёт match score

### Pipeline
- `GET /pipeline/{vacancy_id}` — Воронка вакансии
- `POST /pipeline/move` — Перемещение кандидата

## Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
alembic upgrade head

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Тестирование

```bash
pytest
pytest --cov=app tests/
```
