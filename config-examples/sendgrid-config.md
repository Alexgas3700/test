# SendGrid Configuration Guide

## Обзор

SendGrid - один из самых популярных сервисов для email рассылок с отличной доставляемостью и богатым функционалом.

## Преимущества

- ✅ Отличная доставляемость (>95%)
- ✅ Подробная аналитика и отчеты
- ✅ Встроенные шаблоны писем
- ✅ A/B тестирование
- ✅ Webhook для событий (открытия, клики, bounces)
- ✅ Управление подписками
- ✅ IP warming для новых аккаунтов
- ✅ Отличная документация

## Тарифы

### Free Tier
- **100 писем в день** (3,000 в месяц)
- Все основные функции
- Email поддержка
- **Идеально для**: тестирования и малых проектов

### Essentials
- **От $19.95/месяц** за 50,000 писем
- 2 дня email поддержки
- Удаление брендинга SendGrid
- **Идеально для**: малого бизнеса

### Pro
- **От $89.95/месяц** за 100,000 писем
- 24/7 email и chat поддержка
- Dedicated IP
- Subuser management
- **Идеально для**: среднего и крупного бизнеса

## Быстрый старт

### 1. Создание аккаунта

1. Перейдите на https://sendgrid.com
2. Нажмите "Start for Free"
3. Заполните регистрационную форму
4. Подтвердите email

### 2. Получение API ключа

1. Войдите в SendGrid Dashboard
2. Settings → API Keys
3. Нажмите "Create API Key"
4. Выберите "Full Access" или настройте права:
   - Mail Send: Full Access
   - Stats: Read Access (для аналитики)
   - Suppressions: Full Access (для отписок)
5. Скопируйте API ключ (он показывается только один раз!)
6. Сохраните ключ в безопасном месте

### 3. Верификация домена (рекомендуется)

#### Зачем нужна верификация:

- Улучшает доставляемость
- Позволяет использовать свой домен в "From" адресе
- Настраивает SPF и DKIM автоматически

#### Процесс верификации:

1. Settings → Sender Authentication → Domain Authentication
2. Нажмите "Get Started"
3. Выберите DNS хостинг (например, Cloudflare, GoDaddy)
4. Введите ваш домен (например, `example.com`)
5. SendGrid предоставит DNS записи для добавления:

```
CNAME: em1234.example.com → u1234567.wl123.sendgrid.net
CNAME: s1._domainkey.example.com → s1.domainkey.u1234567.wl123.sendgrid.net
CNAME: s2._domainkey.example.com → s2.domainkey.u1234567.wl123.sendgrid.net
```

6. Добавьте эти записи в DNS вашего домена
7. Вернитесь в SendGrid и нажмите "Verify"
8. Верификация может занять до 48 часов

### 4. Верификация отправителя (Single Sender)

Если не хотите верифицировать домен, можно верифицировать отдельный email:

1. Settings → Sender Authentication → Single Sender Verification
2. Нажмите "Create New Sender"
3. Заполните форму:
   - From Name: Your Company
   - From Email Address: noreply@yourdomain.com
   - Reply To: support@yourdomain.com
   - Company Address, City, State, Zip, Country
4. Нажмите "Save"
5. Проверьте email и подтвердите

## Настройка в n8n

### Вариант 1: SendGrid Node (рекомендуется)

1. В n8n workflow добавьте узел "SendGrid"
2. Создайте новый credential:
   - Credential Type: SendGrid API
   - API Key: вставьте ваш API ключ
3. Настройте параметры:
   ```
   Operation: Send
   From Email: noreply@yourdomain.com (верифицированный)
   To Email: {{ $json.email }}
   Subject: {{ $json.subject }}
   Email Type: HTML
   Message: {{ $json.htmlBody }}
   ```

### Вариант 2: HTTP Request Node

```json
{
  "method": "POST",
  "url": "https://api.sendgrid.com/v3/mail/send",
  "authentication": "headerAuth",
  "headerAuth": {
    "name": "Authorization",
    "value": "Bearer YOUR_API_KEY"
  },
  "body": {
    "personalizations": [
      {
        "to": [
          {
            "email": "{{ $json.email }}",
            "name": "{{ $json.fullName }}"
          }
        ],
        "subject": "{{ $json.subject }}"
      }
    ],
    "from": {
      "email": "noreply@yourdomain.com",
      "name": "Your Company"
    },
    "content": [
      {
        "type": "text/html",
        "value": "{{ $json.htmlBody }}"
      }
    ]
  }
}
```

