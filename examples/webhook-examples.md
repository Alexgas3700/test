# Примеры использования Webhook для VK Content Workflow

## Базовые примеры

### 1. Простой текстовый пост

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Привет, VK! Это автоматический пост из n8n.",
    "from_group": 1
  }'
```

**Ответ:**
```json
{
  "post_id": "123456789_987654321",
  "date": 1707264000,
  "text": "Привет, VK! Это автоматический пост из n8n."
}
```

### 2. Пост с изображением

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Посмотрите на это фото!",
    "attachments": ["photo-123456789_456239017"],
    "from_group": 1
  }'
```

### 3. Пост с несколькими вложениями

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Новая коллекция фотографий",
    "attachments": [
      "photo-123456789_456239017",
      "photo-123456789_456239018",
      "photo-123456789_456239019"
    ],
    "from_group": 1
  }'
```

## Расширенные примеры

### 4. Отложенная публикация

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Этот пост будет опубликован завтра в 12:00",
    "publish_date": "2026-02-08T12:00:00Z",
    "from_group": 1
  }'
```

### 5. Пост с хэштегами

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Новая статья о технологиях",
    "hashtags": ["технологии", "инновации", "будущее"],
    "from_group": 1
  }'
```

### 6. Пост с геолокацией

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Мы открылись по новому адресу!",
    "lat": 55.751244,
    "long": 37.618423,
    "place_id": 12345,
    "from_group": 1
  }'
```

### 7. Рекламный пост

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Специальное предложение только сегодня! Скидка 50%",
    "attachments": ["photo-123456789_456239017"],
    "mark_as_ads": 1,
    "from_group": 1
  }'
```

### 8. Пост с закрытыми комментариями

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Важное объявление (комментарии отключены)",
    "close_comments": 1,
    "from_group": 1
  }'
```

### 9. Пост без уведомлений

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Тихая публикация без уведомлений подписчиков",
    "mute_notifications": 1,
    "from_group": 1
  }'
```

### 10. Пост с указанием авторства

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Интересная статья",
    "attachments": ["https://example.com/article"],
    "copyright": "https://example.com",
    "from_group": 1
  }'
```

## Примеры с Python

### Простой пост

```python
import requests
import json

url = "https://your-n8n-instance.com/webhook/create-vk-post"
headers = {"Content-Type": "application/json"}

data = {
    "owner_id": "-123456789",
    "message": "Привет из Python!",
    "from_group": 1
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

### Массовая публикация

```python
import requests
import json
from datetime import datetime, timedelta

url = "https://your-n8n-instance.com/webhook/create-vk-post"
headers = {"Content-Type": "application/json"}

posts = [
    {"message": "Пост 1: Утренняя мотивация", "hashtags": ["утро", "мотивация"]},
    {"message": "Пост 2: Обеденный совет", "hashtags": ["обед", "советы"]},
    {"message": "Пост 3: Вечерняя мудрость", "hashtags": ["вечер", "мудрость"]}
]

