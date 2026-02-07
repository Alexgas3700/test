# Примеры интеграций VK Content Workflow

## 1. Интеграция с Google Sheets

### Автоматическая публикация из таблицы

Создайте workflow, который читает данные из Google Sheets и публикует их в VK.

**Структура таблицы:**

| Дата публикации | Текст поста | Хэштеги | Вложения | Статус |
|----------------|-------------|---------|----------|--------|
| 2026-02-08 12:00 | Текст 1 | технологии,новости | photo123_456 | pending |
| 2026-02-08 15:00 | Текст 2 | обзор,продукт | photo123_457 | pending |

**n8n Workflow:**

```json
{
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 1}]
        }
      }
    },
    {
      "name": "Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "read",
        "sheetId": "your-sheet-id",
        "range": "A2:E100",
        "options": {
          "valueRenderOption": "UNFORMATTED_VALUE"
        }
      }
    },
    {
      "name": "Filter Pending",
      "type": "n8n-nodes-base.filter",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.status }}",
              "operation": "equals",
              "value2": "pending"
            }
          ],
          "dateTime": [
            {
              "value1": "={{ $json.publish_date }}",
              "operation": "before",
              "value2": "={{ $now }}"
            }
          ]
        }
      }
    },
    {
      "name": "Create VK Post",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  hashtags: $json.hashtags.split(','),\n  attachments: [$json.attachments],\n  from_group: 1\n}) }}"
      }
    },
    {
      "name": "Update Status",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "update",
        "sheetId": "your-sheet-id",
        "range": "E{{ $json.row }}",
        "options": {
          "valueInputOption": "USER_ENTERED"
        },
        "dataToUpdate": "published"
      }
    }
  ]
}
```

## 2. Интеграция с RSS лентой

### Автоматическая публикация новостей

```json
{
  "nodes": [
    {
      "name": "RSS Feed Trigger",
      "type": "n8n-nodes-base.rssFeedRead",
      "parameters": {
        "url": "https://example.com/rss",
        "pollTimes": {
          "item": [
            {
              "mode": "everyMinute",
              "value": 30
            }
          ]
        }
      }
    },
    {
      "name": "Extract Data",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const items = $input.all();\nconst results = [];\n\nfor (const item of items) {\n  const data = item.json;\n  \n  // Формируем сообщение\n  let message = `📰 ${data.title}\\n\\n`;\n  message += `${data.contentSnippet || data.description}\\n\\n`;\n  message += `Читать полностью: ${data.link}`;\n  \n  // Извлекаем изображение если есть\n  let attachments = [];\n  if (data.enclosure && data.enclosure.url) {\n    attachments.push(data.enclosure.url);\n  }\n  \n  results.push({\n    json: {\n      message: message,\n      attachments: attachments,\n      link: data.link,\n      title: data.title\n    }\n  });\n}\n\nreturn results;"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  attachments: $json.attachments,\n  from_group: 1,\n  copyright: $json.link\n}) }}"
      }
    }
  ]
}
```

## 3. Интеграция с OpenAI для генерации контента

### AI-генерация постов

```json
{
  "nodes": [
    {
      "name": "Schedule Daily",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 24}]
        }
      }
    },
    {
      "name": "Get Topics",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const topics = [\n  'Технологии будущего',\n  'Искусственный интеллект',\n  'Экология и устойчивое развитие',\n  'Космические исследования',\n  'Здоровый образ жизни'\n];\n\nconst randomTopic = topics[Math.floor(Math.random() * topics.length)];\n\nreturn [{\n  json: {\n    topic: randomTopic\n  }\n}];"
      }
    },
    {
      "name": "Generate Content",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "resource": "text",
        "operation": "message",
        "model": "gpt-4",
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "Ты - креативный копирайтер для социальных сетей. Создавай интересные, вовлекающие посты на русском языке длиной 200-300 символов."
            },
            {
              "role": "user",
              "content": "Создай интересный пост на тему: {{ $json.topic }}"
            }
          ]
        },
        "options": {
          "temperature": 0.8,
          "maxTokens": 300
        }
      }
    },
    {
      "name": "Generate Hashtags",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "resource": "text",
        "operation": "message",
        "model": "gpt-4",
        "messages": {
          "values": [
            {
              "role": "user",
              "content": "Создай 3-5 релевантных хэштегов для этого поста (только слова без #): {{ $json.choices[0].message.content }}"
            }
          ]
        }
      }
    },
    {
      "name": "Format Post",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const message = $input.first().json.choices[0].message.content;\nconst hashtagsText = $input.last().json.choices[0].message.content;\nconst hashtags = hashtagsText.split(/[,\\s]+/).filter(tag => tag.length > 0);\n\nreturn [{\n  json: {\n    message: message,\n    hashtags: hashtags\n  }\n}];"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  hashtags: $json.hashtags,\n  from_group: 1\n}) }}"
      }
    }
  ]
}
```

