# Quick Setup Guide - n8n Customer Acquisition Workflow

Пошаговое руководство по настройке и запуску email-кампании для привлечения клиентов.

## 📋 Предварительные требования

### Необходимое ПО
- ✅ n8n (версия 1.0 или выше)
- ✅ PostgreSQL (версия 12 или выше)
- ✅ Email provider (SMTP, Gmail, или SendGrid)

### Необходимые данные
- 📧 Email credentials (SMTP, Gmail OAuth2, или SendGrid API key)
- 🗄️ PostgreSQL connection details
- 🔔 Slack webhook URL (опционально)

---

## 🚀 Быстрый старт (15 минут)

### Шаг 1: Импорт Workflow (2 минуты)

1. Откройте n8n в браузере
2. Нажмите кнопку **"+"** в левом верхнем углу
3. Выберите **"Import from File"**
4. Загрузите файл `n8n-customer-acquisition-workflow.json`
5. Нажмите **"Import"**

✅ Workflow успешно импортирован!

### Шаг 2: Настройка PostgreSQL (5 минут)

#### 2.1 Создание Credential

1. В n8n перейдите в **Settings → Credentials**
2. Нажмите **"Add Credential"**
3. Найдите и выберите **"PostgreSQL"**
4. Заполните поля:
   ```
   Host: localhost (или ваш хост)
   Database: your_database_name
   User: your_username
   Password: your_password
   Port: 5432
   SSL: Enable (рекомендуется для production)
   ```
5. Нажмите **"Save"**
6. Дайте credential понятное имя: "PostgreSQL account"

#### 2.2 Создание таблиц

Выполните SQL-скрипт из файла `example-user-preferences.sql`:

```bash
psql -U your_username -d your_database_name -f example-user-preferences.sql
```

Или скопируйте и выполните SQL-команды вручную в вашем PostgreSQL клиенте.

✅ База данных настроена!

### Шаг 3: Настройка Email Provider (5 минут)

Выберите один из вариантов:

#### Вариант A: SMTP (Универсальный)

1. В n8n: **Settings → Credentials → Add Credential**
2. Выберите **"SMTP"**
3. Заполните:
   ```
   Host: smtp.gmail.com (или ваш SMTP сервер)
   Port: 587 (или 465 для SSL)
   User: your-email@gmail.com
   Password: your-app-password
   Secure: true
   ```
4. Сохраните как "SMTP account"

**Для Gmail**: Используйте App Password, не обычный пароль!
- Создайте App Password: https://myaccount.google.com/apppasswords

#### Вариант B: Gmail OAuth2 (Рекомендуется для Gmail)

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com)
2. Включите Gmail API
3. Создайте OAuth 2.0 credentials
4. В n8n: **Settings → Credentials → Add Credential**
5. Выберите **"Gmail OAuth2"**
6. Введите Client ID и Client Secret
7. Пройдите OAuth авторизацию
8. Сохраните как "Gmail OAuth2 account"

#### Вариант C: SendGrid (Рекомендуется для массовых рассылок)

