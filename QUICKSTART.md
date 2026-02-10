# Быстрый старт

Пошаговая инструкция для запуска VK Auto Posting с n8n за 15 минут.

## Шаг 1: Запуск n8n (5 минут)

### Вариант A: Docker Compose (рекомендуется)

```bash
# 1. Скопируйте пример конфигурации
cp .env.example .env

# 2. Отредактируйте .env файл
nano .env  # или используйте любой редактор

# 3. Запустите n8n
docker-compose up -d

# 4. Откройте в браузере
# http://localhost:5678
```

### Вариант B: NPM

```bash
# 1. Установите n8n глобально
npm install n8n -g

# 2. Запустите n8n
n8n start

# 3. Откройте в браузере
# http://localhost:5678
```

## Шаг 2: Получение VK Access Token (5 минут)

### Для группы (рекомендуется):

1. Откройте вашу группу ВКонтакте
2. Перейдите в **Управление** → **Работа с API**
3. Нажмите **Создать ключ**
4. Выберите права:
   - ✅ Управление сообществом
   - ✅ Фотографии
   - ✅ Создание опросов
5. Скопируйте полученный токен
6. Найдите ID группы в URL: `vk.com/club123456789` → ID = `-123456789`

### Для Standalone приложения:

1. Перейдите на https://vk.com/apps?act=manage
2. Нажмите **Создать приложение**
3. Выберите **Standalone приложение**
4. После создания перейдите в **Настройки**
5. Получите токен через OAuth: https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&scope=photos,wall,polls&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token

## Шаг 3: Настройка Google Sheets (3 минуты)

1. Создайте новую Google Sheets таблицу
2. Скопируйте содержимое файла `google-sheets-template.csv`
3. Вставьте в первый лист таблицы
4. Скопируйте ID таблицы из URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_FILE_ID_HERE/edit
   ```

## Шаг 4: Импорт и настройка Workflow (2 минуты)

1. Откройте n8n в браузере
2. Нажмите **+** → **Import from File**
3. Выберите файл `vk-n8n-workflow.json`
4. Настройте credentials:

### VK API Credentials:

- Тип: **HTTP Query Auth**
- Имя: `VK API Credentials`
- Параметры:
  - Name: `access_token`
  - Value: ваш VK токен
- Custom fields:
  - Name: `vkGroupId`
  - Value: ваш Group ID (например: `-123456789`)

### Google Sheets Credentials:

- Тип: **Google Sheets OAuth2 API**
- Следуйте инструкциям для подключения Google аккаунта

5. В узле "Read Posts from Google Sheets" укажите:
   - File ID: ID вашей таблицы
   - Sheet: `Sheet1`

## Шаг 5: Тестирование и активация

1. Нажмите **Execute Workflow** для тестового запуска
2. Проверьте результаты в каждом узле
3. Если все работает - активируйте workflow переключателем **Active**

## Готово! 🎉

Теперь workflow будет автоматически проверять Google Sheets каждый час и публиковать готовые посты в вашу группу VK.

## Быстрые примеры использования

### Опубликовать текстовый пост через 1 час:

Добавьте в Google Sheets:
```
post_date: 2026-02-10 13:00:00
post_type: text
content: Мой первый автоматический пост!
published: false
```

### Опубликовать изображение:

```
post_date: 2026-02-10 14:00:00
post_type: image
content: Красивое фото!
image_url: https://picsum.photos/800/600
published: false
```

### Создать опрос:

```
post_date: 2026-02-10 15:00:00
post_type: poll
poll_question: Какой ваш любимый цвет?
poll_options: Красный|Синий|Зеленый|Желтый
published: false
```

## Частые вопросы

**Q: Как изменить частоту проверки?**
A: В узле "Schedule Trigger" измените interval (например, на 30 минут или используйте Cron).

**Q: Можно ли публиковать сразу?**
A: Да, установите `post_date` на текущее время или прошедшее.

**Q: Как отменить запланированную публикацию?**
A: Измените `published` на `true` или удалите строку из таблицы.

**Q: Workflow не публикует посты**
A: Проверьте:
1. Workflow активирован (переключатель Active)
2. `post_date` <= текущее время
3. `published` = `false`
4. Credentials настроены правильно

## Дополнительная информация

Полная документация: [README.md](README.md)

## Поддержка

Если что-то не работает:
1. Проверьте логи в разделе "Executions"
2. Убедитесь, что все credentials настроены
3. Проверьте формат данных в Google Sheets
4. Создайте Issue в репозитории с описанием проблемы