## 4. Интеграция с Telegram

### Публикация из Telegram канала в VK

```json
{
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "parameters": {
        "updates": ["channel_post"]
      }
    },
    {
      "name": "Check Admin",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ $json.message.from.id }}",
              "operation": "equals",
              "value2": "YOUR_ADMIN_ID"
            }
          ]
        }
      }
    },
    {
      "name": "Process Message",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const message = $json.message;\nlet text = message.text || message.caption || '';\nlet attachments = [];\n\n// Обработка фото\nif (message.photo && message.photo.length > 0) {\n  const photo = message.photo[message.photo.length - 1];\n  attachments.push({\n    type: 'photo',\n    file_id: photo.file_id\n  });\n}\n\n// Обработка видео\nif (message.video) {\n  attachments.push({\n    type: 'video',\n    file_id: message.video.file_id\n  });\n}\n\nreturn [{\n  json: {\n    message: text,\n    telegram_attachments: attachments\n  }\n}];"
      }
    },
    {
      "name": "Download Media",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "resource": "file",
        "operation": "get",
        "fileId": "={{ $json.telegram_attachments[0].file_id }}"
      }
    },
    {
      "name": "Upload to VK",
      "type": "n8n-nodes-base.vk",
      "parameters": {
        "resource": "photo",
        "operation": "upload",
        "albumId": "wall"
      }
    },
    {
      "name": "Create VK Post",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  attachments: [$json.vk_photo_id],\n  from_group: 1\n}) }}"
      }
    }
  ]
}
```

## 5. Интеграция с Airtable

### Контент-календарь в Airtable

```json
{
  "nodes": [
    {
      "name": "Schedule Check",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 15}]
        }
      }
    },
    {
      "name": "Get Scheduled Posts",
      "type": "n8n-nodes-base.airtable",
      "parameters": {
        "operation": "list",
        "application": "YOUR_BASE_ID",
        "table": "Content Calendar",
        "filterByFormula": "AND(Status = 'Scheduled', IS_BEFORE({Publish Date}, NOW()))"
      }
    },
    {
      "name": "Process Each Post",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": {
        "batchSize": 1
      }
    },
    {
      "name": "Prepare Post Data",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const record = $json.fields;\n\nreturn [{\n  json: {\n    record_id: $json.id,\n    owner_id: record['VK Group ID'],\n    message: record['Post Text'],\n    hashtags: record['Hashtags'] ? record['Hashtags'].split(',') : [],\n    attachments: record['Attachments'] ? record['Attachments'].split(',') : [],\n    from_group: 1\n  }\n}];"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: $json.owner_id,\n  message: $json.message,\n  hashtags: $json.hashtags,\n  attachments: $json.attachments,\n  from_group: $json.from_group\n}) }}"
      }
    },
    {
      "name": "Update Airtable Status",
      "type": "n8n-nodes-base.airtable",
      "parameters": {
        "operation": "update",
        "application": "YOUR_BASE_ID",
        "table": "Content Calendar",
        "id": "={{ $json.record_id }}",
        "fields": {
          "Status": "Published",
          "VK Post ID": "={{ $json.post_id }}",
          "Published At": "={{ $now }}"
        }
      }
    }
  ]
}
```

## 6. Интеграция с WordPress

### Автопубликация статей из WordPress

