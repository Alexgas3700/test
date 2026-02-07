# N8N Email Campaign Workflow

Профессиональный workflow для n8n, предназначенный для автоматизации email-рассылок с поддержкой множества функций.

## 🚀 Возможности

- **Множественные триггеры**: Ручной запуск, webhook, расписание (cron)
- **Гибкие источники данных**: База данных (PostgreSQL), REST API, или тестовые данные
- **Фильтрация получателей**: Автоматическая фильтрация подписчиков и валидация email
- **Мультиязычность**: Поддержка нескольких языков (английский, русский) с автоматическим выбором шаблона
- **Персонализация**: Динамическая подстановка данных получателя в письма
- **Множественные провайдеры**: SMTP, Gmail, SendGrid, Mailgun
- **Отслеживание**: Tracking pixels для открытий писем
- **Отписка**: Автоматические ссылки для отписки
- **Логирование**: Сохранение истории отправок в базу данных
- **Rate Limiting**: Контроль скорости отправки
- **A/B тестирование**: Встроенная поддержка A/B тестов (опционально)
- **Обработка ошибок**: Централизованная обработка ошибок отправки

## 📋 Требования

- n8n версии 1.0 или выше
- Один из почтовых провайдеров:
  - SMTP сервер
  - Gmail аккаунт с OAuth2
  - SendGrid API ключ
  - Mailgun API ключ
- (Опционально) PostgreSQL для хранения данных получателей и логов

## 🔧 Установка

### 1. Импорт workflow

1. Откройте n8n
2. Перейдите в раздел "Workflows"
3. Нажмите "Import from File"
4. Выберите файл `email-campaign-workflow.json`

### 2. Настройка credentials

#### Вариант A: SMTP

1. В n8n перейдите в "Credentials" → "New"
2. Выберите "SMTP"
3. Заполните данные:
   ```
   Host: smtp.example.com
   Port: 587
   User: your-email@example.com
   Password: your-password
   Secure: true (для SSL/TLS)
   ```

#### Вариант B: Gmail

1. Создайте OAuth2 credentials в Google Cloud Console
2. В n8n добавьте "Gmail OAuth2" credentials
3. Авторизуйтесь через Google

#### Вариант C: SendGrid

1. Получите API ключ в SendGrid Dashboard
2. В n8n добавьте "SendGrid API" credentials
3. Вставьте API ключ

#### Вариант D: Mailgun

1. Получите API ключ в Mailgun Dashboard
2. В n8n добавьте "HTTP Basic Auth" credentials
3. Username: `api`
4. Password: ваш Mailgun API ключ

### 3. Настройка источника данных

#### Вариант A: Тестовые данные (по умолчанию)

Workflow уже содержит узел "Sample Recipients Data" с тестовыми данными. Для начала работы просто запустите workflow.

#### Вариант B: База данных PostgreSQL

1. Включите узел "Get Recipients from Database" (снимите флаг "disabled")
2. Отключите узел "Sample Recipients Data"
3. Настройте PostgreSQL credentials
4. Создайте таблицу:

```sql
CREATE TABLE recipients (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    language VARCHAR(10) DEFAULT 'en',
    segment VARCHAR(50),
    subscribed BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Пример данных
INSERT INTO recipients (email, first_name, last_name, language, segment, subscribed)
VALUES 
    ('user1@example.com', 'John', 'Doe', 'en', 'premium', true),
    ('user2@example.com', 'Jane', 'Smith', 'ru', 'standard', true);
```

#### Вариант C: REST API

1. Включите узел "Get Recipients from API"
2. Отключите узел "Sample Recipients Data"
3. Настройте URL вашего API
4. Добавьте необходимую аутентификацию

API должен возвращать JSON массив с объектами:

```json
[
  {
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "language": "en",
    "segment": "premium",
    "subscribed": true
  }
]
```

### 4. Выбор триггера

#### Ручной запуск (по умолчанию)

Используется для тестирования. Просто нажмите "Test workflow".

#### Webhook триггер

