# 🚀 Быстрый старт

Это краткое руководство поможет вам запустить workflow для Telegram за 5 минут.

## Шаг 1: Создайте Telegram бота (2 минуты)

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду: `/newbot`
3. Придумайте имя бота (например: "My Group Bot")
4. Придумайте username (например: "my_group_bot")
5. Сохраните полученный **Bot Token**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

## Шаг 2: Добавьте бота в группу (1 минута)

1. Откройте вашу Telegram группу
2. Нажмите на название группы → **Add Members**
3. Найдите вашего бота и добавьте его
4. Сделайте бота администратором:
   - Нажмите на название группы → **Administrators**
   - Нажмите **Add Administrator**
   - Выберите вашего бота
   - Включите право **Post Messages**

## Шаг 3: Получите Chat ID группы (1 минута)

1. Отправьте любое сообщение в группу
2. Откройте в браузере (замените `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Найдите в ответе: `"chat":{"id":-1001234567890}`
4. Сохраните этот **Chat ID**: `-1001234567890`

## Шаг 4: Запустите n8n (1 минута)

### Вариант A: Docker (рекомендуется)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Вариант B: npm

```bash
npx n8n
```

Откройте: http://localhost:5678

## Шаг 5: Импортируйте workflow (30 секунд)

1. В n8n нажмите **☰** (меню) → **Import from File**
2. Выберите файл: `telegram_group_posting_workflow.json`
3. Нажмите **Import**

## Шаг 6: Настройте credentials (30 секунд)

1. Нажмите на узел **Send Telegram Message**
2. В поле **Credentials** нажмите **Create New**
3. Выберите **Telegram API**
4. Вставьте ваш **Bot Token**
5. Нажмите **Save**

## Шаг 7: Настройте Chat ID (30 секунд)

1. Нажмите на узел **Set Message Data**
2. Измените значение `chatId` на ваш Chat ID
3. При желании измените текст сообщения

## Шаг 8: Тест! (10 секунд)

1. Нажмите **Execute Workflow**
2. Проверьте вашу Telegram группу - должно появиться сообщение! 🎉

---

## Что дальше?

### Хотите автоматические посты по расписанию?

Импортируйте `telegram_scheduled_posting_workflow.json` и настройте расписание в узле **Schedule Trigger**.

### Хотите интеграцию через API?

Импортируйте `telegram_webhook_posting_workflow.json` и используйте webhook для отправки сообщений из внешних систем.

### Нужна помощь?

Читайте полную документацию в [README.md](README.md)

---

**Готово!** Теперь вы можете автоматизировать посты в вашей Telegram группе! 🚀
