# N8N Customer Acquisition Email Campaign Workflow

Автоматизированная система email-рассылок для привлечения клиентов с персонализацией на основе предпочтений пользователей.

## 📋 Описание

Этот workflow реализует полноценную систему email-маркетинга для привлечения новых клиентов с использованием:
- Персонализации на основе user_preferences
- Сегментации по отраслям (industry)
- Динамического контента на основе интересов
- Автоматического логирования и отчетности

## 🎯 Основные возможности

### 1. Персонализация
- **Имя и приветствие**: Персональное обращение к каждому получателю
- **Интересы**: Контент адаптируется под интересы пользователя (automation, analytics, integration, security)
- **Отрасль**: Специализированные шаблоны для technology, finance, healthcare, retail
- **Язык**: Поддержка предпочитаемого языка из user_preferences
- **Должность и размер компании**: Контекстная информация для более релевантного контента

### 2. Сегментация
Автоматическая сегментация лидов по отраслям:
- Technology
- Finance
- Healthcare
- Retail
- Other

### 3. Динамический контент
Email включает блоки контента на основе интересов:
- 🚀 Automation Benefits
- 📊 Analytics Showcase
- 🔗 Integration Features
- 🔒 Security Highlights
- ✨ General Benefits
- 💬 Customer Testimonials

## 🏗️ Архитектура Workflow

### Узлы (Nodes)

1. **Triggers**
   - Manual Trigger: Для тестирования
   - Schedule Trigger: Автоматический запуск (каждый понедельник в 9:00)

2. **Data Collection**
   - Get Leads with Preferences: SQL-запрос для получения лидов с их предпочтениями
   - Filter Valid Leads: Фильтрация лидов с валидными данными

3. **Processing**
   - Segment by Industry: Сегментация по отраслям
   - Personalize Email Content: Создание персонализированного контента
   - Build Email HTML: Генерация финального HTML

4. **Sending** (выберите один из вариантов)
   - Send Email via SMTP
   - Send Email via Gmail
   - Send Email via SendGrid

5. **Tracking & Reporting**
   - Log Campaign Activity: Логирование отправленных писем
   - Check for Errors: Проверка ошибок
   - Log Errors: Логирование ошибок
   - Generate Campaign Summary: Создание отчета
   - Send Slack Notification: Уведомление команды

## 📊 Структура базы данных

### Таблица: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'lead',
    email_verified BOOLEAN DEFAULT false,
    unsubscribed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity_date TIMESTAMP
);
```

### Таблица: user_preferences
```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    interests TEXT, -- comma-separated: automation,analytics,integration,security
    preferred_language VARCHAR(10) DEFAULT 'en',
    industry VARCHAR(100), -- technology, finance, healthcare, retail, other
    company_size VARCHAR(50), -- small, medium, large, enterprise
    job_role VARCHAR(100), -- developer, manager, executive, etc.
    communication_frequency VARCHAR(50), -- daily, weekly, monthly
    opt_in_marketing BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Таблица: email_campaigns
```sql
CREATE TABLE email_campaigns (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    campaign_name VARCHAR(255),
    email_subject TEXT,
    template_id VARCHAR(100),
    segment VARCHAR(100),
    sent_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50), -- sent, failed, bounced
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP
);
```

### Таблица: email_errors
```sql
CREATE TABLE email_errors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    campaign_name VARCHAR(255),
    error_message TEXT,
    error_date TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Установка и настройка

### Шаг 1: Импорт workflow в n8n

1. Откройте n8n
2. Нажмите "Import from File"
3. Выберите файл `n8n-customer-acquisition-workflow.json`
4. Workflow будет импортирован со всеми узлами

### Шаг 2: Настройка credentials

#### PostgreSQL
1. Перейдите в Settings → Credentials
2. Создайте новый PostgreSQL credential
3. Укажите:
   - Host: ваш хост БД
   - Database: имя базы данных
   - User: пользователь БД
   - Password: пароль
   - Port: 5432 (по умолчанию)

#### Email Provider (выберите один)

**Вариант A: SMTP**
1. Создайте SMTP credential
2. Укажите данные вашего SMTP-сервера

**Вариант B: Gmail**
1. Создайте Gmail OAuth2 credential
2. Настройте OAuth2 в Google Cloud Console
3. Авторизуйте приложение

**Вариант C: SendGrid**
1. Создайте SendGrid API credential
2. Получите API ключ в SendGrid dashboard

#### Slack (опционально)
1. Создайте Incoming Webhook в Slack
2. Замените URL в узле "Send Slack Notification"

### Шаг 3: Настройка базы данных

Выполните SQL-скрипты из раздела "Структура базы данных" для создания необходимых таблиц.

### Шаг 4: Заполнение тестовых данных

Используйте файл `example-user-preferences.sql` для добавления тестовых данных.

### Шаг 5: Настройка расписания

В узле "Schedule Trigger" настройте cron-выражение:
- `0 9 * * 1` - каждый понедельник в 9:00
- `0 9 * * *` - каждый день в 9:00
- `0 9 * * 1,3,5` - понедельник, среда, пятница в 9:00

### Шаг 6: Тестирование

1. Используйте "Manual Trigger" для тестового запуска
2. Проверьте логи в n8n
3. Убедитесь, что письма отправлены
4. Проверьте записи в таблице `email_campaigns`

## 📧 Шаблоны писем

### Структура шаблона

Каждое письмо включает:
- **Header**: Градиентный заголовок с персональным приветствием
- **Content**: Динамические блоки контента на основе интересов
- **CTA Button**: Призыв к действию с UTM-метками
- **Footer**: Ссылки на отписку и управление предпочтениями

### Персонализация

Токены персонализации:
- `{{first_name}}` - Имя пользователя
- `{{interests}}` - Список интересов
- `{{industry}}` - Отрасль
- `{{company_size}}` - Размер компании
- `{{job_role}}` - Должность

### UTM-метки

Все ссылки включают UTM-метки для отслеживания:
```
?ref=email&industry={{industry}}&utm_source=n8n&utm_medium=email&utm_campaign=acquisition
```

## 📈 Аналитика и отчетность

### Метрики кампании

Workflow автоматически собирает:
- Общее количество обработанных лидов
- Успешно отправленные письма
- Ошибки отправки
- Распределение по сегментам

### Отчеты

После каждого запуска:
1. Данные сохраняются в `email_campaigns`
2. Генерируется сводка кампании
3. Отправляется уведомление в Slack

### SQL-запросы для аналитики

**Конверсия по сегментам:**
```sql
SELECT 
    segment,
    COUNT(*) as sent,
    COUNT(opened_at) as opened,
    COUNT(clicked_at) as clicked,
    ROUND(COUNT(opened_at)::numeric / COUNT(*) * 100, 2) as open_rate,
    ROUND(COUNT(clicked_at)::numeric / COUNT(*) * 100, 2) as click_rate
