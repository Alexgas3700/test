# Mailgun Configuration Guide

## Обзор

Mailgun - мощный сервис для отправки email, особенно популярный среди разработчиков благодаря простому API и отличной документации.

## Преимущества

- ✅ Простой и понятный API
- ✅ Отличная документация
- ✅ Мощные инструменты валидации email
- ✅ Гибкая маршрутизация писем
- ✅ Webhook для всех событий
- ✅ Логи всех отправок (30 дней)
- ✅ Поддержка нескольких доменов
- ✅ Встроенный парсинг входящих писем

## Тарифы

### Free Trial
- **5,000 писем в месяц** (первые 3 месяца)
- Все основные функции
- Email поддержка
- **Идеально для**: тестирования

### Foundation
- **$35/месяц** за 50,000 писем
- $0.80 за каждую дополнительную 1,000
- Email поддержка
- 7 дней логов
- **Идеально для**: малого бизнеса

### Growth
- **$80/месяц** за 100,000 писем
- $0.70 за каждую дополнительную 1,000
- Email и chat поддержка
- 30 дней логов
- Email validation
- **Идеально для**: растущего бизнеса

### Scale
- **$90/месяц** за 100,000 писем
- $0.50 за каждую дополнительную 1,000
- Priority поддержка
- 30 дней логов
- Dedicated IPs
- **Идеально для**: крупного бизнеса

## Быстрый старт

### 1. Создание аккаунта

1. Перейдите на https://www.mailgun.com
2. Нажмите "Sign Up"
3. Заполните регистрационную форму
4. Подтвердите email
5. Добавьте платежную информацию (требуется даже для trial)

### 2. Получение API ключей

1. Войдите в Mailgun Dashboard
2. Settings → API Keys
3. Найдите:
   - **Private API Key**: для отправки писем
   - **Public Validation Key**: для валидации email
4. Скопируйте ключи

### 3. Настройка домена

#### Вариант A: Использование sandbox домена (для тестирования)

Mailgun предоставляет sandbox домен:
```
sandbox1234567890abcdef.mailgun.org
```

**Ограничения**:
- Можно отправлять только на авторизованные адреса
- Лимит 300 писем в день
- Не подходит для production

**Авторизация получателей**:
1. Sending → Sandbox Domain → Authorized Recipients
2. Добавьте email адреса для тестирования
3. Подтвердите через email

#### Вариант B: Добавление собственного домена (рекомендуется)

1. Sending → Domains → Add New Domain
2. Введите домен (например, `mg.example.com` или `mail.example.com`)
3. Mailgun предоставит DNS записи:

```
TXT @ "v=spf1 include:mailgun.org ~all"

TXT mailo._domainkey "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4..."

CNAME email.mg.example.com mailgun.org

MX @ mxa.mailgun.org (priority 10)
MX @ mxb.mailgun.org (priority 10)
```

4. Добавьте эти записи в DNS вашего домена
5. Вернитесь в Mailgun и нажмите "Verify DNS Settings"
6. Верификация обычно занимает 5-15 минут

### 4. Настройка SMTP (опционально)

Если предпочитаете SMTP вместо API:

```
Host: smtp.mailgun.org
Port: 587 (TLS) or 465 (SSL)
Username: postmaster@mg.yourdomain.com
Password: (найдите в Domain Settings → SMTP Credentials)
```

## Настройка в n8n

### Вариант 1: HTTP Request Node (рекомендуется)

```json
{
  "method": "POST",
  "url": "https://api.mailgun.net/v3/mg.yourdomain.com/messages",
  "authentication": "basicAuth",
  "basicAuth": {
    "user": "api",
    "password": "YOUR_PRIVATE_API_KEY"
  },
  "sendBody": true,
  "contentType": "form-urlencoded",
  "bodyParameters": {
    "from": "Your Company <noreply@mg.yourdomain.com>",
    "to": "{{ $json.email }}",
    "subject": "{{ $json.subject }}",
    "html": "{{ $json.htmlBody }}",
    "text": "{{ $json.textBody }}"
  }
}
```

### Вариант 2: SMTP через n8n

```json
{
  "node": "Email Send (SMTP)",
  "credentials": {
    "host": "smtp.mailgun.org",
    "port": 587,
    "user": "postmaster@mg.yourdomain.com",
    "password": "YOUR_SMTP_PASSWORD",
    "secure": true
  },
  "fromEmail": "noreply@mg.yourdomain.com",
  "toEmail": "{{ $json.email }}",
  "subject": "{{ $json.subject }}",
  "html": "{{ $json.htmlBody }}"
}
```

