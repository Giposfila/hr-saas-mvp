# HR SaaS Frontend

Next.js frontend для платформы HR-автоматизации.

## Структура проекта

```
frontend/
├── app/                     # Next.js App Router
│   ├── layout.tsx
│   ├── page.tsx             # Dashboard
│   ├── login/
│   ├── vacancies/
│   ├── candidates/
│   ├── pipeline/
│   └── settings/
├── components/              # React компоненты
│   ├── ui/                  # shadcn/ui компоненты
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── TopBar.tsx
│   │   └── Layout.tsx
│   ├── vacancies/
│   ├── candidates/
│   └── pipeline/
├── lib/                     # Утилиты
│   ├── api.ts               # API client
│   ├── utils.ts
│   └── constants.ts
├── hooks/                   # Custom hooks
├── store/                   # Zustand store
├── types/                   # TypeScript types
├── public/                  # Static files
├── styles/
│   └── globals.css
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## Основные зависимости

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.2.0",
    "@tanstack/react-query": "^5.8.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.0",
    "@radix-ui/react-*": "latest",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "recharts": "^2.10.0",
    "framer-motion": "^10.16.0",
    "react-beautiful-dnd": "^13.1.1",
    "lucide-react": "^0.292.0"
  }
}
```

## Страницы

### `/login`
Авторизация пользователя

### `/dashboard`
Главная панель:
- Карточки: "Новые отклики", "В работе", "Лучшие кандидаты"
- Графики и статистика

### `/vacancies`
Список вакансий с фильтрами и поиском

### `/vacancies/[id]`
Страница вакансии:
- Описание
- AI-генерация текста
- Список кандидатов с match score

### `/candidates`
Таблица кандидатов с фильтрацией

### `/candidates/[id]`
Карточка кандидата:
- Табы: Резюме / Структурированное / Навыки / Опыт / AI Summary
- Блок рекомендаций от AI
- Кнопки действий

### `/pipeline/[vacancy_id]`
Канбан-воронка подбора (drag-and-drop)

### `/settings`
Профиль, токены, интеграции

## UI-Kit (shadcn/ui)

Используемые компоненты:
- Button, Input, Textarea
- Card, Table, Dialog
- Tabs, Select, Checkbox
- Avatar, Badge, Progress
- Tooltip, Skeleton
- DropdownMenu, Popover

## State Management

```typescript
// Zustand store example
import create from 'zustand'

interface AppState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
}

const useAppStore = create<AppState>((set) => ({
  sidebarCollapsed: false,
  toggleSidebar: () => set((state) => ({ 
    sidebarCollapsed: !state.sidebarCollapsed 
  }))
}))
```

## API Integration

```typescript
// React Query example
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

const { data, isLoading } = useQuery({
  queryKey: ['vacancies'],
  queryFn: () => api.get('/vacancies')
})
```

## Запуск

```bash
# Установка зависимостей
npm install

# Development
npm run dev

# Production build
npm run build
npm start

# Linting
npm run lint
```

## Дизайн-система

### Цвета
- Primary: Фиолетовый/Синий (#6366F1)
- Background: #F9FAFB
- Card: #FFFFFF
- Border: #E5E7EB
- Text: #111827 / #6B7280

### Типографика
- Font: Inter / Geist Sans
- Heading: 600-700 weight
- Body: 400 weight

### Spacing
- Base: 4px (rem unit)
- Grid: 8px columns

## Адаптивность

- Desktop: 1440px+
- Tablet: 768px - 1439px
- Mobile: 375px - 767px