FROM email_campaigns
WHERE campaign_name = 'customer_acquisition'
    AND sent_at > NOW() - INTERVAL '30 days'
GROUP BY segment
ORDER BY sent DESC;
```

**Топ-шаблоны:**
```sql
SELECT 
    template_id,
    COUNT(*) as sent,
    COUNT(opened_at) as opened,
    ROUND(COUNT(opened_at)::numeric / COUNT(*) * 100, 2) as open_rate
FROM email_campaigns
WHERE sent_at > NOW() - INTERVAL '30 days'
GROUP BY template_id
ORDER BY open_rate DESC;
```

## 🔧 Кастомизация

### Добавление новых отраслей

В узле "Segment by Industry" добавьте новую отрасль в объект `segmentedLeads`:

```javascript
const segmentedLeads = {
  technology: [],
  finance: [],
  healthcare: [],
  retail: [],
  education: [], // новая отрасль
  other: []
};
```

### Добавление новых интересов

В узле "Personalize Email Content" добавьте новый блок контента:

```javascript
if (interests.includes('ai')) {
  contentBlocks.push('ai_features');
}
```

Затем в узле "Build Email HTML" добавьте соответствующий HTML-блок.

### Изменение дизайна писем

Отредактируйте CSS в узле "Build Email HTML" в секции `<style>`.

### Добавление A/B тестирования

Добавьте узел "Split In Batches" после "Filter Valid Leads" для разделения на группы A и B.

## 🔒 Безопасность и соответствие

### GDPR Compliance
- Все пользователи должны дать согласие (`opt_in_marketing = true`)
- Ссылка на отписку в каждом письме
- Возможность управления предпочтениями

### Защита данных
- Используйте SSL/TLS для подключения к БД
- Храните credentials в n8n Credentials Manager
- Не логируйте персональные данные в открытом виде

### Ограничение частоты
Добавьте проверку в SQL-запрос для предотвращения спама:

```sql
AND NOT EXISTS (
    SELECT 1 FROM email_campaigns 
    WHERE user_id = u.id 
    AND campaign_name = 'customer_acquisition'
    AND sent_at > NOW() - INTERVAL '7 days'
)
```

## 🐛 Устранение неполадок

### Письма не отправляются

1. Проверьте credentials для email-провайдера
2. Убедитесь, что в БД есть лиды с `opt_in_marketing = true`
3. Проверьте логи n8n на наличие ошибок
4. Проверьте таблицу `email_errors`

### Ошибки подключения к БД

1. Проверьте PostgreSQL credentials
2. Убедитесь, что БД доступна из n8n
3. Проверьте права пользователя БД

### Workflow не запускается по расписанию

1. Убедитесь, что workflow активирован (toggle в правом верхнем углу)
2. Проверьте cron-выражение в Schedule Trigger
3. Проверьте timezone в настройках n8n

## 📚 Дополнительные ресурсы

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [Email Marketing Best Practices](https://www.campaignmonitor.com/resources/)

## 🤝 Поддержка

Для вопросов и предложений:
- Создайте issue в репозитории
- Обратитесь в n8n community
- Проверьте документацию n8n

## 📝 Лицензия

Этот workflow предоставляется "как есть" для использования и модификации.

---

**Версия**: 1.0.0  
**Дата обновления**: 10 февраля 2026  
**Совместимость**: n8n v1.0+