## Продвинутые функции

### 1. Отправка с вложениями

```javascript
// Code node для подготовки multipart/form-data
const FormData = require('form-data');
const form = new FormData();

form.append('from', 'Your Company <noreply@mg.yourdomain.com>');
form.append('to', $json.email);
form.append('subject', $json.subject);
form.append('html', $json.htmlBody);

// Добавление вложения
if ($json.attachment) {
  form.append('attachment', $json.attachment.buffer, {
    filename: $json.attachment.filename,
    contentType: $json.attachment.mimeType
  });
}

return { json: { formData: form } };
```

### 2. Использование шаблонов

Mailgun поддерживает шаблоны через Handlebars:

```javascript
// HTTP Request Node
{
  "method": "POST",
  "url": "https://api.mailgun.net/v3/mg.yourdomain.com/messages",
  "bodyParameters": {
    "from": "noreply@mg.yourdomain.com",
    "to": "{{ $json.email }}",
    "subject": "{{ $json.subject }}",
    "template": "welcome_email",
    "h:X-Mailgun-Variables": JSON.stringify({
      "firstName": "{{ $json.firstName }}",
      "activationLink": "{{ $json.activationLink }}"
    })
  }
}
```

Создание шаблона:
1. Sending → Templates → Create Template
2. Используйте Handlebars синтаксис:
   ```html
   <h1>Welcome, {{firstName}}!</h1>
   <a href="{{activationLink}}">Activate Account</a>
   ```

### 3. Отслеживание (Tracking)

Mailgun автоматически добавляет tracking:

```javascript
{
  "bodyParameters": {
    // ... другие параметры
    "o:tracking": "yes",           // Общий tracking
    "o:tracking-clicks": "yes",    // Отслеживание кликов
    "o:tracking-opens": "yes"      // Отслеживание открытий
  }
}
```

### 4. Планирование отправки

Отправка письма в определенное время:

```javascript
{
  "bodyParameters": {
    // ... другие параметры
    "o:deliverytime": "Fri, 14 Feb 2026 12:00:00 GMT"
  }
}
```

### 5. Теги и метаданные

Для организации и аналитики:

```javascript
{
  "bodyParameters": {
    // ... другие параметры
    "o:tag": ["newsletter", "february_2026"],
    "o:campaign": "winter_sale",
    "v:user_id": "12345",
    "v:campaign_id": "camp_001"
  }
}
```

### 6. Webhooks для событий

Mailgun отправляет webhook при различных событиях:

#### Настройка:

1. Sending → Webhooks
2. Добавьте webhook URL: `https://your-n8n-instance.com/webhook/mailgun-events`
3. Выберите события:
   - Delivered
   - Opened
   - Clicked
   - Bounced
   - Complained (spam report)
   - Unsubscribed
   - Failed

#### Защита webhook (рекомендуется):

Mailgun подписывает webhooks. Проверка в n8n:

```javascript
// Code node
const crypto = require('crypto');

const signature = $input.item.json.signature;
const timestamp = signature.timestamp;
const token = signature.token;
const receivedSignature = signature.signature;

// Ваш webhook signing key из Mailgun
const signingKey = process.env.MAILGUN_WEBHOOK_SIGNING_KEY;

// Вычисляем ожидаемую подпись
const expectedSignature = crypto
  .createHmac('sha256', signingKey)
  .update(timestamp + token)
  .digest('hex');

if (receivedSignature !== expectedSignature) {
  throw new Error('Invalid webhook signature');
}

// Обработка события
const eventData = $input.item.json['event-data'];
console.log('Event:', eventData.event);
console.log('Email:', eventData.recipient);

return $input.all();
```

#### Обработка событий:

```javascript
// Code node
const eventData = $json['event-data'];

switch(eventData.event) {
  case 'delivered':
    console.log(`Email delivered to ${eventData.recipient}`);
    // Обновить статус в БД
    break;
    
  case 'opened':
    console.log(`Email opened by ${eventData.recipient}`);
    // Логировать открытие
    break;
    
  case 'clicked':
    console.log(`Link clicked: ${eventData.url}`);
    // Логировать клик
    break;
    
  case 'bounced':
    console.log(`Email bounced: ${eventData.recipient}`);
    console.log(`Reason: ${eventData.reason}`);
    // Пометить email как невалидный
    break;
    
  case 'complained':
    console.log(`Spam complaint from ${eventData.recipient}`);
    // Немедленно отписать
    break;
    
  case 'unsubscribed':
    console.log(`Unsubscribed: ${eventData.recipient}`);
    // Обновить статус подписки
    break;
}

return { json: eventData };
```