```json
{
  "nodes": [
    {
      "name": "WordPress Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "wordpress-to-vk"
      }
    },
    {
      "name": "Extract Post Data",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const post = $json;\n\n// Формируем анонс\nlet message = `📝 Новая статья: ${post.title}\\n\\n`;\nmessage += `${post.excerpt.substring(0, 200)}...\\n\\n`;\nmessage += `Читать полностью: ${post.link}`;\n\n// Извлекаем featured image\nlet attachments = [];\nif (post.featured_image_url) {\n  attachments.push(post.featured_image_url);\n}\n\n// Извлекаем категории как хэштеги\nlet hashtags = [];\nif (post.categories) {\n  hashtags = post.categories.map(cat => cat.name.toLowerCase().replace(/\\s+/g, ''));\n}\n\nreturn [{\n  json: {\n    message: message,\n    image_url: post.featured_image_url,\n    hashtags: hashtags,\n    link: post.link\n  }\n}];"
      }
    },
    {
      "name": "Download Featured Image",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "={{ $json.image_url }}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      }
    },
    {
      "name": "Upload to VK",
      "type": "n8n-nodes-base.vk",
      "parameters": {
        "resource": "photo",
        "operation": "upload",
        "albumId": "wall",
        "binaryProperty": "data"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  attachments: [$json.vk_photo_id],\n  hashtags: $json.hashtags,\n  from_group: 1,\n  copyright: $json.link\n}) }}"
      }
    }
  ]
}
```

## 7. Интеграция с Instagram (через API)

### Кросспостинг из Instagram в VK

```json
{
  "nodes": [
    {
      "name": "Schedule Check",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 2}]
        }
      }
    },
    {
      "name": "Get Instagram Posts",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "https://graph.instagram.com/me/media",
        "qs": {
          "fields": "id,caption,media_type,media_url,permalink,timestamp",
          "access_token": "YOUR_INSTAGRAM_ACCESS_TOKEN"
        }
      }
    },
    {
      "name": "Filter New Posts",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const posts = $json.data;\nconst results = [];\nconst lastCheckTime = $workflow.staticData.lastCheckTime || 0;\nconst currentTime = Date.now();\n\nfor (const post of posts) {\n  const postTime = new Date(post.timestamp).getTime();\n  \n  if (postTime > lastCheckTime) {\n    results.push({\n      json: post\n    });\n  }\n}\n\n$workflow.staticData.lastCheckTime = currentTime;\n\nreturn results;"
      }
    },
    {
      "name": "Process Instagram Post",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const post = $json;\n\n// Извлекаем хэштеги из caption\nconst caption = post.caption || '';\nconst hashtagRegex = /#(\\w+)/g;\nconst hashtags = [];\nlet match;\nwhile ((match = hashtagRegex.exec(caption)) !== null) {\n  hashtags.push(match[1]);\n}\n\n// Убираем хэштеги из текста\nconst cleanCaption = caption.replace(hashtagRegex, '').trim();\n\n// Добавляем ссылку на оригинал\nconst message = `${cleanCaption}\\n\\n📸 Instagram: ${post.permalink}`;\n\nreturn [{\n  json: {\n    message: message,\n    media_url: post.media_url,\n    media_type: post.media_type,\n    hashtags: hashtags\n  }\n}];"
      }
    },
    {
      "name": "Download Media",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",\n        "url": "={{ $json.media_url }}",
        "options": {
          "response": {
            "response": {
              "responseFormat": "file"
            }
          }
        }
      }
    },
    {
      "name": "Upload to VK",
      "type": "n8n-nodes-base.vk",
      "parameters": {
        "resource": "photo",
        "operation": "upload",
        "albumId": "wall",
        "binaryProperty": "data"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  attachments: [$json.vk_photo_id],\n  hashtags: $json.hashtags,\n  from_group: 1\n}) }}"
      }
    }
  ]
}
```

## 8. Интеграция с Notion

### Контент-менеджмент через Notion

```json
{
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 30}]
        }
      }
    },
    {
      "name": "Query Notion Database",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "resource": "databasePage",
        "operation": "getAll",
        "databaseId": "YOUR_DATABASE_ID",
        "filters": {
          "conditions": [
            {
              "key": "Status",
              "condition": "equals",
              "value": "Ready to Publish"
            },
            {
              "key": "Publish Date",
              "condition": "on_or_before",
              "value": "{{ $now }}"
            }
          ]
        }
      }
    },
    {
      "name": "Extract Page Content",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "resource": "block",
        "operation": "getAll",
        "blockId": "={{ $json.id }}"
      }
    },
    {
      "name": "Format Content",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const page = $input.first().json;\nconst blocks = $input.last().json;\n\n// Извлекаем свойства страницы\nconst title = page.properties.Title.title[0].plain_text;\nconst hashtags = page.properties.Hashtags.multi_select.map(tag => tag.name);\nconst attachments = page.properties.Attachments.rich_text[0]?.plain_text.split(',') || [];\n\n// Собираем текст из блоков\nlet content = '';\nfor (const block of blocks) {\n  if (block.type === 'paragraph' && block.paragraph.rich_text.length > 0) {\n    content += block.paragraph.rich_text[0].plain_text + '\\n';\n  }\n}\n\nconst message = `${title}\\n\\n${content}`;\n\nreturn [{\n  json: {\n    page_id: page.id,\n    message: message,\n    hashtags: hashtags,\n    attachments: attachments\n  }\n}];"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  hashtags: $json.hashtags,\n  attachments: $json.attachments,\n  from_group: 1\n}) }}"
      }
    },
    {
      "name": "Update Notion Status",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "resource": "databasePage",
        "operation": "update",
        "pageId": "={{ $json.page_id }}",
        "properties": {
          "Status": {
            "type": "select",
            "select": {
              "name": "Published"
            }
          },
          "VK Post ID": {
            "type": "rich_text",
            "rich_text": [
              {
                "text": {
                  "content": "={{ $json.post_id }}"
                }
              }
            ]
          }
        }
      }
    }
  ]
}
```

