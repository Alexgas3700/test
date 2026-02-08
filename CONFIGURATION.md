# Руководство по конфигурации

Это руководство поможет вам настроить workflow для управления Telegram каналом.

## 📋 Содержание

- [Быстрый старт](#быстрый-старт)
- [Telegram настройки](#telegram-настройки)
- [RSS ленты](#rss-ленты)
- [Расписание](#расписание)
- [Шаблоны сообщений](#шаблоны-сообщений)
- [Webhook](#webhook)
- [Фильтры и ограничения](#фильтры-и-ограничения)

## 🚀 Быстрый старт

1. Скопируйте `config.example.json` в `config.json`
2. Заполните обязательные поля
3. Импортируйте workflow в n8n
4. Обновите узлы Configuration значениями из config.json

## 🤖 Telegram настройки

### Получение Bot Token

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

```json
{
  "telegram": {
    "botToken": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
  }
}
```

### Получение Channel ID

#### Для публичных каналов:
```json
{
  "channelId": "@your_channel_name"
}
```

#### Для приватных каналов:

1. Добавьте бота [@userinfobot](https://t.me/userinfobot) в канал
2. Перешлите любое сообщение из канала боту
3. Скопируйте ID (формат: `-1001234567890`)

```json
{
  "channelId": "-1001234567890"
}
```

### Admin Chat ID

Для получения вашего Chat ID:

1. Напишите [@userinfobot](https://t.me/userinfobot)
2. Скопируйте ваш ID

```json
{
  "adminChatId": "123456789"
}
```

### Настройки форматирования

```json
{
  "parseMode": "Markdown",  // или "HTML", "MarkdownV2"
  "disableWebPagePreview": false  // true - отключить превью ссылок
}
```

## 📰 RSS ленты

### Добавление RSS источников

```json
{
  "rss": {
    "feeds": [
      {
        "name": "Название ленты",
        "url": "https://example.com/rss",
        "enabled": true,
        "maxAge": 24  // Публиковать новости не старше 24 часов
      }
    ]
  }
}
```

### Популярные RSS источники

**Новости:**
- Lenta.ru: `https://lenta.ru/rss`
- RBC: `https://rssexport.rbc.ru/rbcnews/news/30/full.rss`
- Meduza: `https://meduza.io/rss/all`

**Технологии:**
- Habr: `https://habr.com/ru/rss/all/`
- VC.ru: `https://vc.ru/rss`

**Блоги:**
- Medium: `https://medium.com/feed/@username`

### RSS2JSON API

Для работы с RSS используется сервис RSS2JSON:

1. Зарегистрируйтесь на [rss2json.com](https://rss2json.com/)
2. Получите API ключ
3. Добавьте в конфигурацию:

```json
{
  "rss": {
    "rss2jsonApiKey": "your_api_key_here"
  }
}
```

**Бесплатный план:**
- 10,000 запросов/день
- Достаточно для большинства случаев

## ⏰ Расписание

### Cron выражения

```json
{
  "schedule": {
    "cronExpression": "0 9,12,18 * * *",
    "timezone": "Europe/Moscow",
    "enabled": true
  }
}
```

### Примеры cron выражений

| Выражение | Описание |
|-----------|----------|
| `0 9,12,18 * * *` | 3 раза в день: 9:00, 12:00, 18:00 |
| `0 */2 * * *` | Каждые 2 часа |
| `0 10 * * 1-5` | Будни в 10:00 |
| `0 8 * * 1` | Каждый понедельник в 8:00 |
| `0 0 * * *` | Каждый день в полночь |
| `*/30 * * * *` | Каждые 30 минут |

### Генератор cron

Используйте [crontab.guru](https://crontab.guru/) для создания cron выражений.

### Часовые пояса

Популярные часовые пояса:

```
Europe/Moscow    - Москва (UTC+3)
Europe/Kiev      - Киев (UTC+2)
Asia/Almaty      - Алматы (UTC+6)
Europe/Minsk     - Минск (UTC+3)
Asia/Tashkent    - Ташкент (UTC+5)
```

Полный список: [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## 📝 Шаблоны сообщений

### Базовый шаблон

```json
{
  "messages": {
    "postTemplate": "## 📰 {{ title }}\n\n{{ description }}\n\n🔗 [Читать полностью]({{ link }})\n\n{{ hashtags }}"
  }
}
```

### Доступные переменные

| Переменная | Описание |
|------------|----------|
| `{{ title }}` | Заголовок статьи |
| `{{ description }}` | Описание/краткое содержание |
| `{{ link }}` | Ссылка на оригинал |
| `{{ pubDate }}` | Дата публикации |
| `{{ hashtags }}` | Хэштеги из конфига |
| `{{ date }}` | Текущая дата |

### Примеры шаблонов

**Минималистичный:**
```
{{ title }}

{{ description }}

{{ link }}
```

**С эмодзи:**
```
📰 {{ title }}

📝 {{ description }}

🔗 Источник: {{ link }}

🏷️ {{ hashtags }}
```

**Формальный:**
```
**{{ title }}**

{{ description }}

Подробнее: {{ link }}

Опубликовано: {{ pubDate }}
```

### Ежедневное приветствие

```json
{
  "messages": {
    "dailyGreeting": {
      "enabled": true,
      "time": "09:00",
      "template": "📢 Доброе утро! Сегодня {{ date }}\n\n{{ message }}"
    }
  }
}
```

Примеры сообщений:
- "Желаем продуктивного дня! 💪"
- "Начинаем новый день с хороших новостей!"
- "Доброе утро! Вот что интересного сегодня:"

## 🌐 Webhook

### Базовая настройка

```json
{
  "webhook": {
    "enabled": true,
    "path": "/webhook/telegram-webhook"
  }
}
```

URL webhook: `https://your-n8n-instance.com/webhook/telegram-webhook`

### Аутентификация

```json
{
  "webhook": {
    "authentication": {
      "enabled": true,
      "type": "bearer",
      "token": "your_secret_token_here"
    }
  }
}
```

Пример запроса с аутентификацией:

```bash
curl -X POST https://your-n8n-instance.com/webhook/telegram-webhook \
  -H "Authorization: Bearer your_secret_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "channelId": "@your_channel",
    "text": "Сообщение через webhook"
  }'
```

### Формат данных

#### Текстовое сообщение:

```json
{
  "channelId": "@your_channel",
  "text": "Текст сообщения",
  "type": "text"
}
```

#### Сообщение с фото:

```json
{
  "channelId": "@your_channel",
  "message": "Подпись к фото",
  "type": "photo",
  "media": "https://example.com/image.jpg"
}
```

#### Отложенная публикация:

```json
{
  "channelId": "@your_channel",
  "text": "Сообщение",
  "type": "text",
  "scheduledTime": "2026-02-09T12:00:00Z"
}
```

## 🔧 Настройки публикации

```json
{
  "posting": {
    "delayBetweenPosts": 5,      // Задержка в секундах
    "maxPostsPerRun": 10,         // Макс. постов за раз
    "filterDuplicates": true      // Фильтр дубликатов
  }
}
```

### Рекомендации:

- **delayBetweenPosts**: 3-10 секунд (защита от спама)
- **maxPostsPerRun**: 5-15 постов (не перегружать канал)
- **filterDuplicates**: всегда `true`

## 🎯 Фильтры и ограничения

### Фильтрация по ключевым словам

```json
{
  "filters": {
    "keywords": {
      "include": ["технологии", "наука", "AI"],
      "exclude": ["реклама", "спам", "казино"]
    }
  }
}
```

- **include**: Публиковать только если содержит эти слова (пусто = все)
- **exclude**: Не публиковать если содержит эти слова

### Ограничения по длине

```json
{
  "filters": {
    "minContentLength": 50,    // Минимум символов
    "maxContentLength": 4000   // Максимум символов (лимит Telegram: 4096)
  }
}
```

## 🔔 Уведомления

```json
{
  "notifications": {
    "errorNotifications": true,     // Уведомления об ошибках
    "successNotifications": false,  // Уведомления об успехе
    "dailyReport": true,           // Ежедневный отчет
    "reportTime": "20:00"          // Время отчета
  }
}
```

### Типы уведомлений:

1. **Ошибки** - отправляются сразу при возникновении
2. **Успех** - после каждой публикации (может быть много)
3. **Ежедневный отчет** - статистика за день

## 🔐 Хэштеги

```json
{
  "hashtags": [
    "#новости",
    "#telegram",
    "#автоматизация"
  ]
}
```

Хэштеги автоматически добавляются к каждому посту.

**Рекомендации:**
- 3-5 хэштегов на пост
- Используйте релевантные теги
- Не злоупотребляйте

## ⚙️ Расширенные настройки

```json
{
  "advanced": {
    "retryOnError": true,    // Повторять при ошибке
    "maxRetries": 3,         // Количество попыток
    "retryDelay": 5,         // Задержка между попытками (сек)
    "logLevel": "info"       // debug, info, warn, error
  }
}
```

## 📊 Примеры конфигураций

### Новостной канал

```json
{
  "telegram": {
    "channelId": "@news_channel",
    "parseMode": "Markdown"
  },
  "schedule": {
    "cronExpression": "0 */2 * * *"
  },
  "posting": {
    "delayBetweenPosts": 10,
    "maxPostsPerRun": 5
  },
  "hashtags": ["#новости", "#актуально"]
}
```

### Технологический блог

```json
{
  "telegram": {
    "channelId": "@tech_blog",
    "parseMode": "HTML"
  },
  "schedule": {
    "cronExpression": "0 10,16 * * 1-5"
  },
  "filters": {
    "keywords": {
      "include": ["технологии", "программирование", "AI"]
    }
  },
  "hashtags": ["#tech", "#programming", "#AI"]
}
```

### Развлекательный канал

```json
{
  "telegram": {
    "channelId": "@fun_channel",
    "disableWebPagePreview": true
  },
  "schedule": {
    "cronExpression": "0 12,18,21 * * *"
  },
  "posting": {
    "delayBetweenPosts": 3,
    "maxPostsPerRun": 15
  },
  "hashtags": ["#развлечения", "#интересное"]
}
```

## ✅ Чек-лист перед запуском

- [ ] Bot Token получен и добавлен в credentials
- [ ] Бот добавлен в канал как администратор
- [ ] Channel ID указан корректно
- [ ] Admin Chat ID настроен для уведомлений
- [ ] RSS ленты проверены и доступны
- [ ] Расписание настроено под ваш часовой пояс
- [ ] Шаблоны сообщений кастомизированы
- [ ] Хэштеги подобраны
- [ ] Фильтры настроены (если нужны)
- [ ] Workflow импортирован в n8n
- [ ] Тестовый запуск выполнен успешно
- [ ] Workflow активирован

## 🆘 Помощь

Если что-то не работает:

1. Проверьте логи в n8n (кнопка "Executions")
2. Убедитесь, что все credentials настроены
3. Проверьте права бота в канале
4. Изучите раздел "Устранение неполадок" в README.md

---

**Готово! Ваш Telegram канал готов к автоматизации! 🎉**
