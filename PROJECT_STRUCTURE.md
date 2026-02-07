# Структура проекта VK Content Workflow

## Обзор

Этот проект представляет собой полное решение для автоматизации создания и публикации контента в VKontakte с использованием n8n.

## Структура файлов

```
vk-content-workflow/
├── README.md                              # Основная документация
├── QUICKSTART.md                          # Быстрый старт (10 минут)
├── DEPLOYMENT.md                          # Руководство по развертыванию
├── PROJECT_STRUCTURE.md                   # Этот файл
│
├── .env.example                           # Шаблон конфигурации
├── .gitignore                             # Игнорируемые файлы
├── docker-compose.yml                     # Docker Compose конфигурация
│
├── vk-content-workflow.json              # Базовый workflow для n8n
├── vk-content-advanced-workflow.json     # Расширенный workflow
│
├── database/
│   └── schema.sql                        # SQL схема базы данных
│
├── scripts/
│   ├── backup.sh                         # Скрипт резервного копирования
│   ├── restore.sh                        # Скрипт восстановления
│   └── analytics.sh                      # Сбор аналитики из VK API
│
└── examples/
    ├── webhook-examples.md               # Примеры использования webhook
    └── integration-examples.md           # Примеры интеграций
```

## Описание файлов

### Документация

#### README.md
Основная документация проекта, включающая:
- Полное описание возможностей
- Требования и установка
- Настройка VK API и n8n
- Структура workflow
- API и параметры
- Примеры использования
- Troubleshooting
- Интеграции

#### QUICKSTART.md
Краткое руководство для быстрого старта:
- Пошаговая инструкция на 10 минут
- Получение VK токена
- Настройка и запуск
- Первый тестовый пост
- Базовые примеры

#### DEPLOYMENT.md
Подробное руководство по развертыванию:
- Развертывание с Docker и без
- Настройка VK API
- Импорт workflow
- Настройка credentials
- Production deployment
- Мониторинг и резервное копирование
- Troubleshooting

#### PROJECT_STRUCTURE.md
Описание структуры проекта и назначения файлов.

### Конфигурация

#### .env.example
Шаблон файла конфигурации со всеми доступными переменными окружения:
- VK API настройки
- n8n конфигурация
- База данных
- OpenAI (опционально)
- Уведомления (Telegram, Email, Slack)
- Настройки workflow
- Модерация контента
- Медиа-файлы
- Кэширование
- Логирование
- Безопасность
- Интеграции
- Аналитика
- Резервное копирование

#### docker-compose.yml
Docker Compose конфигурация для запуска всех сервисов:
- **n8n**: Основной сервис workflow automation
- **postgres**: База данных PostgreSQL
- **redis**: Кэш и очереди (опционально)
- **pgadmin**: Веб-интерфейс для управления БД (dev)
- **nginx**: Reverse proxy (production)
- **backup**: Сервис резервного копирования

Поддерживает профили:
- `dev` - разработка (с pgAdmin)
- `production` - продакшн (с Redis и Nginx)
- `backup` - резервное копирование

### Workflows

#### vk-content-workflow.json
Базовый workflow для публикации контента в VK:

**Узлы:**
1. **Schedule Trigger** - запуск по расписанию
2. **Webhook Trigger** - запуск через HTTP запрос
3. **Check Content** - валидация данных
4. **Process Data** - обработка и подготовка
5. **Create VK Post** - публикация в VK
6. **Log to Database** - сохранение в БД (опционально)
7. **Notify Success/Error** - уведомления

**Возможности:**
- Публикация текстовых постов
- Поддержка вложений (фото, видео, ссылки)
- Хэштеги
- Отложенная публикация
- Геолокация
- Настройки поста (комментарии, уведомления, реклама)

#### vk-content-advanced-workflow.json
Расширенный workflow с дополнительными возможностями:

**Дополнительные узлы:**
1. **AI Content Generator** - генерация контента с OpenAI
2. **Content Moderation** - модерация и валидация
3. **Download Image** - загрузка изображений
4. **Upload to VK** - загрузка медиа в VK
5. **Extract Post Data** - извлечение данных
6. **Webhook Response** - ответ на webhook запрос

**Дополнительные возможности:**
- AI-генерация контента
- Автоматическая обработка изображений
- Расширенная модерация
- Детальное логирование
- REST API ответы

### База данных

#### database/schema.sql
Полная SQL схема базы данных PostgreSQL:

**Таблицы:**
1. **vk_posts** - опубликованные посты
2. **vk_posts_errors** - ошибки публикации
3. **vk_scheduled_posts** - запланированные посты
4. **vk_posts_metrics** - метрики постов (история)
5. **vk_groups** - настройки групп VK
6. **vk_post_templates** - шаблоны постов
7. **vk_media** - кэш медиа-файлов

**Представления (Views):**
- `vk_posts_stats_30d` - статистика за 30 дней
- `vk_top_posts` - топ постов по вовлеченности
- `vk_errors_summary` - сводка ошибок
- `vk_upcoming_posts` - предстоящие публикации

**Функции:**
- `get_group_stats()` - получение статистики группы
- `cleanup_old_records()` - очистка старых записей
- `archive_old_posts()` - архивация старых постов

**Триггеры:**
- Автоматическое обновление `updated_at`

### Скрипты

#### scripts/backup.sh
Скрипт автоматического резервного копирования:
- Создание дампа базы данных
- Сжатие резервной копии
- Удаление старых копий
- Опционально: загрузка в облако (S3)
- Опционально: уведомления (Telegram)

**Использование:**
```bash
# Вручную
./scripts/backup.sh

# Через Docker
docker-compose run --rm backup

# По расписанию (cron)
0 2 * * * /path/to/backup.sh
```

