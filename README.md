# n8n Workflow для постинга в Telegram группу

Этот репозиторий содержит готовые workflow для n8n, которые позволяют автоматизировать публикацию постов в Telegram группах.

## 📋 Содержание

- [Описание](#описание)
- [Доступные Workflow](#доступные-workflow)
- [Предварительные требования](#предварительные-требования)
- [Установка и настройка](#установка-и-настройка)
- [Использование](#использование)
- [Примеры](#примеры)
- [Устранение неполадок](#устранение-неполадок)

## 🎯 Описание

Коллекция n8n workflow для автоматизации постинга в Telegram группы. Поддерживает:

- ✅ Ручной запуск постов
- ⏰ Запланированные посты по расписанию
- 🔗 Webhook интеграция для внешних систем
- 🎨 HTML форматирование сообщений
- 📊 Условная логика публикации
- 🔐 API ключи для безопасности

## 📦 Доступные Workflow

### 1. Базовый Workflow (telegram_group_posting_workflow.json)

**Назначение:** Простой workflow для ручной отправки сообщений в Telegram группу.

**Особенности:**
- Ручной триггер (Manual Trigger)
- Настраиваемое сообщение
- HTML форматирование
- Поддержка эмодзи

**Когда использовать:** Для разовых постов или тестирования.

### 2. Запланированный Workflow (telegram_scheduled_posting_workflow.json)

**Назначение:** Автоматическая отправка сообщений по расписанию.

**Особенности:**
- Cron расписание (по умолчанию: каждый день в 9:00)
- Случайные мотивационные сообщения
- Условная логика (например, только в будни)
- Динамическое форматирование даты

**Когда использовать:** Для регулярных постов (ежедневные новости, напоминания, мотивационные сообщения).

### 3. Webhook Workflow (telegram_webhook_posting_workflow.json)

**Назначение:** Прием сообщений через HTTP API для публикации в Telegram.

**Особенности:**
- REST API endpoint
- Валидация API ключа
- Гибкая настройка сообщений
- JSON ответы
- Обработка ошибок

**Когда использовать:** Для интеграции с внешними системами (CRM, сайты, другие сервисы).

## 🔧 Предварительные требования

### 1. n8n установлен и запущен

Установите n8n одним из способов:

```bash
# Через npm
npm install n8n -g

# Через Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Через Docker Compose (рекомендуется для продакшена)
# См. docker-compose.example.yml
```

### 2. Telegram Bot

Вам нужен Telegram бот с токеном:

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный **Bot Token** (формат: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. ID Telegram группы

Получите Chat ID вашей группы:

1. Добавьте бота в вашу группу
2. Сделайте бота администратором (дайте права на отправку сообщений)
3. Отправьте любое сообщение в группу
4. Откройте в браузере: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. Найдите `"chat":{"id":-1001234567890}` - это ваш Chat ID

**Примечание:** Chat ID группы всегда начинается с `-100`

## 🚀 Установка и настройка

### Шаг 1: Импорт Workflow

1. Откройте n8n (обычно `http://localhost:5678`)
2. Нажмите на кнопку меню (☰) → **Import from File**
3. Выберите нужный workflow файл:
   - `telegram_group_posting_workflow.json` - базовый
   - `telegram_scheduled_posting_workflow.json` - по расписанию
   - `telegram_webhook_posting_workflow.json` - через webhook

### Шаг 2: Настройка Telegram Credentials

1. В импортированном workflow найдите узел **Send Telegram Message** (или аналогичный)
2. Нажмите на узел
3. В поле **Credentials** нажмите **Create New**
4. Выберите **Telegram API**
5. Введите ваш **Bot Token**
6. Нажмите **Save**

### Шаг 3: Настройка Chat ID

В зависимости от workflow:

#### Для базового workflow:
1. Откройте узел **Set Message Data**
2. Измените значение `chatId` на ваш Chat ID группы
3. Измените `message` на нужный текст

#### Для запланированного workflow:
1. Откройте узел **Prepare Message**
2. В коде JavaScript найдите строку:
   ```javascript
   chatId: '-1001234567890'
   ```
3. Замените на ваш Chat ID

#### Для webhook workflow:
- Chat ID можно передавать в запросе
- Или установить значение по умолчанию в узле **Send to Telegram**

### Шаг 4: Активация Workflow

1. Нажмите кнопку **Active** в правом верхнем углу
2. Workflow начнет работать согласно настройкам

## 💡 Использование

### Базовый Workflow

1. Откройте workflow
2. Нажмите **Execute Workflow** или **Test workflow**
3. Сообщение будет отправлено в группу

### Запланированный Workflow

#### Настройка расписания:

1. Откройте узел **Schedule Trigger**
2. Измените cron выражение:
   - `0 9 * * *` - каждый день в 9:00
   - `0 9 * * 1-5` - по будням в 9:00
   - `0 */4 * * *` - каждые 4 часа
   - `0 9,18 * * *` - в 9:00 и 18:00

#### Настройка условий:

В узле **Prepare Message** можно изменить логику:

```javascript
// Пример: постить только по понедельникам
const isMonday = dayOfWeek === 1;

// Пример: постить только с 9:00 до 18:00
const isWorkingHours = hour >= 9 && hour <= 18;

// Установите условие
const shouldPost = isMonday && isWorkingHours;
```

#### Настройка сообщений:

Измените массив `messages` в узле **Prepare Message**:

```javascript
const messages = [
  "🌟 Ваше сообщение 1",
  "💡 Ваше сообщение 2",
  "🎯 Ваше сообщение 3"
];
```

### Webhook Workflow

#### Получение URL webhook:

1. Откройте workflow
2. Нажмите на узел **Webhook**
3. Скопируйте **Production URL** (например: `https://your-n8n.com/webhook/telegram-post`)

#### Отправка запроса:

```bash
# Базовый запрос
curl -X POST https://your-n8n.com/webhook/telegram-post \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "your-secret-key",
    "message": "Привет из API!",
    "title": "Важное объявление"
  }'

# С дополнительными параметрами
curl -X POST https://your-n8n.com/webhook/telegram-post \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "your-secret-key",
    "chatId": "-1001234567890",
    "message": "Текст сообщения",
    "title": "Заголовок",
    "includeTimestamp": true,
    "silent": false,
    "disablePreview": false
  }'
```

#### Параметры запроса:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `apiKey` | string | Да | API ключ для авторизации |
| `message` | string | Да | Текст сообщения |
| `title` | string | Нет | Заголовок (будет выделен жирным) |
| `chatId` | string | Нет | ID группы (если не указан, используется значение по умолчанию) |
| `includeTimestamp` | boolean | Нет | Добавить временную метку |
| `silent` | boolean | Нет | Отправить без уведомления |
| `disablePreview` | boolean | Нет | Отключить предпросмотр ссылок |

## 📝 Примеры

### Пример 1: Ежедневная сводка новостей

```javascript
// В узле Prepare Message
const news = [
  "📰 Новость 1: ...",
  "📰 Новость 2: ...",
  "📰 Новость 3: ..."
];

const message = `<b>📅 Новости дня</b>\n\n${news.join('\n\n')}\n\n<i>Хорошего дня!</i>`;

return {
  chatId: '-1001234567890',
  message: message,
  shouldPost: true
};
```

### Пример 2: Интеграция с веб-формой

HTML форма на сайте:

```html
<form id="telegramForm">
  <input type="text" id="title" placeholder="Заголовок" required>
  <textarea id="message" placeholder="Сообщение" required></textarea>
  <button type="submit">Отправить в Telegram</button>
</form>

<script>
document.getElementById('telegramForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const response = await fetch('https://your-n8n.com/webhook/telegram-post', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      apiKey: 'your-secret-key',
      title: document.getElementById('title').value,
      message: document.getElementById('message').value,
      includeTimestamp: true
    })
  });
  
  const result = await response.json();
  alert(result.success ? 'Отправлено!' : 'Ошибка: ' + result.error);
});
</script>
```

### Пример 3: Еженедельный отчет

```javascript
// Cron: 0 9 * * 1 (каждый понедельник в 9:00)

const weekNumber = Math.ceil((new Date() - new Date(new Date().getFullYear(), 0, 1)) / 604800000);

const message = `
<b>📊 Еженедельный отчет - Неделя ${weekNumber}</b>

<b>Достижения:</b>
✅ Пункт 1
✅ Пункт 2
✅ Пункт 3

<b>Планы на неделю:</b>
🎯 Цель 1
🎯 Цель 2
🎯 Цель 3

<i>Продуктивной недели!</i>
`;

return {
  chatId: '-1001234567890',
  message: message,
  shouldPost: true
};
```

### Пример 4: HTML форматирование

```javascript
const message = `
<b>Жирный текст</b>
<i>Курсив</i>
<u>Подчеркнутый</u>
<s>Зачеркнутый</s>
<code>Моноширинный код</code>
<pre>Блок кода</pre>
<a href="https://example.com">Ссылка</a>

<b>Список:</b>
• Пункт 1
• Пункт 2
• Пункт 3

🎉 Эмодзи поддерживаются!
`;
```

## 🔐 Безопасность

### API ключи для Webhook

1. Откройте узел **Validate API Key** в webhook workflow
2. Измените условие проверки:

```javascript
// Простая проверка
value1: "={{ $json.body.apiKey }}"
value2: "your-secret-api-key-here"

// Или используйте переменные окружения n8n
value1: "={{ $json.body.apiKey }}"
value2: "={{ $env.TELEGRAM_API_KEY }}"
```

3. Установите переменную окружения:

```bash
# В .env файле n8n
TELEGRAM_API_KEY=your-secret-key-here
```

### Рекомендации:

- 🔒 Используйте HTTPS для webhook URL
- 🔑 Храните Bot Token в безопасности
- 🚫 Не публикуйте API ключи в коде
- 👥 Ограничьте права бота в группе
- 📝 Логируйте все запросы для аудита

## 🐛 Устранение неполадок

### Сообщения не отправляются

**Проблема:** Workflow выполняется, но сообщения не появляются в группе.

**Решения:**
1. Проверьте, что бот добавлен в группу
2. Убедитесь, что бот является администратором
3. Проверьте правильность Chat ID (должен начинаться с `-100`)
4. Проверьте Bot Token в credentials

### Ошибка "Chat not found"

**Проблема:** Telegram API возвращает ошибку "Chat not found".

**Решения:**
1. Убедитесь, что Chat ID правильный
2. Бот должен быть добавлен в группу ДО отправки сообщения
3. Для супергрупп ID начинается с `-100`

### Webhook не работает

**Проблема:** Запросы к webhook не обрабатываются.

**Решения:**
1. Убедитесь, что workflow активирован (кнопка Active)
2. Проверьте URL webhook (должен быть доступен извне)
3. Для локальной разработки используйте ngrok:
   ```bash
   ngrok http 5678
   ```
4. Проверьте формат JSON в запросе

### Расписание не срабатывает

**Проблема:** Scheduled workflow не запускается по расписанию.

**Решения:**
1. Workflow должен быть активирован
2. Проверьте cron выражение на правильность
3. Убедитесь, что n8n запущен постоянно (не останавливается)
4. Проверьте часовой пояс в настройках n8n

### HTML форматирование не работает

**Проблема:** HTML теги отображаются как текст.

**Решения:**
1. Убедитесь, что `parse_mode` установлен в `HTML`
2. Проверьте правильность HTML тегов
3. Telegram поддерживает ограниченный набор тегов: `<b>`, `<i>`, `<u>`, `<s>`, `<code>`, `<pre>`, `<a>`

## 📚 Дополнительные ресурсы

- [Документация n8n](https://docs.n8n.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Cron выражения](https://crontab.guru/)
- [HTML форматирование в Telegram](https://core.telegram.org/bots/api#html-style)

## 🤝 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте раздел [Устранение неполадок](#устранение-неполадок)
2. Изучите логи n8n (вкладка Executions)
3. Проверьте документацию Telegram Bot API

## 📄 Лицензия

Эти workflow предоставляются "как есть" для свободного использования и модификации.

---

**Версия:** 1.0.0  
**Последнее обновление:** Февраль 2026
