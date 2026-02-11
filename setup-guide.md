# Пошаговое руководство по настройке Email Campaign Workflow

Подробная инструкция по установке и настройке workflow для email-рассылок в n8n.

## 📋 Содержание

1. [Предварительные требования](#предварительные-требования)
2. [Установка n8n](#установка-n8n)
3. [Настройка Google Sheets](#настройка-google-sheets)
4. [Настройка SMTP](#настройка-smtp)
5. [Импорт workflow](#импорт-workflow)
6. [Первый запуск](#первый-запуск)
7. [Устранение неполадок](#устранение-неполадок)

---

## 1. Предварительные требования

### Необходимые аккаунты

- ✅ Google аккаунт (для Google Sheets API)
- ✅ SMTP сервер или аккаунт email-сервиса (Gmail, SendGrid, Mailgun и т.д.)
- ✅ n8n инстанция (локальная или облачная)

### Технические требования

- Node.js 18.x или выше (для локальной установки n8n)
- Docker (опционально, для контейнеризованной установки)
- Браузер с поддержкой современных веб-стандартов

---

## 2. Установка n8n

### Вариант A: Локальная установка через npm

```bash
# Установка n8n глобально
npm install n8n -g

# Запуск n8n
n8n start

# n8n будет доступен по адресу http://localhost:5678
```

### Вариант B: Установка через Docker

```bash
# Создание volume для данных
docker volume create n8n_data

# Запуск контейнера
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# n8n будет доступен по адресу http://localhost:5678
```

### Вариант C: n8n Cloud

1. Перейдите на [n8n.cloud](https://n8n.cloud)
2. Зарегистрируйтесь или войдите в аккаунт
3. Создайте новую инстанцию
4. Дождитесь завершения настройки

---

## 3. Настройка Google Sheets

### Шаг 3.1: Создание проекта в Google Cloud

1. Откройте [Google Cloud Console](https://console.cloud.google.com/)
2. Нажмите "Select a project" → "New Project"
3. Введите название проекта (например, "n8n Email Campaigns")
4. Нажмите "Create"

### Шаг 3.2: Включение Google Sheets API

1. В меню выберите "APIs & Services" → "Library"
2. Найдите "Google Sheets API"
3. Нажмите на него и затем "Enable"

### Шаг 3.3: Создание OAuth 2.0 credentials

1. Перейдите в "APIs & Services" → "Credentials"
2. Нажмите "Create Credentials" → "OAuth client ID"
3. Если требуется, настройте OAuth consent screen:
   - User Type: External
   - App name: n8n Email Campaigns
   - User support email: ваш email
   - Developer contact: ваш email
   - Нажмите "Save and Continue"
   - Scopes: добавьте `.../auth/spreadsheets`
   - Test users: добавьте свой email
4. Вернитесь к созданию OAuth client ID:
   - Application type: Web application
   - Name: n8n
   - Authorized redirect URIs: `http://localhost:5678/rest/oauth2-credential/callback`
     (для n8n Cloud используйте: `https://ваш-домен.app.n8n.cloud/rest/oauth2-credential/callback`)
5. Нажмите "Create"
6. Скопируйте Client ID и Client Secret

### Шаг 3.4: Добавление credentials в n8n

1. В n8n откройте меню → "Settings" → "Credentials"
2. Нажмите "Add Credential"
3. Найдите и выберите "Google Sheets OAuth2 API"
4. Заполните поля:
   - **Credential Name**: Google Sheets account (или любое другое имя)
   - **Client ID**: вставьте скопированный Client ID
   - **Client Secret**: вставьте скопированный Client Secret
5. Нажмите "Connect my account"
6. Авторизуйтесь через Google
7. Разрешите доступ к Google Sheets
8. Нажмите "Save"

### Шаг 3.5: Создание таблицы контактов

1. Откройте [Google Sheets](https://sheets.google.com)
2. Создайте новую таблицу
3. Назовите её "Email Campaign Contacts"
4. Создайте заголовки в первой строке:

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Email | Name | Company | Status | Last Contact | Last Email Sent | Email Status | Error Timestamp | Error Message |

5. Заполните несколько тестовых контактов:

```
john.doe@example.com | John Doe | Acme Corp | Active | 2026-01-15
jane.smith@example.com | Jane Smith | Tech Inc | Active | 2026-01-20
```

6. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/[ЭТО_ID_ТАБЛИЦЫ]/edit
   ```

---

## 4. Настройка SMTP

### Вариант A: Gmail

#### Шаг 4.1: Включение двухфакторной аутентификации

1. Откройте [Google Account Security](https://myaccount.google.com/security)
2. Включите "2-Step Verification"

#### Шаг 4.2: Создание пароля приложения

1. Перейдите в [App Passwords](https://myaccount.google.com/apppasswords)
2. Выберите "Mail" и "Other (Custom name)"
3. Введите "n8n" и нажмите "Generate"
4. Скопируйте сгенерированный пароль (16 символов)

#### Шаг 4.3: Настройка SMTP в n8n

1. В n8n откройте "Settings" → "Credentials"
2. Нажмите "Add Credential"
3. Выберите "SMTP"
4. Заполните поля:
   - **Credential Name**: Gmail SMTP
   - **User**: ваш Gmail адрес (например, yourname@gmail.com)
   - **Password**: пароль приложения из шага 4.2
   - **Host**: smtp.gmail.com
   - **Port**: 587
   - **SSL/TLS**: включено
5. Нажмите "Save"

### Вариант B: SendGrid

#### Шаг 4.1: Создание API ключа

1. Зарегистрируйтесь на [SendGrid](https://sendgrid.com)
2. Перейдите в "Settings" → "API Keys"
3. Нажмите "Create API Key"
4. Выберите "Full Access" или "Mail Send"
5. Скопируйте API ключ

#### Шаг 4.2: Настройка SMTP в n8n

1. В n8n добавьте SMTP credential
2. Заполните:
   - **User**: apikey (буквально слово "apikey")
   - **Password**: ваш API ключ из шага 4.1
   - **Host**: smtp.sendgrid.net
   - **Port**: 587
   - **SSL/TLS**: включено

### Вариант C: Mailgun

#### Шаг 4.1: Получение SMTP credentials

1. Зарегистрируйтесь на [Mailgun](https://mailgun.com)
2. Перейдите в "Sending" → "Domain settings"
3. Выберите ваш домен
4. Найдите "SMTP credentials"

#### Шаг 4.2: Настройка в n8n

1. Добавьте SMTP credential
2. Заполните:
   - **User**: postmaster@ваш-домен.mailgun.org
   - **Password**: SMTP пароль из Mailgun
   - **Host**: smtp.mailgun.org
   - **Port**: 587
   - **SSL/TLS**: включено

### Вариант D: Другие SMTP серверы

| Сервис | Host | Port | SSL/TLS |
|--------|------|------|---------|
| Outlook/Hotmail | smtp-mail.outlook.com | 587 | Да |
| Yahoo | smtp.mail.yahoo.com | 587 | Да |
| Yandex | smtp.yandex.ru | 587 | Да |
| Mail.ru | smtp.mail.ru | 587 | Да |
| Office 365 | smtp.office365.com | 587 | Да |

---

## 5. Импорт workflow

### Шаг 5.1: Скачивание workflow

1. Скачайте файл `email-campaign-workflow.json` из репозитория
2. Сохраните его на своем компьютере

### Шаг 5.2: Импорт в n8n

1. Откройте n8n
2. Нажмите на меню (три линии) в левом верхнем углу
3. Выберите "Import from File"
4. Выберите файл `email-campaign-workflow.json`
5. Нажмите "Import"

### Шаг 5.3: Настройка узлов

#### Узел "Get Email List"

1. Откройте узел двойным кликом
2. В поле "Credential to connect with" выберите созданный Google Sheets credential
3. В поле "Document" выберите вашу таблицу или вставьте ID
4. Убедитесь, что Range установлен на "A:E"
5. Нажмите "Execute Node" для тестирования
6. Если данные загружаются корректно, нажмите "Save"

#### Узел "Send Email"

1. Откройте узел двойным кликом
2. В поле "Credential to connect with" выберите SMTP credential
3. Измените "From Email" на ваш email адрес
4. Проверьте другие настройки
5. Нажмите "Save"

#### Узел "Update Google Sheet"

1. Откройте узел
2. Выберите тот же Google Sheets credential
3. Убедитесь, что Document ID совпадает с вашей таблицей
4. Нажмите "Save"

#### Узел "Send Report"

1. Откройте узел
2. Выберите SMTP credential
3. Измените "To Email" на email администратора
4. Измените "From Email" на ваш email
5. Нажмите "Save"

---

## 6. Первый запуск

### Шаг 6.1: Подготовка тестовых данных

1. Откройте вашу Google Sheets таблицу
2. Добавьте 2-3 тестовых контакта с вашими email адресами
3. Установите Status = "Active" для всех тестовых контактов

Пример:

```
your.email@gmail.com | Тест 1 | Test Company | Active | 2026-02-11
your.email2@gmail.com | Тест 2 | Test Corp | Active | 2026-02-11
```

### Шаг 6.2: Тестовый запуск

1. В n8n откройте импортированный workflow
2. Нажмите "Execute Workflow" в правом верхнем углу
3. Дождитесь завершения выполнения
4. Проверьте результаты:
   - Зеленые галочки на всех узлах = успех
   - Красные крестики = ошибки (см. раздел "Устранение неполадок")

### Шаг 6.3: Проверка результатов

1. **Проверьте почту**: должны прийти тестовые письма
2. **Проверьте Google Sheets**: колонки F и G должны обновиться
3. **Проверьте отчет**: на email администратора должен прийти отчет

### Шаг 6.4: Анализ выполнения

1. Кликните на каждый узел для просмотра данных
2. Проверьте, что персонализация работает корректно
3. Убедитесь, что все ссылки в письмах рабочие

---

## 7. Устранение неполадок

### Проблема: "Ошибка подключения к Google Sheets"

**Решение:**

1. Проверьте, что Google Sheets API включен в Google Cloud Console
2. Убедитесь, что OAuth credentials настроены правильно
3. Попробуйте переподключить credential в n8n:
   - Откройте credential
   - Нажмите "Reconnect"
   - Авторизуйтесь заново
4. Проверьте, что у вас есть доступ к таблице

### Проблема: "Ошибка отправки email"

**Решение для Gmail:**

1. Убедитесь, что используете пароль приложения, а не обычный пароль
2. Проверьте, что двухфакторная аутентификация включена
3. Проверьте настройки:
   - Host: smtp.gmail.com
   - Port: 587
   - SSL/TLS: включено

**Решение для других SMTP:**

1. Проверьте правильность host и port
2. Убедитесь, что учетные данные верны
3. Проверьте лимиты отправки вашего провайдера
4. Попробуйте другой порт (например, 465 вместо 587)

### Проблема: "Письма попадают в спам"

**Решение:**

1. Настройте SPF запись для вашего домена:
   ```
   v=spf1 include:_spf.google.com ~all
   ```

2. Настройте DKIM (в настройках вашего SMTP провайдера)

3. Настройте DMARC запись:
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
   ```

4. Используйте профессиональный email адрес (не @gmail.com)

5. Избегайте спам-слов в теме и тексте:
   - "Бесплатно", "Заработок", "Кредит"
   - Множественные восклицательные знаки
   - Полностью заглавные буквы

### Проблема: "Workflow выполняется слишком долго"

**Решение:**

1. Уменьшите размер партии в узле "Split In Batches"
2. Уменьшите время ожидания в узле "Wait Between Batches"
3. Проверьте скорость интернет-соединения
4. Убедитесь, что SMTP сервер не ограничивает скорость

### Проблема: "Персонализация не работает"

**Решение:**

1. Проверьте, что названия колонок в Google Sheets совпадают с кодом
2. Убедитесь, что в узле "Personalize Emails" используются правильные переменные:
   - `$json.Email` (с заглавной E)
   - `$json.Name` (с заглавной N)
   - `$json.Company` (с заглавной C)
3. Проверьте, что данные корректно загружаются из Google Sheets

### Проблема: "Ошибка 'Cannot read property of undefined'"

**Решение:**

1. Проверьте, что все обязательные колонки заполнены в Google Sheets
2. Добавьте проверки в код узла "Personalize Emails":
   ```javascript
   const name = item.json.Name || 'Уважаемый клиент';
   const company = item.json.Company || '';
   ```

### Проблема: "Workflow не запускается по расписанию"

**Решение:**

1. Убедитесь, что workflow активирован (переключатель в правом верхнем углу)
2. Проверьте настройки триггера Cron
3. Убедитесь, что n8n запущен и работает
4. Проверьте логи n8n:
   ```bash
   # Для Docker
   docker logs n8n
   
   # Для npm
   ~/.n8n/logs/
   ```

---

## 📊 Мониторинг и оптимизация

### Отслеживание метрик

Рекомендуется отслеживать:

1. **Delivery Rate** - процент доставленных писем
2. **Open Rate** - процент открытых писем
3. **Click Rate** - процент кликов по ссылкам
4. **Unsubscribe Rate** - процент отписок
5. **Bounce Rate** - процент недоставленных писем

### Оптимизация производительности

1. **Батчинг**: отправляйте письма партиями по 10-50 штук
2. **Тайминг**: выбирайте оптимальное время отправки (обычно 9-11 утра)
3. **Частота**: не отправляйте слишком часто (максимум 1-2 раза в неделю)
4. **Сегментация**: разделяйте аудиторию на группы для таргетированных рассылок

---

## 🔐 Безопасность

### Рекомендации по безопасности

1. **Не храните credentials в коде** - используйте n8n credentials manager
2. **Используйте environment variables** для чувствительных данных
3. **Регулярно обновляйте пароли** SMTP и API ключи
4. **Ограничьте доступ** к n8n инстанции (используйте аутентификацию)
5. **Используйте HTTPS** для production окружения
6. **Делайте бэкапы** workflow и credentials

### Настройка аутентификации в n8n

Для production окружения:

```bash
# Установите переменные окружения
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=your_secure_password

# Перезапустите n8n
```

---

## 📈 Следующие шаги

После успешной настройки:

1. ✅ Изучите [email-templates.md](email-templates.md) для готовых шаблонов
2. ✅ Настройте автоматический запуск по расписанию
3. ✅ Интегрируйте с вашей CRM системой
4. ✅ Добавьте A/B тестирование
5. ✅ Настройте отслеживание открытий и кликов
6. ✅ Создайте сегменты аудитории для таргетированных рассылок

---

## 🆘 Получение помощи

Если у вас возникли проблемы:

1. Проверьте [официальную документацию n8n](https://docs.n8n.io/)
2. Посетите [форум сообщества n8n](https://community.n8n.io/)
3. Проверьте [GitHub Issues](https://github.com/n8n-io/n8n/issues)
4. Создайте issue в репозитории этого проекта

---

**Поздравляем!** Вы успешно настроили email campaign workflow для n8n. 🎉