### 7. Валидация email адресов

Mailgun предоставляет API для валидации:

```javascript
// Code node - валидация перед отправкой
const email = $json.email;

const response = await $http.request({
  method: 'GET',
  url: `https://api.mailgun.net/v4/address/validate`,
  auth: {
    user: 'api',
    password: process.env.MAILGUN_PUBLIC_KEY
  },
  qs: {
    address: email
  }
});

const validation = response.body;

if (validation.result === 'deliverable') {
  // Email валидный, можно отправлять
  return [$input.item];
} else {
  // Email невалидный, пропускаем
  console.log(`Invalid email: ${email} - ${validation.reason}`);
  return [];
}
```

Результаты валидации:
- `deliverable` - можно отправлять
- `undeliverable` - не отправлять
- `do_not_send` - в blacklist
- `catch_all` - домен принимает все адреса
- `unknown` - невозможно определить

### 8. Bulk отправка

Для массовых рассылок используйте batch sending:

```javascript
// Code node - подготовка batch
const recipients = [
  { email: 'user1@example.com', name: 'John', vars: { code: 'ABC123' } },
  { email: 'user2@example.com', name: 'Jane', vars: { code: 'DEF456' } }
];

const recipientVariables = {};
const toList = [];

recipients.forEach(recipient => {
  toList.push(`${recipient.name} <${recipient.email}>`);
  recipientVariables[recipient.email] = recipient.vars;
});

return {
  json: {
    to: toList.join(', '),
    recipientVariables: JSON.stringify(recipientVariables)
  }
};
```

```javascript
// HTTP Request Node
{
  "bodyParameters": {
    "from": "noreply@mg.yourdomain.com",
    "to": "{{ $json.to }}",
    "subject": "Your code: %recipient.code%",
    "html": "<p>Hi %recipient_fname%! Your code is: %recipient.code%</p>",
    "recipient-variables": "{{ $json.recipientVariables }}"
  }
}
```

### 9. Маршрутизация (Routes)

Автоматическая обработка входящих писем:

1. Receiving → Routes → Create Route
2. Настройте условие:
   ```
   match_recipient("support@mg.yourdomain.com")
   ```
3. Действие:
   ```
   forward("https://your-n8n-instance.com/webhook/incoming-email")
   store(notify="https://your-n8n-instance.com/webhook/email-stored")
   ```

В n8n создайте webhook для обработки:

```javascript
// Code node
const emailData = $json;

console.log('From:', emailData.sender);
console.log('Subject:', emailData.subject);
console.log('Body:', emailData['body-plain']);

// Парсинг и обработка письма
// Например, создание тикета в системе поддержки

return { json: emailData };
```

### 10. Списки рассылки (Mailing Lists)

Создание и управление списками:

```javascript
// Создание списка
const response = await $http.request({
  method: 'POST',
  url: 'https://api.mailgun.net/v3/lists',
  auth: { user: 'api', password: process.env.MAILGUN_API_KEY },
  form: {
    address: 'newsletter@mg.yourdomain.com',
    name: 'Newsletter Subscribers',
    description: 'Monthly newsletter list'
  }
});

// Добавление подписчика
await $http.request({
  method: 'POST',
  url: 'https://api.mailgun.net/v3/lists/newsletter@mg.yourdomain.com/members',
  auth: { user: 'api', password: process.env.MAILGUN_API_KEY },
  form: {
    address: 'user@example.com',
    name: 'John Doe',
    vars: JSON.stringify({ age: 30, city: 'Moscow' }),
    subscribed: 'yes'
  }
});
```

## Аналитика и логи

### Просмотр логов

1. Sending → Logs
2. Фильтры:
   - По email получателя
   - По тегу
   - По статусу (delivered, failed, etc.)
   - По дате

### API для получения логов

```javascript
// Code node
const response = await $http.request({
  method: 'GET',
  url: 'https://api.mailgun.net/v3/mg.yourdomain.com/events',
  auth: { user: 'api', password: process.env.MAILGUN_API_KEY },
  qs: {
    begin: 'Mon, 03 Feb 2026 00:00:00 GMT',
    end: 'Fri, 07 Feb 2026 23:59:59 GMT',
    event: 'delivered',
    limit: 300
  }
});

const events = response.body.items;
console.log(`Total delivered: ${events.length}`);