#### scripts/restore.sh
Скрипт восстановления из резервной копии:
- Проверка файла резервной копии
- Создание safety backup перед восстановлением
- Восстановление базы данных
- Верификация восстановления

**Использование:**
```bash
./scripts/restore.sh /backups/vk_content_20260207_120000.sql.gz
```

#### scripts/analytics.sh
Скрипт сбора аналитики из VK API:
- Получение метрик постов (лайки, комментарии, репосты, просмотры)
- Обновление базы данных
- Сохранение истории метрик
- Генерация отчетов
- Опционально: уведомления

**Использование:**
```bash
# Вручную
./scripts/analytics.sh

# По расписанию (cron)
0 */6 * * * /path/to/analytics.sh
```

### Примеры

#### examples/webhook-examples.md
Примеры использования webhook API:

**Содержание:**
- Базовые примеры (curl)
- Примеры на Python
- Примеры на Node.js
- Примеры на PHP
- Примеры с авторизацией
- Обработка ошибок
- Интеграция с другими сервисами
- Тестирование

**Языки программирования:**
- Bash (curl)
- Python
- Node.js (JavaScript)
- PHP
- Google Apps Script

#### examples/integration-examples.md
Примеры интеграций с различными сервисами:

**Интеграции:**
1. **Google Sheets** - публикация из таблиц
2. **RSS Feed** - автопубликация новостей
3. **OpenAI** - AI-генерация контента
4. **Telegram** - публикация из Telegram канала
5. **Airtable** - контент-календарь
6. **WordPress** - автопубликация статей
7. **Instagram** - кросспостинг
8. **Notion** - контент-менеджмент
9. **Email (IMAP)** - публикация из email
10. **Zapier/Make** - универсальный webhook

Каждая интеграция включает:
- Описание use case
- JSON конфигурацию workflow
- Пошаговую настройку
- Примеры кода

## Workflow архитектура

### Базовый workflow

```
┌─────────────────┐
│ Schedule/Webhook│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Content   │
│  (Validation)   │
└────┬────────────┘
     │
     ├─ Valid ──►┌──────────────┐
     │           │Process Data  │
     │           └──────┬───────┘
     │                  │
     │                  ▼
     │           ┌──────────────┐
     │           │Create VK Post│
     │           └──────┬───────┘
     │                  │
     │                  ├──►┌──────────┐
     │                  │   │Log to DB │
     │                  │   └──────────┘
     │                  │
     │                  └──►┌──────────┐
     │                      │ Notify   │
     │                      └──────────┘
     │
     └─ Invalid ─►┌──────────┐
                  │Set Error │
                  └────┬─────┘
                       │
                       ▼
                  ┌──────────┐
                  │  Notify  │
                  │  Error   │
                  └──────────┘
```

### Расширенный workflow

Добавляет:
- AI Content Generation
- Image Processing
- Content Moderation
- Advanced Analytics
- Webhook Responses

## Технологический стек

### Backend
- **n8n** - Workflow automation platform
- **PostgreSQL** - Реляционная база данных
- **Redis** - Кэш и очереди (опционально)

### API
- **VK API** v5.131 - Публикация контента
- **OpenAI API** - AI-генерация (опционально)

### Инфраструктура
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация контейнеров
- **Nginx** - Reverse proxy (production)

### Мониторинг (опционально)
- **Prometheus** - Сбор метрик
- **Grafana** - Визуализация

## Использование

### Быстрый старт
```bash
# 1. Настройка
cp .env.example .env
nano .env

# 2. Запуск
docker-compose up -d

# 3. Доступ
open http://localhost:5678
```

### Development
```bash
docker-compose --profile dev up -d
```

### Production
```bash
docker-compose --profile production up -d
```

## Масштабирование

### Вертикальное
- Увеличение ресурсов контейнеров
- Оптимизация базы данных
- Настройка connection pooling

### Горизонтальное
- Queue mode с Redis
- Несколько worker instances
- Load balancing с Nginx

## Безопасность

### Рекомендации
1. Используйте сильные пароли
2. Включите HTTPS
3. Ограничьте доступ к webhook
4. Регулярное резервное копирование
5. Обновление зависимостей
6. Мониторинг логов

### Защита данных
- Токены в environment variables
- Шифрование credentials в n8n
- SSL/TLS для соединений
- Firewall правила

## Мониторинг

### Healthchecks
- n8n: `/healthz`
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f n8n

# Последние N строк
docker-compose logs --tail=100 n8n
```

### Метрики
- Количество публикаций
- Успешность публикаций
- Время выполнения workflow
- Использование ресурсов

## Резервное копирование

### Автоматическое
```bash
# Настройка cron
0 2 * * * docker-compose run --rm backup
```

### Ручное
```bash
docker-compose run --rm backup
```

### Восстановление
```bash
./scripts/restore.sh /backups/backup_file.sql.gz
```

## Обновление

### n8n
```bash
docker-compose pull n8n
docker-compose up -d n8n
```

### Workflows
1. Экспорт текущего (резервная копия)
2. Импорт новой версии
3. Тестирование

## Поддержка

### Документация
- README.md - полная документация
- QUICKSTART.md - быстрый старт
- DEPLOYMENT.md - развертывание
- examples/ - примеры использования

### Ресурсы
- [n8n Documentation](https://docs.n8n.io/)
- [VK API Documentation](https://dev.vk.com/reference)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Помощь
- Создайте issue в репозитории
- Проверьте Troubleshooting в README.md
- Изучите логи: `docker-compose logs`

## Лицензия

MIT License

## Авторы

Разработано для автоматизации контента в VKontakte с использованием n8n.

---

**Версия:** 1.0.0  
**Дата:** 2026-02-07
