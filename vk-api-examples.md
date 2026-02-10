# VK API Examples

Примеры использования VK API для различных сценариев публикации.

## Базовые примеры

### 1. Простой текстовый пост

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Привет, мир!" \
  -d "from_group=1"
```

### 2. Пост с изображением

#### Шаг 1: Получить upload URL

```bash
curl "https://api.vk.com/method/photos.getWallUploadServer" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "group_id=123456789"
```

Ответ:
```json
{
  "response": {
    "upload_url": "https://pu.vk.com/c123456/upload.php?...",
    "album_id": -7,
    "user_id": 123456789
  }
}
```

#### Шаг 2: Загрузить фото

```bash
curl -X POST "UPLOAD_URL_FROM_STEP_1" \
  -F "photo=@/path/to/image.jpg"
```

Ответ:
```json
{
  "server": 123456,
  "photo": "[]",
  "hash": "abc123..."
}
```

#### Шаг 3: Сохранить фото

```bash
curl "https://api.vk.com/method/photos.saveWallPhoto" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "group_id=123456789" \
  -d "photo=PHOTO_FROM_STEP_2" \
  -d "server=SERVER_FROM_STEP_2" \
  -d "hash=HASH_FROM_STEP_2"
```

Ответ:
```json
{
  "response": [
    {
      "id": 456789,
      "album_id": -7,
      "owner_id": -123456789,
      "sizes": [...]
    }
  ]
}
```

#### Шаг 4: Опубликовать пост с фото

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Посмотрите на это фото!" \
  -d "attachments=photo-123456789_456789" \
  -d "from_group=1"
```

### 3. Создание и публикация опроса

#### Шаг 1: Создать опрос

```bash
curl "https://api.vk.com/method/polls.create" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "question=Какой ваш любимый язык программирования?" \
  -d "add_answers=[\"Python\",\"JavaScript\",\"Go\",\"Rust\"]" \
  -d "owner_id=-123456789"
```

Ответ:
```json
{
  "response": {
    "id": 789012,
    "owner_id": -123456789,
    "created": 1707566400,
    "question": "Какой ваш любимый язык программирования?",
    "votes": 0,
    "answers": [...]
  }
}
```

#### Шаг 2: Опубликовать пост с опросом

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Пройдите наш опрос!" \
  -d "attachments=poll-123456789_789012" \
  -d "from_group=1"
```

## Продвинутые примеры

### 4. Отложенная публикация

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Этот пост будет опубликован позже" \
  -d "publish_date=1707566400" \
  -d "from_group=1"
```

### 5. Пост с несколькими изображениями

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Галерея фотографий" \
  -d "attachments=photo-123_456,photo-123_457,photo-123_458" \
  -d "from_group=1"
```

### 6. Пост с ссылкой

```bash
curl -X POST "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Интересная статья" \
  -d "attachments=https://example.com/article" \
  -d "from_group=1"
```

### 7. Закрепление поста

```bash
curl "https://api.vk.com/method/wall.pin" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "post_id=12345"
```

### 8. Удаление поста

```bash
curl "https://api.vk.com/method/wall.delete" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "post_id=12345"
```

## Полезные методы API

### Получить информацию о группе

```bash
curl "https://api.vk.com/method/groups.getById" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "group_id=123456789"
```

### Получить последние посты группы

```bash
curl "https://api.vk.com/method/wall.get" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "count=10"
```

### Получить статистику поста

```bash
curl "https://api.vk.com/method/wall.getById" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "posts=-123456789_12345"
```

## Обработка ошибок

### Типичные коды ошибок:

- **5**: Authorization failed - неверный access token
- **15**: Access denied - недостаточно прав
- **100**: One of the parameters specified was missing or invalid - неверные параметры
- **214**: Access to adding post denied - нет прав на публикацию
- **219**: Advertisement post was recently added - слишком частые публикации

### Пример обработки ошибок:

```bash
response=$(curl -s "https://api.vk.com/method/wall.post" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "owner_id=-123456789" \
  -d "message=Test")

if echo "$response" | grep -q "error"; then
  echo "Error occurred:"
  echo "$response" | jq '.error'
else
  echo "Success:"
  echo "$response" | jq '.response'
fi
```

## Лимиты API

- **Запросы в секунду**: 3 запроса/сек для пользователя, 20 запросов/сек для сообщества
- **Размер изображения**: до 50 МБ
- **Количество вариантов в опросе**: от 2 до 10
- **Длина текста поста**: до 16384 символов
- **Количество вложений**: до 10

## Рекомендации

1. **Используйте батчинг** для множественных запросов:

```bash
curl "https://api.vk.com/method/execute" \
  -d "access_token=YOUR_TOKEN" \
  -d "v=5.131" \
  -d "code=return [API.wall.post({...}), API.wall.post({...})];"
```

2. **Кэшируйте upload URL** для загрузки нескольких фото

3. **Проверяйте ответы** на наличие ошибок перед следующим шагом

4. **Используйте exponential backoff** при ошибках rate limit

## Дополнительные ресурсы

- [VK API Documentation](https://dev.vk.com/reference)
- [VK API Explorer](https://dev.vk.com/method)
- [Community API Guide](https://dev.vk.com/ru/api/community-messages/getting-started)

## Примеры для n8n

Все эти примеры можно использовать в узлах HTTP Request в n8n. Просто замените curl команды на соответствующие параметры узла:

- URL: `https://api.vk.com/method/METHOD_NAME`
- Method: `POST` или `GET`
- Query Parameters: все параметры из `-d`
- Authentication: HTTP Query Auth с вашим токеном
