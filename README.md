# VK Content Creation Workflow для n8n

Полнофункциональное решение для автоматизации создания и публикации контента в VKontakte через n8n.

## 🚀 Быстрый старт

**Хотите начать прямо сейчас?** Читайте [QUICK_START.md](./QUICK_START.md) - запуститесь за 5 минут!

## 📋 Что входит в проект

### Workflow файлы

1. **vk-content-workflow.json** - Базовый workflow
   - Автоматическая публикация по расписанию
   - Валидация контента
   - Обработка ошибок
   - Логирование результатов

2. **vk-advanced-workflow.json** - Продвинутый workflow
   - Интеграция с OpenAI для генерации контента
   - Fallback на шаблоны при недоступности AI
   - Расширенная валидация
   - Детальное логирование

### Документация

1. **QUICK_START.md** - Быстрый старт за 5 минут
2. **VK_WORKFLOW_README.md** - Полная документация
3. **README.md** (этот файл) - Обзор проекта

### Конфигурация

1. **vk-workflow-config.example.json** - Пример конфигурации
2. **database-schema.sql** - SQL схема для логирования

### Утилиты

1. **vk_api_tester.py** - Скрипт для тестирования VK API

## ✨ Возможности

### Базовые функции

- ✅ Автоматическая публикация контента по расписанию
- ✅ Генерация контента из шаблонов
- ✅ Валидация перед публикацией
- ✅ Обработка ошибок
- ✅ Поддержка текста и вложений (фото, видео)

### Продвинутые функции

- 🤖 Интеграция с AI (OpenAI, Claude) для генерации уникального контента
- 📊 Логирование в базу данных (PostgreSQL, MySQL, SQLite)
- 📈 Сбор статистики опубликованных постов
- 📧 Уведомления о результатах (Email, Telegram, Slack)
- 🔄 Retry механизм при ошибках
- 🎯 Таргетинг по темам и категориям
- 📅 Планирование публикаций на будущее

## 🎯 Кому подходит

- **SMM-специалистам** - автоматизация рутинных публикаций
- **Контент-менеджерам** - управление контентом в VK
- **Маркетологам** - регулярные публикации и аналитика
- **Владельцам бизнеса** - автоматическое присутствие в соцсетях
- **Блогерам** - регулярный контент для аудитории

## 📦 Установка

### Требования

- n8n (self-hosted или cloud)
- VK аккаунт с правами администратора группы
- VK Access Token с правами: `wall`, `photos`, `groups`

### Опционально

- PostgreSQL/MySQL для логирования
- OpenAI API ключ для AI генерации контента
- Email/Telegram для уведомлений

### Шаги установки

1. **Клонируйте репозиторий или скачайте файлы**

2. **Получите VK Access Token**
   ```
   https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,photos,groups&response_type=token&v=5.131
   ```

3. **Импортируйте workflow в n8n**
   - Откройте n8n
   - Import from File → выберите `vk-content-workflow.json`

4. **Настройте credentials**
   - Добавьте VK Access Token в credentials

5. **Настройте параметры**
   - Откройте узел "Generate Content"
   - Укажите ваш `owner_id`

6. **Тестируйте!**
   - Запустите workflow вручную
   - Проверьте публикацию в VK

Подробная инструкция: [QUICK_START.md](./QUICK_START.md)

## 🧪 Тестирование

### Использование Python тестера

```bash
# Установите зависимости
pip install requests

# Запустите тестер
python vk_api_tester.py YOUR_ACCESS_TOKEN

# Или интерактивно
python vk_api_tester.py
```

Тестер проверит:
- ✅ Валидность токена
- ✅ Права доступа
- ✅ Список доступных групп
- ✅ Возможность публикации
- ✅ Получение статистики

## 📖 Использование

### Базовый сценарий

1. Workflow запускается по расписанию (каждые 6 часов)
2. Генерируется контент из шаблонов
3. Контент валидируется
4. Публикуется в VK
5. Логируется результат

### С AI генерацией

1. Workflow запускается по расписанию
2. Выбирается случайная тема
3. OpenAI генерирует уникальный контент
4. Контент валидируется
5. Публикуется в VK
6. Собирается статистика

### Кастомизация

**Изменить расписание:**
```javascript
// В узле Schedule Trigger
Interval: Hours
Value: 4 // Каждые 4 часа
```

**Добавить свои шаблоны:**
```javascript
// В узле Generate Content
const contentTemplates = [
  "Ваш текст 1 #хештег1",
  "Ваш текст 2 #хештег2"
];
```

**Добавить изображение:**
```javascript
// В узле Generate Content
const attachments = "photo-123456_789012";
```

## 🔧 Конфигурация

### Основные параметры

```json
{
  "vk_config": {
    "access_token": "YOUR_TOKEN",
    "owner_id": "-YOUR_GROUP_ID",
    "api_version": "5.131"
  },
  "schedule": {
    "interval_hours": 6
  }
}
```

Полный пример: [vk-workflow-config.example.json](./vk-workflow-config.example.json)

### База данных

Для логирования в БД:

1. Создайте базу данных
2. Выполните [database-schema.sql](./database-schema.sql)
3. Включите узлы Log Success/Error в workflow
4. Настройте credentials для PostgreSQL

## 📊 Аналитика

### Встроенная аналитика

Workflow собирает:
- ID опубликованных постов
- Статус публикации
- Время публикации
- Ошибки (если были)

### Расширенная аналитика (с БД)

