# 🚀 Quick Start Guide - n8n Email Campaign

Быстрый старт для запуска email-рассылки за 15 минут.

## ⚡ Минимальная настройка

### Шаг 1: Установите n8n (2 минуты)

```bash
# Вариант 1: Docker (рекомендуется)
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# Вариант 2: npm
npm install n8n -g
n8n start
```

Откройте http://localhost:5678

### Шаг 2: Импортируйте workflow (1 минута)

1. В n8n: Menu → Import from File
2. Выберите `email-campaign-workflow.json`
3. Нажмите Import

### Шаг 3: Настройте Google Sheets (5 минут)

#### 3.1 Создайте таблицу

1. Откройте [Google Sheets](https://sheets.google.com)
2. Создайте новую таблицу
3. Скопируйте структуру из `google-sheets-template.csv`:

```
Email | Name | Company | Status | Last Contact
your@email.com | Your Name | Test Company | Active | 2026-02-11
```

4. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/[ЭТОТ_ID]/edit
   ```

#### 3.2 Настройте доступ

1. В n8n: Settings → Credentials → Add Credential
2. Выберите "Google Sheets OAuth2 API"
3. Следуйте инструкциям для авторизации

**Быстрый способ (для тестирования):**
- Сделайте таблицу публичной: Share → Anyone with the link can view

### Шаг 4: Настройте SMTP (5 минут)

#### Для Gmail:

1. Включите [2FA](https://myaccount.google.com/security)
2. Создайте [App Password](https://myaccount.google.com/apppasswords)
3. В n8n: Settings → Credentials → Add Credential → SMTP
4. Заполните:
   - User: ваш Gmail
   - Password: пароль приложения (16 символов)
   - Host: smtp.gmail.com
   - Port: 587
   - SSL/TLS: включено

#### Альтернативы:

**SendGrid (бесплатно до 100 писем/день):**
```
User: apikey
Password: ваш API ключ
Host: smtp.sendgrid.net
Port: 587
```

**Mailgun (бесплатно до 5000 писем/месяц):**
```
User: postmaster@ваш-домен.mailgun.org
Password: SMTP пароль
Host: smtp.mailgun.org
Port: 587
```

### Шаг 5: Настройте workflow (2 минуты)

1. Откройте узел "Get Email List"
   - Выберите ваш Google Sheets credential
   - Вставьте ID таблицы
   - Сохраните

2. Откройте узел "Send Email"
   - Выберите SMTP credential
   - Измените "From Email" на ваш email
   - Сохраните

3. Откройте узел "Send Report"
   - Измените "To Email" на ваш email
   - Сохраните

### Шаг 6: Тестовый запуск (1 минута)

1. Убедитесь, что в Google Sheets есть хотя бы 1 контакт со статусом "Active"
2. В n8n нажмите "Execute Workflow"
3. Проверьте почту - должно прийти письмо и отчет

## ✅ Готово!

Ваша первая email-рассылка отправлена!

---

## 🎨 Быстрая кастомизация

### Изменить текст письма

Откройте узел "Personalize Emails" → измените переменную `body`:

```javascript
const body = `
  <html>
    <body style="font-family: Arial; padding: 20px;">
      <h1>Привет, ${name}!</h1>
      <p>Ваше сообщение здесь.</p>
      <a href="https://example.com" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
        Кнопка действия
      </a>
    </body>
  </html>
`;
```

### Изменить тему письма

В том же узле измените:

```javascript
const subject = `Ваша тема письма для ${company}`;
```

### Использовать готовый шаблон

1. Откройте `email-templates.md`
2. Выберите понравившийся шаблон
3. Скопируйте HTML код
4. Вставьте в переменную `body` в узле "Personalize Emails"

---

## 🔄 Автоматический запуск

### По расписанию (например, каждый понедельник в 10:00)

1. Удалите узел "Manual Trigger"
2. Добавьте узел "Schedule Trigger"
3. Настройте:
   - Rule: `0 10 * * 1` (каждый понедельник в 10:00)
   - Timezone: Europe/Moscow
4. Подключите к узлу "Get Email List"
5. Активируйте workflow (переключатель в правом верхнем углу)

### По событию (новый контакт в Google Sheets)

1. Используйте "Google Sheets Trigger"
2. Настройте отслеживание новых строк
3. Workflow запустится автоматически при добавлении контакта

---

## 📊 Мониторинг

### Просмотр истории выполнений

1. В n8n: Menu → Executions
2. Кликните на любое выполнение для просмотра деталей
3. Проверьте данные в каждом узле

### Проверка результатов в Google Sheets

После отправки проверьте колонки:
- **F (Last Email Sent)**: дата отправки
- **G (Email Status)**: статус (sent/failed)
- **H-I**: информация об ошибках (если были)

---

## 🐛 Быстрое решение проблем

### Письма не отправляются

```bash
# Проверьте SMTP настройки
1. Откройте узел "Send Email"
2. Нажмите "Test Step"
3. Проверьте ошибку в выводе
```

**Частые причины:**
- ❌ Неверный пароль → используйте App Password для Gmail
- ❌ Неверный порт → попробуйте 587 или 465
- ❌ Блокировка файрволом → проверьте настройки сети

### Google Sheets не читается

```bash
# Проверьте доступ
1. Откройте таблицу в браузере
2. Убедитесь, что у вас есть доступ
3. Проверьте правильность ID таблицы
```

**Быстрое решение:**
- Сделайте таблицу публичной для тестирования

### Персонализация не работает

```bash
# Проверьте названия колонок
1. В Google Sheets колонки должны быть: Email, Name, Company, Status
2. Названия с заглавной буквы
3. Без лишних пробелов
```

---

## 📚 Что дальше?

### Изучите документацию:

1. **README.md** - полное описание проекта
2. **setup-guide.md** - детальная настройка
3. **best-practices.md** - лучшие практики email-маркетинга
4. **email-templates.md** - готовые шаблоны писем

### Улучшите workflow:

- ✨ Добавьте A/B тестирование
- 📊 Настройте отслеживание открытий
- 🎯 Создайте сегменты аудитории
- 🔄 Настройте drip-кампании
- 📧 Интегрируйте с CRM

### Присоединяйтесь к сообществу:

- [n8n Community Forum](https://community.n8n.io/)
- [n8n Discord](https://discord.gg/n8n)
- [n8n GitHub](https://github.com/n8n-io/n8n)

---

## 💡 Полезные советы

### Тестирование

Всегда тестируйте на себе перед массовой рассылкой:
1. Добавьте свой email в Google Sheets
2. Установите Status = "Active"
3. Запустите workflow
4. Проверьте письмо на разных устройствах

### Безопасность

- 🔒 Никогда не коммитьте credentials в Git
- 🔑 Используйте App Passwords вместо основного пароля
- 🛡️ Регулярно меняйте API ключи
- 📝 Делайте бэкапы workflow

### Производительность

- 📦 Отправляйте партиями по 10-50 писем
- ⏱️ Добавляйте паузы между партиями
- 📊 Мониторьте bounce rate
- 🚫 Удаляйте недействительные email адреса

---

## 🎯 Чек-лист первого запуска

```
□ n8n установлен и запущен
□ Workflow импортирован
□ Google Sheets таблица создана
□ Google Sheets credential настроен
□ SMTP credential настроен
□ Узлы workflow настроены
□ Тестовый контакт добавлен
□ Тестовая отправка выполнена
□ Письмо получено и проверено
□ Отчет получен
□ Google Sheets обновлен
```

---

## 🆘 Нужна помощь?

1. Проверьте [setup-guide.md](setup-guide.md) для детальных инструкций
2. Посмотрите раздел "Устранение неполадок" в setup-guide.md
3. Создайте issue в репозитории
4. Спросите в [n8n Community](https://community.n8n.io/)

---

**Время на настройку:** ~15 минут  
**Сложность:** Легко  
**Требуется опыт:** Не требуется

Удачи с вашими email-кампаниями! 🚀