return { json: events };
```

### Статистика

```javascript
// Получение статистики за период
const response = await $http.request({
  method: 'GET',
  url: 'https://api.mailgun.net/v3/mg.yourdomain.com/stats/total',
  auth: { user: 'api', password: process.env.MAILGUN_API_KEY },
  qs: {
    event: ['accepted', 'delivered', 'failed', 'opened', 'clicked'],
    start: '2026-02-01',
    end: '2026-02-07',
    resolution: 'day'
  }
});

const stats = response.body.stats;
stats.forEach(day => {
  console.log(`Date: ${day.time}`);
  console.log(`Delivered: ${day.delivered.total}`);
  console.log(`Opened: ${day.opened.total}`);
  console.log(`Clicked: ${day.clicked.total}`);
});
```

## Лучшие практики

### 1. Используйте поддомен

Вместо `example.com` используйте `mg.example.com` или `mail.example.com`:
- Защищает основной домен
- Легче управлять DNS
- Изолирует репутацию

### 2. Warm-up для новых доменов

**День 1-3**: 50 писем в день
**День 4-7**: 100-200 писем в день
**Неделя 2**: 500-1,000 писем в день
**Неделя 3**: 2,000-5,000 писем в день
**Неделя 4+**: полный объем

### 3. Мониторинг метрик

Следите за:
- **Delivery rate**: должен быть > 95%
- **Bounce rate**: должен быть < 5%
- **Complaint rate**: должен быть < 0.1%
- **Open rate**: 15-25% (зависит от индустрии)
- **Click rate**: 2-5%

### 4. Управление репутацией

1. Регулярно очищайте списки от bounced emails
2. Немедленно обрабатывайте жалобы на спам
3. Используйте double opt-in для подписок
4. Сегментируйте аудиторию
5. Не покупайте списки email адресов

### 5. Оптимизация доставляемости

1. Используйте validated email адреса
2. Настройте SPF, DKIM, DMARC
3. Поддерживайте чистые списки
4. Персонализируйте контент
5. Избегайте спам-триггеров
6. Используйте dedicated IP для больших объемов

## Устранение проблем

### Письма не доставляются

1. Проверьте логи в Mailgun Dashboard
2. Убедитесь, что домен верифицирован
3. Проверьте DNS записи
4. Убедитесь, что не превышен лимит
5. Проверьте, не в blacklist ли ваш IP

### Высокий bounce rate

1. Используйте email validation API
2. Удаляйте hard bounces из списков
3. Проверьте формат email адресов
4. Используйте double opt-in

### Письма в спаме

1. Настройте DMARC policy
2. Добавьте физический адрес
3. Используйте ссылку отписки
4. Избегайте спам-слов
5. Проверьте sender reputation

### API ошибки

**401 Unauthorized**:
```
Проверьте API ключ и формат аутентификации
```

**400 Bad Request**:
```
Проверьте параметры запроса, особенно email адреса
```

**402 Payment Required**:
```
Превышен лимит или проблема с оплатой
```

**404 Not Found**:
```
Неправильный домен в URL
```

## Миграция

### С SendGrid:

1. Экспортируйте списки получателей
2. Верифицируйте домен в Mailgun
3. Обновите DNS записи
4. Замените API endpoints
5. Настройте webhooks

### С Amazon SES:

1. Верифицируйте домен в Mailgun
2. Обновите код для Mailgun API
3. Настройте webhooks вместо SNS
4. Перенесите suppression lists

## Регионы

Mailgun доступен в двух регионах:

### US Region (по умолчанию)
- API: `https://api.mailgun.net`
- SMTP: `smtp.mailgun.org`

### EU Region
- API: `https://api.eu.mailgun.net`
- SMTP: `smtp.eu.mailgun.org`

Выбирайте регион ближе к вашей аудитории для лучшей производительности.

## Безопасность

### Защита API ключей

1. Используйте переменные окружения
2. Никогда не коммитьте в git
3. Создавайте отдельные ключи для разных приложений
4. Регулярно ротируйте ключи
5. Используйте read-only ключи где возможно

### Webhook signing

Всегда проверяйте подпись webhook для защиты от поддельных запросов.

### IP Whitelist

1. Settings → Security → IP Whitelist
2. Добавьте IP адреса, с которых разрешен API доступ

## Полезные ссылки

- Документация API: https://documentation.mailgun.com/
- Status Page: https://status.mailgun.com/
- Email Validation: https://www.mailgun.com/email-validation/
- Deliverability Guide: https://www.mailgun.com/resources/
- Postman Collection: https://www.postman.com/mailgun

## Поддержка

- Email: support@mailgun.com
- Chat: доступен в dashboard (Growth и выше)
- Documentation: https://help.mailgun.com/
- Время ответа: 24-48 часов (Foundation), 12-24 часа (Growth+)