1. Зарегистрируйтесь на [SendGrid](https://sendgrid.com)
2. Создайте API Key в SendGrid Dashboard
3. В n8n: **Settings → Credentials → Add Credential**
4. Выберите **"SendGrid"**
5. Вставьте API Key
6. Сохраните как "SendGrid account"

✅ Email provider настроен!

### Шаг 4: Связывание Credentials с Workflow (2 минуты)

1. Откройте импортированный workflow
2. Найдите узел **"Get Leads with Preferences"**
3. Кликните на узел
4. В правой панели выберите ваш PostgreSQL credential
5. Повторите для узлов:
   - "Log Campaign Activity"
   - "Log Errors"
6. Выберите один из email-узлов (SMTP, Gmail, или SendGrid)
7. Удалите неиспользуемые email-узлы (опционально)
8. Привяжите credential к выбранному email-узлу

✅ Credentials связаны!

### Шаг 5: Тестовый запуск (1 минута)

1. В workflow нажмите **"Execute Workflow"** (кнопка play)
2. Workflow запустится с использованием Manual Trigger
3. Проверьте выполнение каждого узла (зеленые галочки = успех)
4. Проверьте вашу почту на наличие тестового письма

✅ Workflow работает!

---

## 🔧 Детальная настройка

### Настройка расписания

По умолчанию workflow запускается каждый понедельник в 9:00.

**Изменить расписание:**

1. Откройте узел **"Schedule Trigger"**
2. Измените cron-выражение:
   - Каждый день в 9:00: `0 9 * * *`
   - Каждый понедельник, среду, пятницу в 9:00: `0 9 * * 1,3,5`
   - Каждый час: `0 * * * *`
   - Каждые 2 часа: `0 */2 * * *`

**Cron-генератор**: https://crontab.guru/

### Настройка Slack уведомлений (опционально)

1. Создайте Incoming Webhook в Slack:
   - Перейдите в Slack App Directory
   - Найдите "Incoming Webhooks"
   - Выберите канал для уведомлений
   - Скопируйте Webhook URL
2. В workflow откройте узел **"Send Slack Notification"**
3. Замените URL на ваш Webhook URL
4. Настройте текст сообщения (опционально)

### Персонализация email-контента

#### Изменение отправителя

В узле **"Build Email HTML"** найдите:

```javascript
from: 'hello@yourcompany.com',
fromName: 'Your Company Team',
replyTo: 'support@yourcompany.com',
```

Замените на ваши данные.

#### Изменение дизайна

В узле **"Build Email HTML"** найдите секцию `<style>` и измените:

- **Цвета**: Замените `#667eea` и `#764ba2` на цвета вашего бренда
- **Шрифты**: Измените `font-family`
- **Размеры**: Настройте `padding`, `margin`, `font-size`

#### Добавление логотипа

В секции `.header` добавьте:

```html
<img src="https://yourcompany.com/logo.png" alt="Company Logo" style="max-width: 200px; margin-bottom: 20px;">
```

#### Изменение CTA

Найдите `.cta-button` и измените:

```html
<a href="https://yourcompany.com/signup?..." class="cta-button">
  Ваш текст кнопки →
</a>
```

### Добавление новых сегментов

#### Добавить новую отрасль (например, "Education")

1. **В узле "Segment by Industry":**

```javascript
const segmentedLeads = {
  technology: [],
  finance: [],
  healthcare: [],
  retail: [],
  education: [], // НОВАЯ ОТРАСЛЬ
  other: []
};
```

2. **В узле "Personalize Email Content":**

```javascript
} else if (industry === 'education') {
  templateId = 'education_acquisition';
  subject = `${item.personalization.greeting}, Transform Education with Technology`;
  preheader = 'Innovative solutions for educational institutions';
}
```

3. **В узле "Build Email HTML":**

Добавьте специфичный контент для образования.

#### Добавить новый интерес (например, "AI")

1. **В узле "Personalize Email Content":**

```javascript
if (interests.includes('ai')) {
  contentBlocks.push('ai_features');
}
```

2. **В узле "Build Email HTML":**

```javascript
if (config.content_blocks.includes('ai_features')) {
  htmlContent += `
      <div class="benefit-box">
        <h3>🤖 AI-Powered Features</h3>
        <p>Leverage artificial intelligence to automate and optimize your workflows.</p>
      </div>
`;
}
```

### Ограничение частоты рассылок

Чтобы не отправлять письма слишком часто одним и тем же пользователям:

**В узле "Get Leads with Preferences"**, добавьте в SQL-запрос:

```sql
AND NOT EXISTS (
    SELECT 1 FROM email_campaigns 
    WHERE user_id = u.id 
    AND campaign_name = 'customer_acquisition'
    AND sent_at > NOW() - INTERVAL '7 days'
)
```

Это исключит пользователей, которым отправляли письмо в последние 7 дней.

---

## 📊 Мониторинг и аналитика

### Проверка отправленных писем

```sql
SELECT 
    COUNT(*) as total_sent,
    segment,
    DATE(sent_at) as send_date
FROM email_campaigns
WHERE campaign_name = 'customer_acquisition'
    AND sent_at > NOW() - INTERVAL '30 days'
GROUP BY segment, DATE(sent_at)
ORDER BY send_date DESC, total_sent DESC;
```

### Проверка ошибок

```sql
SELECT 
    COUNT(*) as error_count,
    error_message,
    DATE(error_date) as error_date
FROM email_errors
WHERE error_date > NOW() - INTERVAL '7 days'
GROUP BY error_message, DATE(error_date)
ORDER BY error_count DESC;
```

### Анализ эффективности по сегментам

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
ORDER BY open_rate DESC;
```

### Топ-шаблоны по конверсии

```sql
SELECT 
    template_id,
    COUNT(*) as sent,
    COUNT(opened_at) as opened,
    COUNT(clicked_at) as clicked,
    ROUND(COUNT(clicked_at)::numeric / COUNT(opened_at) * 100, 2) as ctr
FROM email_campaigns
WHERE sent_at > NOW() - INTERVAL '30 days'
    AND opened_at IS NOT NULL
GROUP BY template_id
ORDER BY ctr DESC;
```

---

## 🐛 Устранение неполадок

### Проблема: Workflow не запускается по расписанию

**Решение:**
1. Убедитесь, что workflow **активирован** (toggle в правом верхнем углу должен быть включен)
2. Проверьте cron-выражение в Schedule Trigger
3. Проверьте timezone в настройках n8n (Settings → General)
4. Проверьте логи n8n: `docker logs n8n` (если используете Docker)

### Проблема: Ошибка подключения к PostgreSQL

**Решение:**
1. Проверьте, что PostgreSQL запущен: `sudo systemctl status postgresql`
2. Проверьте host и port в credentials
3. Убедитесь, что пользователь имеет права на базу данных
4. Проверьте firewall: `sudo ufw status`
5. Для удаленного подключения: отредактируйте `pg_hba.conf`

### Проблема: Письма не отправляются

**Решение:**
1. Проверьте email credentials
2. Для Gmail: используйте App Password, не обычный пароль
3. Проверьте лимиты отправки вашего email-провайдера
4. Проверьте таблицу `email_errors` на наличие ошибок
5. Проверьте логи узла отправки email в n8n

### Проблема: Письма попадают в спам

**Решение:**
1. Настройте SPF, DKIM, и DMARC записи для вашего домена
2. Используйте профессиональный email-сервис (SendGrid, Mailgun)
3. Прогрейте домен (начните с малых объемов)
4. Избегайте спам-слов в subject и content
5. Включите unsubscribe link
6. Проверьте спам-скор: https://www.mail-tester.com/

### Проблема: Нет тестовых данных

**Решение:**
1. Выполните SQL-скрипт: `psql -U user -d db -f example-user-preferences.sql`
2. Проверьте, что пользователи имеют `opt_in_marketing = true`
3. Проверьте, что `email_verified = true`
4. Проверьте, что `status = 'lead'`

### Проблема: Workflow выполняется слишком долго

**Решение:**
1. Добавьте LIMIT в SQL-запрос (например, LIMIT 100)
2. Используйте индексы в PostgreSQL
3. Разбейте workflow на несколько частей
4. Используйте "Split In Batches" узел для обработки по частям
5. Увеличьте timeout в настройках n8n

---

## 🔒 Безопасность

### Checklist безопасности

- [ ] Используйте SSL/TLS для PostgreSQL
- [ ] Храните credentials только в n8n Credentials Manager
- [ ] Не логируйте персональные данные
- [ ] Используйте App Passwords для Gmail
- [ ] Ограничьте права пользователя PostgreSQL
- [ ] Регулярно обновляйте n8n
- [ ] Используйте firewall для ограничения доступа
- [ ] Включите двухфакторную аутентификацию для n8n
- [ ] Регулярно делайте backup базы данных
- [ ] Мониторьте логи на подозрительную активность

### GDPR Compliance

- [ ] Получайте явное согласие (`opt_in_marketing = true`)
- [ ] Предоставляйте ссылку на отписку в каждом письме
- [ ] Предоставляйте возможность управления предпочтениями
- [ ] Храните данные только необходимое время
- [ ] Обеспечьте право на удаление данных
- [ ] Документируйте обработку персональных данных
- [ ] Назначьте ответственного за защиту данных (DPO)

---

## 📈 Оптимизация и масштабирование

### Увеличение производительности

1. **Индексы PostgreSQL:**
```sql
CREATE INDEX idx_users_status_verified ON users(status, email_verified);
CREATE INDEX idx_user_preferences_opt_in_industry ON user_preferences(opt_in_marketing, industry);
```

2. **Кэширование:**
   - Используйте Redis для кэширования часто используемых данных
   - Кэшируйте результаты SQL-запросов

3. **Batch Processing:**
   - Используйте узел "Split In Batches" для обработки больших объемов
   - Обрабатывайте по 100-500 записей за раз

### Масштабирование для больших объемов

1. **Horizontal Scaling:**
   - Запустите несколько инстансов n8n
   - Используйте load balancer

2. **Database Optimization:**
   - Используйте read replicas для PostgreSQL
   - Партиционируйте большие таблицы

3. **Email Service:**
   - Используйте профессиональный сервис (SendGrid, Mailgun)
   - Настройте rate limiting

---

## 📚 Дополнительные ресурсы

### Документация
- [n8n Documentation](https://docs.n8n.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SendGrid Documentation](https://docs.sendgrid.com/)

### Сообщество
- [n8n Community Forum](https://community.n8n.io/)
- [n8n Discord](https://discord.gg/n8n)
- [n8n GitHub](https://github.com/n8n-io/n8n)

### Инструменты
- [Cron Expression Generator](https://crontab.guru/)
- [Email Spam Checker](https://www.mail-tester.com/)
- [HTML Email Tester](https://www.emailonacid.com/)
- [UTM Builder](https://ga-dev-tools.web.app/campaign-url-builder/)

---

## 🤝 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте раздел "Устранение неполадок" выше
2. Изучите документацию n8n
3. Задайте вопрос в n8n Community Forum
4. Создайте issue в репозитории

---

**Версия**: 1.0.0  
**Последнее обновление**: 10 февраля 2026  
**Автор**: n8n Customer Acquisition Workflow Team

**Удачи с вашей email-кампанией! 🚀**
