# GitHub Pages Setup Instructions

## Настройка GitHub Pages

### 1. Включите GitHub Pages в настройках репозитория

1. Перейдите в настройки репозитория: https://github.com/Giposfila/hr-saas-mvp/settings
2. В боковом меню найдите раздел **Pages**
3. В секции **Build and deployment**:
   - **Source**: выберите **GitHub Actions**
4. Нажмите **Save**

### 2. Проверьте деплой

После включения GitHub Pages:

1. Перейдите на вкладку **Actions**: https://github.com/Giposfila/hr-saas-mvp/actions
2. Вы увидите запущенный workflow "Deploy to GitHub Pages"
3. Дождитесь завершения (обычно 2-5 минут)

### 3. Откройте ваш сайт

После успешного деплоя ваш сайт будет доступен по адресу:

**https://giposfila.github.io/hr-saas-mvp/**

## Что было настроено

### Файлы конфигурации

1. **`frontend/next.config.js`**
   - Добавлен `output: 'export'` для статического экспорта
   - Добавлен `basePath: '/hr-saas-mvp'` для подкаталога GitHub Pages
   - Добавлен `images.unoptimized: true` (т.к. GitHub Pages не поддерживает оптимизацию Next.js)

2. **`.github/workflows/deploy.yml`**
   - GitHub Actions workflow для автоматического деплоя
   - Запускается при каждом push в ветку `main`
   - Устанавливает зависимости, собирает и деплоит приложение

3. **`.nojekyll`**
   - Пустой файл, который говорит GitHub Pages не игнорировать файлы Next.js

## Автоматические обновления

Теперь при каждом push в ветку `main`:
1. GitHub Actions автоматически соберёт приложение
2. Опубликует новую версию на GitHub Pages
3. Сайт будет обновлён через 2-5 минут

## Важные ограничения

⚠️ **Обратите внимание:**

1. **Backend API** не будет работать на GitHub Pages
   - GitHub Pages поддерживает только статические файлы
   - Для backend используйте: Heroku, Railway, Render, Vercel, AWS, DigitalOcean

2. **Оптимизация изображений Next.js** отключена
   - Изображения будут отдаваться в исходном размере

3. **Server-Side Rendering (SSR)** не работает
   - Используется только Static Site Generation (SSG)

## Рекомендации для production

Для полноценного развёртывания рекомендую:

1. **Frontend**: GitHub Pages (бесплатно) или Vercel/Netlify
2. **Backend**: 
   - **Heroku** - простой деплой
   - **Railway** - бесплатный тиер
   - **Render** - бесплатный тиер
   - **AWS/GCP** - больше контроля

## Проблемы?

Если сайт не работает:

1. Проверьте логи в Actions: https://github.com/Giposfila/hr-saas-mvp/actions
2. Убедитесь, что GitHub Pages включён в настройках
3. Подождите 5-10 минут после первого деплоя
4. Очистите кэш браузера (Ctrl+Shift+Delete)
