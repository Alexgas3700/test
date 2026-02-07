# Быстрый старт VK Content Workflow

Это краткое руководство поможет вам запустить VK Content Workflow за 10 минут.

## Шаг 1: Подготовка (2 минуты)

### Что вам понадобится:

- ✅ Docker и Docker Compose установлены
- ✅ VK аккаунт с доступом к группе
- ✅ 10 минут свободного времени

### Проверка Docker:

```bash
docker --version
docker-compose --version
```

Если Docker не установлен:
- **Linux**: `curl -fsSL https://get.docker.com | sh`
- **Mac**: Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Windows**: Скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Шаг 2: Получение VK токена (3 минуты)

### Вариант A: Токен для группы (рекомендуется)

1. Откройте вашу группу VK
2. Перейдите в **Управление** → **Работа с API**
3. Нажмите **Создать ключ**
4. Выберите права:
   - ✅ Управление сообществом
   - ✅ Фотографии
   - ✅ Видеозаписи
5. Скопируйте токен

### Вариант B: Токен приложения

1. Перейдите на https://vk.com/apps?act=manage
2. Создайте **Standalone-приложение**
3. Получите **Client ID** и **Client Secret**
4. Получите токен через OAuth

### Получение ID группы:

Из URL группы:
- `https://vk.com/club123456` → ID = `-123456`
- `https://vk.com/public123456` → ID = `-123456`

**Важно**: ID группы должен быть отрицательным!

## Шаг 3: Настройка проекта (2 минуты)

```bash
# 1. Клонируйте или скачайте проект
git clone <repository-url>
cd vk-content-workflow

# 2. Создайте файл конфигурации
cp .env.example .env

# 3. Отредактируйте .env файл
nano .env  # или любой другой редактор
```

### Минимальная конфигурация в .env:

```bash
# VK Configuration
VK_ACCESS_TOKEN=your_vk_access_token_here
VK_GROUP_ID=-123456789

# n8n Configuration
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=ChangeMeToSecurePassword

# Database
DB_PASSWORD=ChangeThisPassword123
```

**Замените**:
- `your_vk_access_token_here` → ваш токен из Шага 2
- `123456789` → ID вашей группы
- `ChangeMeToSecurePassword` → надежный пароль
- `ChangeThisPassword123` → пароль для БД

## Шаг 4: Запуск (1 минута)

```bash
# Запустите все сервисы
docker-compose up -d

# Проверьте статус
docker-compose ps

# Дождитесь запуска (30-60 секунд)
docker-compose logs -f n8n
```

Когда увидите сообщение `Editor is now accessible via:`, нажмите Ctrl+C.

## Шаг 5: Настройка n8n (2 минуты)

### 5.1 Откройте n8n

Перейдите в браузере: http://localhost:5678

Логин: `admin` (из .env)
Пароль: тот что указали в .env

### 5.2 Импортируйте workflow

1. Нажмите **Workflows** (слева)
2. Нажмите **Import from File**
3. Выберите файл `vk-content-workflow.json`
4. Нажмите **Import**

### 5.3 Настройте VK credentials

1. Откройте импортированный workflow
2. Нажмите на узел **Create VK Post**
3. В поле **Credentials** нажмите **Create New**
4. Выберите **VK OAuth2 API**
5. Заполните:
   - **Name**: VK OAuth2 API
   - **Access Token**: ваш токен из Шага 2
6. Нажмите **Save**

### 5.4 Активируйте workflow

1. В правом верхнем углу переключите **Inactive** → **Active**
2. Workflow теперь работает!

## Шаг 6: Тестирование (2 минуты)

### Получите webhook URL:

1. В workflow нажмите на узел **Webhook Trigger**
2. Скопируйте **Production URL**
3. Он будет выглядеть как: `http://localhost:5678/webhook/create-vk-post`

### Отправьте тестовый пост:

```bash
curl -X POST http://localhost:5678/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "🎉 Мой первый автоматический пост из n8n!",
    "from_group": 1
  }'
```

**Замените** `-123456789` на ID вашей группы!

### Проверьте результат:

1. Откройте вашу группу VK
2. Вы должны увидеть новый пост!
3. В n8n откройте **Executions** → посмотрите результат выполнения

## Готово! 🎉

Ваш VK Content Workflow работает!

## Что дальше?

### Публикация с изображением:

```bash
curl -X POST http://localhost:5678/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Пост с фото",
    "attachments": ["photo-123456789_456239017"],
    "from_group": 1
  }'
```

### Отложенная публикация:

```bash
curl -X POST http://localhost:5678/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Этот пост будет опубликован завтра",
    "publish_date": "2026-02-08T12:00:00Z",
    "from_group": 1
  }'
```

### Пост с хэштегами:

```bash
curl -X POST http://localhost:5678/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Пост с хэштегами",
    "hashtags": ["автоматизация", "n8n", "vk"],
    "from_group": 1
  }'
```

## Полезные команды

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Обновление
docker-compose pull
docker-compose up -d
```

## Дополнительные возможности

### Расширенный workflow

Импортируйте `vk-content-advanced-workflow.json` для:
- ✨ AI-генерации контента (требует OpenAI API)
- 🖼️ Автоматической обработки изображений
- ✅ Модерации контента
- 📊 Расширенной аналитики

### База данных (опционально)

Для логирования постов:

1. Откройте workflow
2. Включите узел **Log to Database**
3. Настройте PostgreSQL credentials:
   - Host: `postgres`
   - Database: `n8n`
   - User: `n8n`
   - Password: из .env

### Интеграции

Смотрите `examples/integration-examples.md` для:
- 📊 Google Sheets
- 📰 RSS ленты
- 🤖 Telegram боты
- 🎨 AI генерация контента
- И многое другое!

## Troubleshooting

### n8n не открывается

```bash
# Проверьте логи
docker-compose logs n8n

# Проверьте, что порт свободен
netstat -tulpn | grep 5678
```

### Ошибка при публикации

1. Проверьте токен VK
2. Проверьте ID группы (должен быть отрицательным)
3. Проверьте права токена
4. Посмотрите логи в n8n → Executions

### База данных не работает

```bash
# Проверьте PostgreSQL
docker-compose exec postgres pg_isready

# Перезапустите
docker-compose restart postgres
```

## Получить помощь

- 📖 Полная документация: `README.md`
- 🚀 Развертывание: `DEPLOYMENT.md`
- 💡 Примеры: `examples/`
- 🐛 Issues: создайте issue в репозитории

## Безопасность

⚠️ **Важно для production**:

1. Измените пароли в `.env`
2. Используйте HTTPS (настройте Nginx)
3. Ограничьте доступ к webhook
4. Регулярно делайте резервные копии
5. Обновляйте Docker образы

```bash
# Для production используйте:
docker-compose --profile production up -d
```

---

**Поздравляем! Вы успешно запустили VK Content Workflow!** 🚀

Если возникли вопросы, изучите полную документацию в `README.md` или создайте issue.