## Продвинутые функции

### 1. Использование шаблонов SendGrid

SendGrid позволяет создавать шаблоны в веб-интерфейсе:

1. Email API → Dynamic Templates
2. Создайте новый шаблон
3. Используйте drag-and-drop редактор
4. Добавьте переменные: `{{firstName}}`, `{{offerUrl}}`
5. Скопируйте Template ID

В n8n:

```json
{
  "template_id": "d-1234567890abcdef",
  "personalizations": [
    {
      "to": [{"email": "{{ $json.email }}"}],
      "dynamic_template_data": {
        "firstName": "{{ $json.firstName }}",
        "offerUrl": "https://example.com/offer"
      }
    }
  ],
  "from": {
    "email": "noreply@yourdomain.com"
  }
}
```

### 2. Отслеживание событий (Webhooks)

SendGrid может отправлять webhook при различных событиях:

#### Настройка:

1. Settings → Mail Settings → Event Webhook
2. Enable Event Webhook
3. HTTP POST URL: `https://your-n8n-instance.com/webhook/sendgrid-events`
4. Выберите события:
   - Delivered
   - Opened
   - Clicked
   - Bounced
   - Spam Report
   - Unsubscribe

#### В n8n создайте webhook:

```json
{
  "node": "Webhook",
  "path": "sendgrid-events",
  "method": "POST"
}
```

#### Обработка событий:

```javascript
// Code node
const events = $input.all();

for (const event of events) {
  const data = event.json;
  
  switch(data.event) {
    case 'open':
      // Логируем открытие
      console.log(`Email opened: ${data.email}`);
      break;
    case 'click':
      // Логируем клик
      console.log(`Link clicked: ${data.url} by ${data.email}`);
      break;
    case 'bounce':
      // Помечаем email как невалидный
      console.log(`Email bounced: ${data.email}`);
      break;
    case 'unsubscribe':
      // Отписываем пользователя
      console.log(`Unsubscribed: ${data.email}`);
      break;
  }
}

return events;
```

### 3. Управление подписками

SendGrid автоматически обрабатывает отписки:

1. Добавьте в письмо:
   ```html
   <a href="<%asm_group_unsubscribe_raw_url%>">Unsubscribe</a>
   ```

2. Или используйте Subscription Groups:
   - Marketing → Unsubscribe Groups
   - Создайте группы (например, "Newsletter", "Promotions")
   - Пользователи могут отписаться от конкретных групп

### 4. Списки подавления (Suppression Lists)

SendGrid автоматически создает списки:

- **Bounces**: невалидные email адреса
- **Blocks**: временно заблокированные
- **Spam Reports**: пожаловались на спам
- **Invalid Emails**: некорректный формат
- **Unsubscribes**: отписались

Проверяйте эти списки перед отправкой:

```javascript
// Code node - проверка перед отправкой
const email = $json.email;

// Вызов SendGrid API для проверки
const response = await $http.request({
  method: 'GET',
  url: `https://api.sendgrid.com/v3/suppression/bounces/${email}`,
  headers: {
    'Authorization': `Bearer ${process.env.SENDGRID_API_KEY}`
  }
});

if (response.statusCode === 200) {
  // Email в списке bounces, не отправляем
  return [];
} else {
  // Email чистый, можно отправлять
  return [$input.item];
}
```

### 5. IP Pools и Dedicated IPs

Для больших объемов рассылок:

1. Settings → IP Addresses
2. Приобретите Dedicated IP ($89.95/месяц)
3. Создайте IP Pools для разных типов писем:
   - Транзакционные письма
   - Маркетинговые рассылки
4. Используйте IP warming для новых IP

В API:

```json
{
  "ip_pool_name": "marketing_pool",
  "from": {...},
  "personalizations": [...]
}
```

## Аналитика и отчеты

### Dashboard

SendGrid предоставляет подробную аналитику:

1. **Overview**: общая статистика
2. **Stats**: детальные метрики
   - Requests (отправлено)
   - Delivered (доставлено)
   - Opens (открыто)
   - Clicks (клики)
   - Bounces (отскоки)
   - Spam Reports
3. **Engagement**: поведение получателей
4. **Deliverability**: проблемы с доставкой

### API для получения статистики

```javascript
// Code node - получение статистики
const startDate = '2026-02-01';
const endDate = '2026-02-07';