SQL запросы для аналитики:

```sql
-- Статистика публикаций за последние 7 дней
SELECT 
    DATE(created_at) as date,
    COUNT(*) as posts_count,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful
FROM vk_posts_log
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at);

-- Топ постов по вовлеченности
SELECT 
    l.message,
    s.likes_count + s.reposts_count * 2 + s.comments_count * 3 as engagement
FROM vk_posts_log l
JOIN vk_posts_stats s ON l.post_id = s.post_id
ORDER BY engagement DESC
LIMIT 10;
```

## 🔐 Безопасность

### Рекомендации

1. **Храните токен в безопасности**
   - Используйте n8n credentials
   - Не коммитьте токен в git
   - Регулярно обновляйте токен

2. **Ограничьте права**
   - Запрашивайте только необходимые права
   - Используйте токен группы, а не личный

3. **Мониторинг**
   - Настройте уведомления об ошибках
   - Проверяйте логи регулярно
   - Отслеживайте rate limits

4. **Резервное копирование**
   - Экспортируйте workflow регулярно
   - Делайте backup БД с логами

## 🚨 Troubleshooting

### Частые проблемы

**"Invalid access token"**
- Получите новый токен
- Проверьте права токена

**"Access denied"**
- Убедитесь, что вы администратор группы
- Проверьте настройки приватности

**"Message is too long"**
- Максимум 4096 символов
- Добавьте обрезку текста

**"Rate limit exceeded"**
- Уменьшите частоту публикаций
- Добавьте задержки между запросами

Подробнее: [VK_WORKFLOW_README.md](./VK_WORKFLOW_README.md#troubleshooting)

## 📚 Документация

- [Быстрый старт](./QUICK_START.md) - запуск за 5 минут
- [Полная документация](./VK_WORKFLOW_README.md) - все возможности
- [VK API Reference](https://dev.vk.com/reference) - документация VK API
- [n8n Documentation](https://docs.n8n.io/) - документация n8n

## 🤝 Примеры использования

### Пример 1: Ежедневные мотивационные посты

```javascript
const quotes = [
  "Успех - это сумма маленьких усилий каждый день.",
  "Не бойтесь начинать с нуля."
];
const message = quotes[Math.floor(Math.random() * quotes.length)];
```

### Пример 2: Публикация новостей из RSS

1. Добавьте RSS Read узел
2. Трансформируйте данные
3. Публикуйте в VK

### Пример 3: Публикация с изображением

```javascript
const attachments = "photo-123456_789012";
return {
  json: {
    owner_id: "-123456",
    message: "Текст поста",
    attachments: attachments
  }
};
```

Больше примеров: [VK_WORKFLOW_README.md](./VK_WORKFLOW_README.md#примеры-использования)

## 🎨 Расширения

### Интеграции

- **OpenAI/Claude** - генерация уникального контента
- **RSS** - автоматическая публикация новостей
- **Telegram** - публикация из Telegram канала
- **Google Calendar** - планирование контента
- **Airtable** - управление контент-планом

### Дополнительные функции

- A/B тестирование контента
- Модерация перед публикацией
- Автоматическое добавление хештегов
- Публикация в несколько групп
- Планирование на будущее

## 📝 Структура проекта

```
.
├── README.md                          # Этот файл
├── QUICK_START.md                     # Быстрый старт
├── VK_WORKFLOW_README.md              # Полная документация
├── vk-content-workflow.json           # Базовый workflow
├── vk-advanced-workflow.json          # Продвинутый workflow
├── vk-workflow-config.example.json    # Пример конфигурации
├── database-schema.sql                # SQL схема
└── vk_api_tester.py                   # Утилита тестирования
```

## 🔄 Обновления

### Version 1.0 (2026-02-07)

- ✅ Базовый workflow для публикации
- ✅ Продвинутый workflow с AI
- ✅ Валидация контента
- ✅ Обработка ошибок
- ✅ Логирование в БД
- ✅ Python тестер
- ✅ Полная документация

## 💡 FAQ

**Q: Можно ли публиковать видео?**
A: Да, используйте метод `video.save` и добавьте attachment.

**Q: Как публиковать в несколько групп?**
A: Создайте цикл или дублируйте узел с разными owner_id.

**Q: Можно ли планировать посты?**
A: Да, используйте параметр `publish_date` (Unix timestamp).

**Q: Как удалить пост при ошибке?**
A: Используйте метод `wall.delete` с owner_id и post_id.

**Q: Нужен ли платный n8n?**
A: Нет, работает на self-hosted версии (бесплатно).

Больше вопросов: [VK_WORKFLOW_README.md](./VK_WORKFLOW_README.md#faq)

## 🤝 Поддержка

Если у вас возникли вопросы:

1. Проверьте [QUICK_START.md](./QUICK_START.md)
2. Прочитайте [VK_WORKFLOW_README.md](./VK_WORKFLOW_README.md)
3. Запустите `vk_api_tester.py` для диагностики
4. Проверьте [VK API Docs](https://dev.vk.com/reference)

## 📄 Лицензия

Этот проект распространяется свободно и может быть использован и модифицирован по вашему усмотрению.

## 🙏 Благодарности

- [n8n](https://n8n.io/) - за отличную платформу автоматизации
- [VK](https://vk.com/) - за API
- Сообщество n8n за поддержку и идеи

---

**Сделано с ❤️ для автоматизации контента в VK**

**Начните прямо сейчас:** [QUICK_START.md](./QUICK_START.md)