## 9. Интеграция с Email (IMAP)

### Публикация из email

```json
{
  "nodes": [
    {
      "name": "Email Trigger",
      "type": "n8n-nodes-base.emailReadImap",
      "parameters": {
        "mailbox": "INBOX",
        "postProcessAction": "mark",
        "options": {
          "customEmailConfig": "imap.gmail.com:993:true"
        }
      }
    },
    {
      "name": "Check Subject",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.subject }}",
              "operation": "contains",
              "value2": "[VK POST]"
            }
          ]
        }
      }
    },
    {
      "name": "Parse Email",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const email = $json;\nconst body = email.textPlain || email.html;\n\n// Извлекаем хэштеги из темы\nconst subject = email.subject.replace('[VK POST]', '').trim();\nconst hashtagRegex = /#(\\w+)/g;\nconst hashtags = [];\nlet match;\nwhile ((match = hashtagRegex.exec(subject)) !== null) {\n  hashtags.push(match[1]);\n}\n\n// Обрабатываем вложения\nconst attachments = [];\nif (email.attachments) {\n  for (const attachment of email.attachments) {\n    if (attachment.contentType.startsWith('image/')) {\n      attachments.push(attachment);\n    }\n  }\n}\n\nreturn [{\n  json: {\n    message: body,\n    hashtags: hashtags,\n    email_attachments: attachments\n  }\n}];"
      }
    },
    {
      "name": "Upload Images",
      "type": "n8n-nodes-base.vk",
      "parameters": {
        "resource": "photo",
        "operation": "upload",
        "albumId": "wall"
      }
    },
    {
      "name": "Post to VK",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://your-n8n-instance.com/webhook/create-vk-post",
        "jsonParameters": true,
        "bodyParametersJson": "={{ JSON.stringify({\n  owner_id: '-123456789',\n  message: $json.message,\n  hashtags: $json.hashtags,\n  attachments: $json.vk_photo_ids,\n  from_group: 1\n}) }}"
      }
    }
  ]
}
```

## 10. Интеграция с Zapier/Make (Webhook)

### Универсальный webhook endpoint

```javascript
// Пример отправки из Zapier
const options = {
  method: 'POST',
  url: 'https://your-n8n-instance.com/webhook/create-vk-post',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    owner_id: '-123456789',
    message: inputData.message,
    hashtags: inputData.hashtags.split(','),
    from_group: 1
  })
};

fetch(options.url, options)
  .then(response => response.json())
  .then(data => {
    output = {
      success: true,
      post_id: data.post_id,
      url: `https://vk.com/wall${data.owner_id}_${data.post_id}`
    };
  });
```

---

## Общие рекомендации

1. **Обработка ошибок**: Всегда добавляйте узлы для обработки ошибок
2. **Логирование**: Сохраняйте информацию о публикациях в базу данных
3. **Лимиты API**: Учитывайте ограничения VK API (не более 3 запросов в секунду)
4. **Тестирование**: Тестируйте workflow на тестовой группе перед продакшеном
5. **Мониторинг**: Настройте уведомления об ошибках
6. **Безопасность**: Используйте environment variables для токенов и ключей

## Полезные ссылки

- [VK API Documentation](https://dev.vk.com/reference)
- [n8n Integration Nodes](https://docs.n8n.io/integrations/)
- [n8n Community Workflows](https://n8n.io/workflows/)