1. Включите узел "Webhook Trigger (Alternative)"
2. Отключите "When clicking 'Test workflow'"
3. Настройте webhook URL
4. Отправляйте POST запросы для запуска рассылки

#### Расписание (Cron)

1. Включите узел "Schedule Trigger"
2. Отключите "When clicking 'Test workflow'"
3. Настройте cron выражение (по умолчанию: каждый понедельник в 9:00)

Примеры cron выражений:
- `0 9 * * 1` - каждый понедельник в 9:00
- `0 10 * * *` - каждый день в 10:00
- `0 9 1 * *` - первое число каждого месяца в 9:00

### 5. Выбор почтового провайдера

По умолчанию все узлы отправки отключены. Включите ОДИН из них:

1. **Send via SMTP** - для использования SMTP сервера
2. **Send via Gmail** - для Gmail API
3. **Send via SendGrid** - для SendGrid
4. **Send via Mailgun** - для Mailgun

Отключите остальные узлы отправки.

### 6. Настройка шаблонов писем

Отредактируйте узлы "English Email Template" и "Russian Email Template":

1. Измените `subject` - тему письма
2. Измените `htmlBody` - HTML версию письма
3. Измените `textBody` - текстовую версию письма

Доступные переменные для подстановки:
- `{{ $json.email }}` - email получателя
- `{{ $json.firstName }}` - имя
- `{{ $json.lastName }}` - фамилия
- `{{ $json.fullName }}` - полное имя
- `{{ $json.language }}` - язык
- `{{ $json.segment }}` - сегмент пользователя
- `{{ $json.unsubscribeLink }}` - ссылка отписки
- `{{ $json.trackingPixel }}` - пиксель отслеживания

### 7. (Опционально) Настройка логирования

Для сохранения логов отправки в базу данных:

1. Включите узел "Save to Database"
2. Создайте таблицу:

```sql
CREATE TABLE email_logs (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    subject TEXT,
    status VARCHAR(50),
    sent_at TIMESTAMP,
    campaign_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Использование

### Базовый запуск

1. Откройте workflow в n8n
2. Нажмите "Execute Workflow" или "Test workflow"
3. Проверьте результаты выполнения

### Добавление новых языков

1. Добавьте условие в узел "Split by Language"
2. Создайте новый узел "Set" для шаблона на новом языке
3. Подключите его к узлам отправки

### Настройка A/B тестирования

1. Включите узел "A/B Test Split"
2. Вставьте его между "Prepare Email Data" и "Split by Language"
3. Создайте два варианта шаблонов (A и B)
4. Используйте переменную `{{ $json.variant }}` для выбора шаблона

### Rate Limiting (ограничение скорости)

1. Включите узел "Rate Limit Delay"
2. Настройте задержку между отправками
3. Вставьте его перед узлами отправки

Это полезно для соблюдения лимитов почтовых провайдеров.

## 📊 Структура данных

### Формат получателя

```json
{
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "language": "en",
  "segment": "premium",
  "subscribed": true
}
```

### Формат лога

```json
{
  "timestamp": "2026-02-07T10:00:00.000Z",
  "email": "user@example.com",
  "subject": "Special Offer",
  "status": "sent",
  "campaign_id": "campaign_001"
}
```

## 🔒 Безопасность

### Отписка от рассылки

Workflow автоматически добавляет ссылки отписки в каждое письмо. Для реализации функционала отписки:

1. Создайте endpoint на вашем сервере: `https://example.com/unsubscribe`
2. Endpoint должен принимать параметры `email` и `token`
3. Проверяйте токен (hash email для безопасности)
4. Обновляйте статус `subscribed` в базе данных

Пример endpoint (Node.js/Express):

```javascript
app.get('/unsubscribe', async (req, res) => {
  const { email, token } = req.query;
  
  // Проверка токена
  if (hashEmail(email) !== token) {
    return res.status(400).send('Invalid token');
  }
  
  // Обновление статуса
  await db.query(
    'UPDATE recipients SET subscribed = false WHERE email = $1',
    [email]
  );
  
  res.send('You have been unsubscribed successfully');
});
```