for i, post in enumerate(posts):
    # Планируем посты с интервалом 4 часа
    publish_date = datetime.now() + timedelta(hours=4*i)
    
    data = {
        "owner_id": "-123456789",
        "message": post["message"],
        "hashtags": post["hashtags"],
        "publish_date": publish_date.isoformat(),
        "from_group": 1
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Пост {i+1}: {response.json()}")
```

### Пост с загрузкой изображения

```python
import requests
import json

# Сначала загружаем фото в VK
def upload_photo_to_vk(image_path, access_token, group_id):
    # Получаем URL для загрузки
    upload_url_response = requests.get(
        "https://api.vk.com/method/photos.getWallUploadServer",
        params={
            "access_token": access_token,
            "v": "5.131",
            "group_id": group_id
        }
    )
    upload_url = upload_url_response.json()["response"]["upload_url"]
    
    # Загружаем фото
    with open(image_path, "rb") as photo:
        files = {"photo": photo}
        upload_response = requests.post(upload_url, files=files)
    
    upload_data = upload_response.json()
    
    # Сохраняем фото
    save_response = requests.get(
        "https://api.vk.com/method/photos.saveWallPhoto",
        params={
            "access_token": access_token,
            "v": "5.131",
            "group_id": group_id,
            "photo": upload_data["photo"],
            "server": upload_data["server"],
            "hash": upload_data["hash"]
        }
    )
    
    photo_data = save_response.json()["response"][0]
    return f"photo{photo_data['owner_id']}_{photo_data['id']}"

# Публикуем пост с фото
access_token = "your_vk_access_token"
group_id = "123456789"
photo_attachment = upload_photo_to_vk("image.jpg", access_token, group_id)

url = "https://your-n8n-instance.com/webhook/create-vk-post"
headers = {"Content-Type": "application/json"}

data = {
    "owner_id": f"-{group_id}",
    "message": "Пост с загруженным фото",
    "attachments": [photo_attachment],
    "from_group": 1
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

## Примеры с Node.js

### Простой пост

```javascript
const axios = require('axios');

const url = 'https://your-n8n-instance.com/webhook/create-vk-post';

const data = {
  owner_id: '-123456789',
  message: 'Привет из Node.js!',
  from_group: 1
};

axios.post(url, data)
  .then(response => {
    console.log('Пост опубликован:', response.data);
  })
  .catch(error => {
    console.error('Ошибка:', error.response.data);
  });
```

### Планирование постов

```javascript
const axios = require('axios');

const url = 'https://your-n8n-instance.com/webhook/create-vk-post';

const posts = [
  { message: 'Доброе утро!', time: 9 },
  { message: 'Приятного обеда!', time: 13 },
  { message: 'Хорошего вечера!', time: 18 }
];

posts.forEach(post => {
  const publishDate = new Date();
  publishDate.setHours(post.time, 0, 0, 0);
  
  const data = {
    owner_id: '-123456789',
    message: post.message,
    publish_date: publishDate.toISOString(),
    from_group: 1
  };
  
  axios.post(url, data)
    .then(response => {
      console.log(`Запланирован пост на ${post.time}:00:`, response.data);
    })
    .catch(error => {
      console.error('Ошибка:', error.response?.data || error.message);
    });
});
```

### Async/Await версия

```javascript
const axios = require('axios');

async function createVKPost(postData) {
  const url = 'https://your-n8n-instance.com/webhook/create-vk-post';
  
  try {
    const response = await axios.post(url, postData);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data || error.message 
    };
  }
}

async function publishMultiplePosts() {
  const posts = [
    {
      owner_id: '-123456789',
      message: 'Первый пост',
      hashtags: ['первый', 'тест'],
      from_group: 1
    },
    {
      owner_id: '-123456789',
      message: 'Второй пост',
      hashtags: ['второй', 'тест'],
      from_group: 1
    }
  ];
  
  for (const post of posts) {
    const result = await createVKPost(post);
    if (result.success) {
      console.log('Успешно:', result.data);
    } else {
      console.error('Ошибка:', result.error);
    }
    
    // Задержка между постами
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

publishMultiplePosts();
```

## Примеры с PHP

### Простой пост

```php
<?php

$url = 'https://your-n8n-instance.com/webhook/create-vk-post';

$data = [
    'owner_id' => '-123456789',
    'message' => 'Привет из PHP!',
    'from_group' => 1
];

$options = [
    'http' => [
        'header'  => "Content-Type: application/json\r\n",
        'method'  => 'POST',
        'content' => json_encode($data)
    ]
];

$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);

if ($result === FALSE) {
    die('Ошибка при публикации поста');
}

$response = json_decode($result, true);
echo "Пост опубликован: " . print_r($response, true);

?>
```

### Массовая публикация из базы данных

```php
<?php

// Подключение к БД
$pdo = new PDO('mysql:host=localhost;dbname=mydb', 'user', 'password');

// Получаем посты для публикации
$stmt = $pdo->query("SELECT * FROM scheduled_posts WHERE published = 0 LIMIT 10");
$posts = $stmt->fetchAll(PDO::FETCH_ASSOC);

$url = 'https://your-n8n-instance.com/webhook/create-vk-post';

foreach ($posts as $post) {
    $data = [
        'owner_id' => $post['owner_id'],
        'message' => $post['message'],
        'hashtags' => json_decode($post['hashtags']),
        'from_group' => 1
    ];
    
    $options = [
        'http' => [
            'header'  => "Content-Type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data)
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    if ($result !== FALSE) {
        // Помечаем как опубликованный
        $updateStmt = $pdo->prepare("UPDATE scheduled_posts SET published = 1 WHERE id = ?");
        $updateStmt->execute([$post['id']]);
        
        echo "Пост {$post['id']} опубликован\n";
    } else {
        echo "Ошибка при публикации поста {$post['id']}\n";
    }
    
    sleep(2); // Задержка между постами
}

?>
```

## Примеры с авторизацией

### Bearer Token

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-token" \
  -d '{
    "owner_id": "-123456789",
    "message": "Защищенный пост",
    "from_group": 1
  }'
```

### API Key

```bash
curl -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "owner_id": "-123456789",
    "message": "Пост с API ключом",
    "from_group": 1
  }'
