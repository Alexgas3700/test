# Руководство по устранению неполадок

Решения распространенных проблем при работе с VK Post Workflow для n8n.

## Содержание

1. [Проблемы с аутентификацией](#проблемы-с-аутентификацией)
2. [Проблемы с загрузкой изображений](#проблемы-с-загрузкой-изображений)
3. [Проблемы с публикацией постов](#проблемы-с-публикацией-постов)
4. [Проблемы с workflow](#проблемы-с-workflow)
5. [Проблемы производительности](#проблемы-производительности)

---

## Проблемы с аутентификацией

### Ошибка: "Invalid access token"

**Симптомы:**
```
Error: Invalid access token
Code: 5
```

**Возможные причины:**
1. Токен истек
2. Токен был отозван пользователем
3. Токен скопирован неполностью
4. Неправильный формат токена

**Решения:**

#### Решение 1: Получите новый токен
```bash
# Используйте OAuth2 URL для получения нового токена
https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,wall,groups,offline&response_type=token&v=5.131
```

#### Решение 2: Проверьте credential в n8n
1. Откройте **Credentials** в n8n
2. Найдите VK credential
3. Нажмите **"Reconnect"** или создайте новый
4. Убедитесь, что авторизация прошла успешно

#### Решение 3: Проверьте формат токена
- Токен должен содержать только буквы и цифры
- Длина токена обычно 85+ символов
- Не должно быть пробелов в начале/конце

---

### Ошибка: "User authorization failed"

**Симптомы:**
```
Error: User authorization failed: invalid client_id
```

**Возможные причины:**
1. Неправильный App ID
2. Приложение удалено или заблокировано
3. Неправильные настройки приложения

**Решения:**

#### Решение 1: Проверьте App ID
1. Откройте [VK Developers](https://dev.vk.com/)
2. Найдите ваше приложение
3. Скопируйте **ID приложения** (App ID)
4. Обновите credential в n8n

#### Решение 2: Проверьте статус приложения
1. Убедитесь, что приложение активно
2. Проверьте, нет ли блокировок
3. Проверьте настройки приложения

---

### Ошибка: "Access denied"

**Симптомы:**
```
Error: Access denied
Code: 15
```

**Возможные причины:**
1. Недостаточно прав у токена
2. Нет прав администратора группы
3. Группа заблокирована

**Решения:**

#### Решение 1: Проверьте scope токена
```bash
# Проверьте права токена
curl "https://api.vk.com/method/account.getAppPermissions?access_token=YOUR_TOKEN&v=5.131"
```

Необходимые права:
- `photos` (8192)
- `wall` (8192)
- `groups` (262144)

#### Решение 2: Проверьте права в группе
1. Откройте группу VK
2. Перейдите в **"Управление"** → **"Участники"**
3. Убедитесь, что вы **администратор** или **редактор**

#### Решение 3: Получите токен с правильными правами
```
scope=photos,wall,groups,offline
```

---

## Проблемы с загрузкой изображений

### Ошибка: "Failed to download image"

**Симптомы:**
```
Error: Request failed with status code 404
```

**Возможные причины:**
1. URL изображения недоступен
2. Изображение удалено
3. Требуется авторизация для доступа
4. Таймаут соединения

**Решения:**

#### Решение 1: Проверьте URL
```bash
# Проверьте доступность изображения
curl -I "https://example.com/image.jpg"
```

Должен вернуться статус `200 OK`.

#### Решение 2: Увеличьте таймаут
В узле **Download Image** добавьте опции:
```json
{
  "timeout": 60000
}
```

#### Решение 3: Используйте прямую ссылку
- Убедитесь, что URL ведет напрямую к файлу
- Избегайте сокращенных ссылок (bit.ly и т.д.)
- Проверьте, что URL начинается с `https://`

---

### Ошибка: "Photo upload failed"

**Симптомы:**
```
Error: Photo upload failed
Code: 129
```

**Возможные причины:**
1. Неподдерживаемый формат изображения
2. Размер файла превышает лимит
3. Изображение повреждено
4. Проблемы с сервером VK

**Решения:**

#### Решение 1: Проверьте формат изображения
Поддерживаемые форматы:
- JPG/JPEG
- PNG
- GIF

#### Решение 2: Проверьте размер файла
```javascript
// Добавьте узел Function перед загрузкой
const binary = $input.first().binary.data;
const sizeInMB = binary.length / (1024 * 1024);

if (sizeInMB > 50) {
  throw new Error(`Image too large: ${sizeInMB.toFixed(2)} MB`);
}

return $input.all();
```

#### Решение 3: Оптимизируйте изображение
Добавьте узел **Edit Image** перед загрузкой:
```json
{
  "operation": "resize",
  "width": 1200,
  "quality": 85,
  "format": "jpeg"
}
```

---

### Ошибка: "Invalid image"

**Симптомы:**
```
Error: Invalid image
```

**Возможные причины:**
1. Файл не является изображением
2. Изображение повреждено
3. Неправильный MIME type

**Решения:**

#### Решение 1: Проверьте MIME type
```javascript
// Узел Function
const binary = $input.first().binary;
console.log('MIME type:', binary.mimeType);

if (!binary.mimeType.startsWith('image/')) {
  throw new Error('File is not an image');
}

return $input.all();
```

#### Решение 2: Конвертируйте изображение
Используйте узел **Edit Image** для конвертации:
```json
{
  "operation": "convert",
  "format": "jpeg"
}
```

---

## Проблемы с публикацией постов

### Ошибка: "Invalid group_id"

**Симптомы:**
```
Error: Invalid group_id
Code: 125
```

**Возможные причины:**
1. Неправильный формат ID
2. Группа не существует
3. Нет доступа к группе

**Решения:**

#### Решение 1: Проверьте формат ID
```javascript
// ID должен быть только цифрами
const groupId = "123456789"; // ✅ Правильно
const groupId = "club123456789"; // ❌ Неправильно
const groupId = "mygroup"; // ❌ Неправильно
```

#### Решение 2: Получите ID группы
```bash
# Используйте API для получения ID
curl "https://api.vk.com/method/groups.getById?group_id=mygroup&access_token=YOUR_TOKEN&v=5.131"
```

#### Решение 3: Проверьте доступ к группе
```bash
# Проверьте, что вы можете получить информацию о группе
curl "https://api.vk.com/method/groups.getById?group_id=123456789&access_token=YOUR_TOKEN&v=5.131"
```

---

### Ошибка: "Captcha needed"

**Симптомы:**
```
Error: Captcha needed
Code: 14
```

**Возможные причины:**
1. Подозрительная активность
2. Слишком много запросов
3. VK требует подтверждение

**Решения:**

#### Решение 1: Уменьшите частоту запросов
Добавьте узел **Wait** между запросами:
```json
{
  "unit": "seconds",
  "amount": 5
}
```

#### Решение 2: Используйте OAuth2
- OAuth2 токены реже вызывают капчу
- Пересоздайте credential с OAuth2

#### Решение 3: Подождите
- Подождите 30-60 минут
- Затем попробуйте снова

---

### Ошибка: "Too many requests per second"

**Симптомы:**
```
Error: Too many requests per second
Code: 6
```

**Возможные причины:**
1. Превышен лимит запросов (3/сек для пользователя)
2. Множественные параллельные запросы

**Решения:**

#### Решение 1: Добавьте задержки
```javascript
// Узел Function перед VK запросом
await new Promise(resolve => setTimeout(resolve, 1000));
return $input.all();
```

#### Решение 2: Используйте батчинг
Вместо множественных запросов используйте один:
```javascript
// Объедините несколько операций в один запрос
const code = `
  var photos = API.photos.getWallUploadServer({"group_id": ${groupId}});
  var post = API.wall.post({"owner_id": -${groupId}, "message": "${text}"});
  return {"photos": photos, "post": post};
`;
```

#### Решение 3: Используйте очередь
Добавьте узел **Split In Batches** с задержкой:
```json
{
  "batchSize": 1,
  "options": {
    "reset": false
  }
}
```

---

## Проблемы с workflow

### Workflow не запускается

**Возможные причины:**
1. Workflow не активирован
2. Ошибка в триггере
3. Недостаточно ресурсов

**Решения:**

#### Решение 1: Активируйте workflow
1. Откройте workflow
2. Переключите тумблер **"Active"** в положение ON
3. Проверьте, что нет ошибок

#### Решение 2: Проверьте триггер
- Для **Manual Trigger**: нажмите "Execute Workflow"
- Для **Schedule Trigger**: проверьте cron выражение
- Для **Webhook**: проверьте URL и метод

#### Решение 3: Проверьте логи
```bash
# Если n8n запущен в Docker
docker logs n8n

# Или проверьте в UI
# Settings → Executions → View Failed
```

---

### Workflow выполняется частично

**Возможные причины:**
1. Ошибка в одном из узлов
2. Неправильные соединения
3. Условие не выполнено

**Решения:**

#### Решение 1: Проверьте каждый узел
1. Откройте workflow
2. Нажмите "Execute Workflow"
3. Проверьте данные на каждом узле (кликните на узел → View Details)

#### Решение 2: Включите "Continue On Fail"
В настройках узла:
```json
{
  "continueOnFail": true,
  "alwaysOutputData": true
}
```

#### Решение 3: Добавьте логирование
```javascript
// Узел Function для отладки
console.log('Input data:', JSON.stringify($input.all(), null, 2));
return $input.all();
```

---

### Данные не передаются между узлами

**Возможные причины:**
1. Неправильные выражения
2. Пустые данные
3. Неправильный путь к данным

**Решения:**

#### Решение 1: Проверьте выражения
```javascript
// Неправильно
{{ $json.data }}

// Правильно
={{ $json.data }}
```

#### Решение 2: Проверьте структуру данных
```javascript
// Узел Function
console.log('Available data:', Object.keys($json));
console.log('Full data:', JSON.stringify($json, null, 2));
return $input.all();
```

#### Решение 3: Используйте правильный синтаксис
```javascript
// Получить данные из предыдущего узла
={{ $json.fieldName }}

// Получить данные из конкретного узла
={{ $('Node Name').item.json.fieldName }}

// Получить все элементы
={{ $input.all() }}
```

---

## Проблемы производительности

### Workflow выполняется медленно

**Возможные причины:**
1. Большие изображения
2. Медленная сеть
3. Много последовательных запросов

**Решения:**

#### Решение 1: Оптимизируйте изображения
```json
{
  "operation": "resize",
  "width": 1200,
  "quality": 80
}
```

#### Решение 2: Используйте параллельные запросы
Вместо последовательных запросов используйте **Split In Batches** с параллельной обработкой.

#### Решение 3: Кешируйте данные
Используйте узел **Cache** для хранения часто используемых данных.

---

### Workflow падает с таймаутом

**Возможные причины:**
1. Слишком долгая операция
2. Зависание на узле
3. Недостаточный таймаут

**Решения:**

#### Решение 1: Увеличьте таймаут
В настройках workflow:
```json
{
  "executionTimeout": 300
}
```

В настройках узла HTTP Request:
```json
{
  "timeout": 60000
}
```

#### Решение 2: Разбейте на части
Разделите большой workflow на несколько меньших с помощью **Execute Workflow** узла.

#### Решение 3: Используйте фоновое выполнение
Для длительных операций используйте **Wait** узел с webhook callback.

---

## Общие советы по отладке

### 1. Включите подробное логирование

В настройках n8n:
```bash
export N8N_LOG_LEVEL=debug
export N8N_LOG_OUTPUT=console,file
```

### 2. Используйте узел Function для отладки

```javascript
// Логирование данных
console.log('=== DEBUG START ===');
console.log('Input:', JSON.stringify($input.all(), null, 2));
console.log('JSON:', JSON.stringify($json, null, 2));
console.log('=== DEBUG END ===');

return $input.all();
```

### 3. Проверяйте данные на каждом шаге

1. Выполните workflow
2. Кликните на каждый узел
3. Нажмите **"View Details"**
4. Проверьте входные и выходные данные

### 4. Используйте Try-Catch

```javascript
try {
  // Ваш код
  const result = someOperation();
  return { success: true, data: result };
} catch (error) {
  console.error('Error:', error.message);
  return { success: false, error: error.message };
}
```

### 5. Тестируйте по частям

1. Отключите часть узлов
2. Протестируйте оставшуюся часть
3. Постепенно добавляйте узлы обратно
4. Найдите проблемный узел

---

## Полезные команды для диагностики

### Проверка доступности VK API

```bash
curl -I "https://api.vk.com/method/users.get?v=5.131"
```

### Проверка токена

```bash
curl "https://api.vk.com/method/users.get?access_token=YOUR_TOKEN&v=5.131"
```

### Проверка прав токена

```bash
curl "https://api.vk.com/method/account.getAppPermissions?access_token=YOUR_TOKEN&v=5.131"
```

### Проверка группы

```bash
curl "https://api.vk.com/method/groups.getById?group_id=123456789&access_token=YOUR_TOKEN&v=5.131"
```

### Тестовая загрузка фото

```bash
# 1. Получить upload URL
curl "https://api.vk.com/method/photos.getWallUploadServer?group_id=123456789&access_token=YOUR_TOKEN&v=5.131"

# 2. Загрузить фото
curl -F "photo=@/path/to/image.jpg" "UPLOAD_URL_FROM_STEP_1"

# 3. Сохранить фото
curl "https://api.vk.com/method/photos.saveWallPhoto?group_id=123456789&photo=...&server=...&hash=...&access_token=YOUR_TOKEN&v=5.131"
```

---

## Контрольный список диагностики

Перед обращением за помощью проверьте:

- [ ] Токен доступа валиден
- [ ] Все необходимые права предоставлены
- [ ] Group ID указан правильно
- [ ] Вы администратор группы
- [ ] Изображения доступны по URL
- [ ] Размер изображений не превышает 50 МБ
- [ ] Формат изображений поддерживается (JPG, PNG, GIF)
- [ ] Все узлы правильно соединены
- [ ] Credentials настроены корректно
- [ ] Нет ошибок в логах n8n
- [ ] VK API доступен (нет блокировок)

---

## Получение помощи

Если проблема не решена:

1. **Проверьте документацию:**
   - [VK API Docs](https://dev.vk.com/ru/reference)
   - [n8n Docs](https://docs.n8n.io/)

2. **Поищите в сообществе:**
   - [n8n Community Forum](https://community.n8n.io/)
   - [VK API Club](https://vk.com/apiclub)
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/vk-api)

3. **Создайте issue:**
   - Опишите проблему подробно
   - Приложите скриншоты
   - Укажите версии n8n и VK API
   - Приложите логи (без токенов!)

---

## Заключение

Большинство проблем можно решить, следуя этому руководству. Если вы столкнулись с новой проблемой, документируйте решение для других пользователей.

**Удачи в устранении неполадок! 🔧**