### Tracking открытий

Workflow добавляет tracking pixel в письма. Для отслеживания открытий:

1. Создайте endpoint: `https://example.com/track/open`
2. Endpoint должен принимать `email` и `campaign_id`
3. Логируйте открытие в базу данных
4. Возвращайте прозрачный 1x1 пиксель (GIF)

Пример endpoint:

```javascript
app.get('/track/open', async (req, res) => {
  const { email, campaign_id } = req.query;
  
  // Логирование открытия
  await db.query(
    'INSERT INTO email_opens (email, campaign_id, opened_at) VALUES ($1, $2, NOW())',
    [email, campaign_id]
  );
  
  // Возврат прозрачного пикселя
  const pixel = Buffer.from(
    'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
    'base64'
  );
  res.type('image/gif').send(pixel);
});
```

## 🐛 Устранение неполадок

### Письма не отправляются

1. Проверьте credentials почтового провайдера
2. Убедитесь, что включен только ОДИН узел отправки
3. Проверьте логи n8n на наличие ошибок
4. Проверьте лимиты вашего почтового провайдера

### Некорректная персонализация

1. Убедитесь, что данные получателей содержат все необходимые поля
2. Проверьте синтаксис переменных: `{{ $json.fieldName }}`
3. Используйте узел "Edit Fields" для отладки данных

### Проблемы с кодировкой

1. Убедитесь, что в HTML шаблоне указан `<meta charset="UTF-8">`
2. Проверьте настройки кодировки в SMTP сервере
3. Используйте UTF-8 для всех текстовых данных

## 📈 Лучшие практики

### Производительность

- Используйте rate limiting для больших рассылок
- Разбивайте большие списки на батчи
- Используйте асинхронную отправку для больших объемов

### Доставляемость

- Настройте SPF, DKIM, DMARC записи для вашего домена
- Используйте подтвержденный домен отправителя
- Избегайте спам-триггеров в теме и тексте
- Всегда добавляйте ссылку отписки
- Предоставляйте текстовую версию письма

### Дизайн писем

- Используйте адаптивный дизайн (responsive)
- Тестируйте письма в разных почтовых клиентах
- Оптимизируйте изображения
- Используйте inline CSS для лучшей совместимости
- Добавляйте alt текст для изображений

### Сегментация

- Разделяйте получателей по сегментам
- Персонализируйте контент для каждого сегмента
- Используйте A/B тестирование для оптимизации
- Отслеживайте метрики для каждого сегмента

## 🔄 Расширенные сценарии

### Многоэтапная рассылка (Drip Campaign)

1. Создайте несколько копий workflow для каждого этапа
2. Используйте Schedule Trigger с разными интервалами
3. Отслеживайте статус пользователя в базе данных
4. Отправляйте следующее письмо только активным пользователям

### Триггерные письма

1. Используйте Webhook Trigger
2. Интегрируйте с вашим приложением
3. Отправляйте webhook при определенных событиях
4. Настройте разные шаблоны для разных событий

### Динамический контент

1. Используйте узел Code для генерации контента
2. Интегрируйте с внешними API для получения данных
3. Используйте условия для показа разного контента
4. Персонализируйте на основе поведения пользователя

## 📞 Поддержка

Для получения помощи:

1. Проверьте документацию n8n: https://docs.n8n.io
2. Посетите форум сообщества: https://community.n8n.io
3. Изучите примеры workflow: https://n8n.io/workflows

## 📝 Лицензия

Этот workflow предоставляется "как есть" без каких-либо гарантий. Вы можете свободно использовать, изменять и распространять его.

## 🔄 Обновления

### Версия 1.0 (2026-02-07)

- Начальный релиз
- Поддержка множественных триггеров
- Множественные почтовые провайдеры
- Мультиязычность (EN, RU)
- Персонализация и tracking
- A/B тестирование
- Rate limiting
- Логирование

---

**Примечание**: Не забудьте заменить все `example.com` на ваш реальный домен и настроить все credentials перед использованием в production.