const response = await $http.request({
  method: 'GET',
  url: `https://api.sendgrid.com/v3/stats?start_date=${startDate}&end_date=${endDate}`,
  headers: {
    'Authorization': `Bearer ${process.env.SENDGRID_API_KEY}`
  }
});

const stats = response.body;
console.log('Total delivered:', stats[0].stats[0].metrics.delivered);
console.log('Total opens:', stats[0].stats[0].metrics.opens);
console.log('Total clicks:', stats[0].stats[0].metrics.clicks);

return { json: stats };
```

## Лучшие практики

### 1. Разделение типов писем

Используйте разные subusers или IP pools для:
- Транзакционных писем (высокий приоритет)
- Маркетинговых рассылок (можно отложить)

### 2. Warm-up для новых аккаунтов

Не отправляйте сразу большие объемы:

**Неделя 1**: 50-100 писем в день
**Неделя 2**: 200-500 писем в день
**Неделя 3**: 1,000-2,000 писем в день
**Неделя 4+**: постепенно увеличивайте

### 3. Мониторинг репутации

Следите за:
- **Bounce rate**: должен быть < 5%
- **Spam rate**: должен быть < 0.1%
- **Open rate**: зависит от индустрии (обычно 15-25%)
- **Click rate**: обычно 2-5%

### 4. Сегментация

Используйте Categories и Custom Args для сегментации:

```json
{
  "categories": ["newsletter", "february_2026"],
  "custom_args": {
    "campaign_id": "winter_sale_2026",
    "user_segment": "premium"
  }
}
```

### 5. Тестирование

Перед массовой рассылкой:
1. Отправьте тестовое письмо себе
2. Проверьте в разных клиентах (Gmail, Outlook, Apple Mail)
3. Используйте SendGrid's Inbox Testing (платная функция)
4. Проверьте все ссылки

## Устранение проблем

### Низкая доставляемость

1. Верифицируйте домен
2. Настройте DKIM и SPF
3. Используйте dedicated IP (для больших объемов)
4. Проверьте содержание писем на спам-слова
5. Очистите список от невалидных адресов

### Письма в спаме

1. Добавьте физический адрес компании
2. Используйте ссылку отписки
3. Избегайте:
   - CAPS LOCK в теме
   - Множество восклицательных знаков!!!
   - Спам-слова (free, winner, click here)
4. Соотношение текст/изображения должно быть 60/40

### Ошибки API

**401 Unauthorized**:
- Проверьте API ключ
- Убедитесь, что ключ имеет нужные права

**403 Forbidden**:
- Email не верифицирован
- Превышен лимит

**429 Too Many Requests**:
- Превышен rate limit
- Добавьте задержки между запросами

## Миграция с других сервисов

### С Mailgun:

1. Экспортируйте списки получателей
2. Импортируйте в SendGrid Contacts
3. Обновите DNS записи
4. Замените API endpoints

### С Amazon SES:

1. Экспортируйте verified emails/domains
2. Верифицируйте в SendGrid
3. Обновите код для использования SendGrid API
4. Настройте webhooks для событий

## Безопасность

### Защита API ключей:

1. Никогда не коммитьте ключи в git
2. Используйте переменные окружения
3. Создавайте ключи с минимальными правами
4. Ротируйте ключи регулярно (раз в 3-6 месяцев)
5. Удаляйте неиспользуемые ключи

### IP Whitelisting:

1. Settings → Access Management → IP Access Management
2. Добавьте IP адреса, с которых разрешен доступ
3. Используйте для production аккаунтов

## Полезные ссылки

- Документация API: https://docs.sendgrid.com/api-reference
- Status Page: https://status.sendgrid.com
- Community Forum: https://community.sendgrid.com
- Email Validation Tool: https://sendgrid.com/solutions/email-validation-api/
- Deliverability Guide: https://sendgrid.com/resource/email-deliverability-guide/

## Контакты поддержки

- Email: support@sendgrid.com
- Chat: доступен в dashboard (Pro и выше)
- Phone: только для Enterprise планов
- Время ответа: 24-48 часов (Essentials), 24/7 (Pro+)