```

## Обработка ошибок

### Пример с обработкой ошибок (Python)

```python
import requests
import json

def create_vk_post(data):
    url = "https://your-n8n-instance.com/webhook/create-vk-post"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP Error: {e.response.status_code}", "details": e.response.text}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error: Unable to connect to server"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout Error: Request took too long"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request Error: {str(e)}"}

# Использование
post_data = {
    "owner_id": "-123456789",
    "message": "Тестовый пост",
    "from_group": 1
}

result = create_vk_post(post_data)

if result["success"]:
    print(f"Успех! Post ID: {result['data']['post_id']}")
else:
    print(f"Ошибка: {result['error']}")
    if "details" in result:
        print(f"Детали: {result['details']}")
```

## Интеграция с другими сервисами

### Webhook от Telegram бота

```python
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import json

def post_to_vk(update: Update, context: CallbackContext):
    message_text = ' '.join(context.args)
    
    if not message_text:
        update.message.reply_text("Использование: /post <текст поста>")
        return
    
    url = "https://your-n8n-instance.com/webhook/create-vk-post"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "owner_id": "-123456789",
        "message": message_text,
        "from_group": 1
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        update.message.reply_text(f"✅ Пост опубликован! ID: {result['post_id']}")
    else:
        update.message.reply_text(f"❌ Ошибка при публикации: {response.text}")

# Настройка бота
updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("post", post_to_vk))
updater.start_polling()
```

### Webhook от Google Forms

```javascript
// Google Apps Script
function onFormSubmit(e) {
  var formResponse = e.response;
  var itemResponses = formResponse.getItemResponses();
  
  var message = '';
  for (var i = 0; i < itemResponses.length; i++) {
    var itemResponse = itemResponses[i];
    message += itemResponse.getItem().getTitle() + ': ' + itemResponse.getResponse() + '\n';
  }
  
  var url = 'https://your-n8n-instance.com/webhook/create-vk-post';
  var data = {
    'owner_id': '-123456789',
    'message': 'Новая заявка:\n\n' + message,
    'from_group': 1
  };
  
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(data)
  };
  
  UrlFetchApp.fetch(url, options);
}
```

## Тестирование

### Тест с Postman

1. Создайте новый POST запрос
2. URL: `https://your-n8n-instance.com/webhook/create-vk-post`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "owner_id": "-123456789",
  "message": "Тестовый пост из Postman",
  "from_group": 1
}
```

### Тест с curl (verbose)

```bash
curl -v -X POST https://your-n8n-instance.com/webhook/create-vk-post \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Тестовый пост",
    "from_group": 1
  }'
```

---

**Примечание**: Замените `https://your-n8n-instance.com` на реальный URL вашего n8n instance и `-123456789` на ID вашей группы VK.
