# HR SaaS MVP — AI-Powered Recruitment Platform

## 🎯 Описание проекта

AI-платформа для автоматизации HR-процессов с функциями:
- Автоматический парсинг и анализ резюме
- AI-скрининг кандидатов с расчётом match score
- Визуальная воронка подбора (канбан)
- Умные рекомендации для рекрутеров

## 🏗️ Архитектура

```
hr-saas-mvp/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docker-compose.yml
└── README.md
```

## 🛠️ Технологический стек

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLModel + Alembic
- **Database:** PostgreSQL + pgvector
- **Cache/Queue:** Redis + RQ
- **Storage:** MinIO / S3
- **AI:** OpenAI API / Llama / Mistral
- **Testing:** Pytest, httpx

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **UI:** React 18 + TypeScript
- **Styling:** TailwindCSS + shadcn/ui
- **State:** Zustand / Jotai
- **Data Fetching:** TanStack Query (React Query)
- **Charts:** Recharts
- **Animations:** Framer Motion

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- MinIO (опционально для локальной разработки)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Полный стек (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Применение миграций
docker-compose exec backend alembic upgrade head
```

## 📁 Структура модулей

### Backend Modules
- `auth` — Аутентификация и авторизация
- `users` — Управление пользователями
- `vacancies` — Управление вакансиями
- `candidates` — Управление кандидатами
- `resume_parser` — Парсинг резюме
- `ai_screening` — AI-анализ и scoring
- `pipeline` — Воронка подбора
- `integrations` — Внешние интеграции
- `notifications` — Уведомления
- `storage` — Файловое хранилище

### Frontend Pages
- `/login` — Авторизация
- `/dashboard` — Главная панель
- `/vacancies` — Список вакансий
- `/vacancies/[id]` — Страница вакансии
- `/candidates` — Список кандидатов
- `/candidates/[id]` — Карточка кандидата
- `/pipeline/[vacancy_id]` — Канбан-воронка
- `/settings` — Настройки

## 🔄 AI-Pipeline

1. **Upload** → Загрузка резюме в S3/MinIO
2. **Parse** → Извлечение текста (PDF/DOCX/OCR)
3. **Extract** → LLM извлекает структурированные данные
4. **Embed** → Создание эмбеддингов резюме
5. **Match** → Сопоставление с вакансией (cosine similarity)
6. **Score** → Расчёт match score (0-100)
7. **Summary** → Генерация AI-саммари для HR

## 🎨 UI/UX Принципы

- **Минимализм:** Стиль Linear/Notion
- **Скорость:** Действия в 1-2 клика
- **Адаптивность:** 1440px → 768px → 375px
- **Обратная связь:** Skeleton loading, tooltips
- **Drag-and-drop:** Интуитивная работа с воронкой

## 🧪 Тестирование

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 📊 Критерии приёмки MVP

- ✅ Создание вакансии
- ✅ Загрузка резюме
- ✅ Автоматический парсинг и AI-анализ
- ✅ Отображение match score
- ✅ Drag-and-drop воронка
- ✅ AI summary на карточке кандидата
- ✅ Адаптивный UI
- ✅ Время отрисовки <200ms

## 🔐 Переменные окружения

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/hr_saas
REDIS_URL=redis://localhost:6379
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret-key
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 License

MIT License

## 👥 Авторы

Разработано для акселератора — проект AI-powered HR платформы
