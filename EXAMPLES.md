# Примеры использования VK Content Workflow

Коллекция практических примеров для различных сценариев использования.

## 📋 Содержание

1. [Мотивационные посты](#1-мотивационные-посты)
2. [Публикация новостей из RSS](#2-публикация-новостей-из-rss)
3. [Публикация с изображениями](#3-публикация-с-изображениями)
4. [Генерация контента с помощью AI](#4-генерация-контента-с-помощью-ai)
5. [Публикация в несколько групп](#5-публикация-в-несколько-групп)
6. [Планирование постов на будущее](#6-планирование-постов-на-будущее)
7. [Публикация из Telegram канала](#7-публикация-из-telegram-канала)
8. [A/B тестирование контента](#8-ab-тестирование-контента)
9. [Автоматические хештеги](#9-автоматические-хештеги)
10. [Модерация контента](#10-модерация-контента)

---

## 1. Мотивационные посты

### Описание
Автоматическая публикация мотивационных цитат каждое утро в 9:00.

### Код для узла Generate Content

```javascript
// Мотивационные цитаты
const quotes = [
  {
    text: "Успех - это сумма маленьких усилий, повторяемых изо дня в день.",
    author: "Роберт Кольер"
  },
  {
    text: "Не бойтесь начинать с нуля. Каждый мастер когда-то был новичком.",
    author: "Робин Шарма"
  },
  {
    text: "Ваше будущее создается тем, что вы делаете сегодня, а не завтра.",
    author: "Роберт Кийосаки"
  },
  {
    text: "Единственный способ сделать великую работу - любить то, что вы делаете.",
    author: "Стив Джобс"
  },
  {
    text: "Не ждите. Время никогда не будет подходящим.",
    author: "Наполеон Хилл"
  }
];

// Выбираем случайную цитату
const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

// Форматируем сообщение
const message = `💪 Мотивация дня:\n\n"${randomQuote.text}"\n\n© ${randomQuote.author}\n\n#мотивация #цитаты #успех #саморазвитие`;

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: ""
  }
};
```

### Настройка расписания

В узле **Schedule Trigger**:
- Interval: Days
- Time: 09:00
- Timezone: Europe/Moscow

---

## 2. Публикация новостей из RSS

### Описание
Автоматическая публикация новостей из RSS ленты каждый час.

### Шаги

1. Добавьте узел **RSS Read**
2. Настройте URL ленты
3. Добавьте узел **Code** для форматирования

### Код для форматирования

```javascript
// Получаем данные из RSS
const title = $json.title || "Без заголовка";
const description = $json.description || "";
const link = $json.link || "";
const pubDate = $json.pubDate ? new Date($json.pubDate).toLocaleString('ru-RU') : "";

// Обрезаем описание если слишком длинное
let shortDescription = description;
if (description.length > 300) {
  shortDescription = description.substring(0, 297) + "...";
}

// Форматируем сообщение
const message = `📰 ${title}\n\n${shortDescription}\n\n🔗 Читать полностью: ${link}\n\n📅 ${pubDate}\n\n#новости #новостидня`;

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: ""
  }
};
```

---

## 3. Публикация с изображениями

### Описание
Публикация постов с прикрепленными изображениями.

### Вариант A: Использование уже загруженного изображения

```javascript
// ID изображения, которое уже загружено в VK
const photoId = "photo-123456_789012"; // Замените на ваше

const message = "🎨 Красивое изображение дня!\n\n#фото #красота #искусство";

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: photoId
  }
};
```

### Вариант B: Загрузка нового изображения

1. **Узел: Get Upload Server**

```javascript
// HTTP Request к VK API
// Method: POST
// URL: https://api.vk.com/method/photos.getWallUploadServer
// Query Parameters:
{
  access_token: "{{ $credentials.vkAccessToken }}",
  v: "5.131",
  group_id: "123456" // ID группы без минуса
}
```

2. **Узел: Upload Photo**

```javascript
// HTTP Request
// Method: POST
// URL: {{ $json.response.upload_url }}
// Body: multipart-form-data
// File: your_image.jpg
```

3. **Узел: Save Wall Photo**

```javascript
// HTTP Request к VK API
// Method: POST
// URL: https://api.vk.com/method/photos.saveWallPhoto
// Query Parameters:
{
  access_token: "{{ $credentials.vkAccessToken }}",
  v: "5.131",
  group_id: "123456",
  photo: "{{ $json.photo }}",
  server: "{{ $json.server }}",
  hash: "{{ $json.hash }}"
}
```

4. **Узел: Post with Photo**

```javascript
const photoId = $json.response[0].id;
const ownerId = $json.response[0].owner_id;
const attachment = `photo${ownerId}_${photoId}`;

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: "Ваш текст",
    attachments: attachment
  }
};
```

---

## 4. Генерация контента с помощью AI

### Описание
Использование OpenAI для генерации уникального контента.

### Настройка OpenAI узла

```javascript
// Model: gpt-4 или gpt-3.5-turbo
// Messages:

[
  {
    "role": "system",
    "content": "Ты - креативный копирайтер для социальных сетей. Создавай интересные, вовлекающие посты для VKontakte на русском языке."
  },
  {
    "role": "user",
    "content": "Создай мотивационный пост для VK на тему саморазвития. Длина: 200-400 символов. Добавь 3-4 релевантных хештега. Используй 2-3 эмодзи для привлечения внимания. Пост должен быть вдохновляющим и практичным."
  }
]
```

### Обработка ответа AI

```javascript
// Получаем текст от OpenAI
const aiResponse = $json.choices[0].message.content;

// Удаляем лишние кавычки если есть
let message = aiResponse.trim();
if (message.startsWith('"') && message.endsWith('"')) {
  message = message.slice(1, -1);
}

// Проверяем длину
if (message.length > 4096) {
  message = message.substring(0, 4093) + "...";
}

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: ""
  }
};
```

---

## 5. Публикация в несколько групп

### Описание
Публикация одного и того же контента в несколько групп одновременно.

### Вариант A: Последовательная публикация

```javascript
// Список групп для публикации
const groups = [
  "-123456",
  "-789012",
  "-345678"
];

const message = "Ваш контент здесь";

// Возвращаем массив для публикации в каждую группу
return groups.map(groupId => ({
  json: {
    owner_id: groupId,
    message: message,
    attachments: ""
  }
}));
```

### Вариант B: С разным контентом для каждой группы

```javascript
const groupsContent = [
  {
    owner_id: "-123456",
    message: "Контент для группы 1 #группа1"
  },
  {
    owner_id: "-789012",
    message: "Контент для группы 2 #группа2"
  },
  {
    owner_id: "-345678",
    message: "Контент для группы 3 #группа3"
  }
];

return groupsContent.map(content => ({
  json: {
    owner_id: content.owner_id,
    message: content.message,
    attachments: ""
  }
}));
```

---

## 6. Планирование постов на будущее

### Описание
Публикация постов с отложенной датой.

### Код

```javascript
// Текущее время + 2 часа
const publishDate = Math.floor(Date.now() / 1000) + (2 * 60 * 60);

// Или конкретная дата
// const publishDate = Math.floor(new Date('2026-02-08 15:00:00').getTime() / 1000);

const message = "Этот пост будет опубликован через 2 часа!";

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: "",
    publish_date: publishDate
  }
};
```

### Настройка VK Post узла

Добавьте параметр `publish_date` в Query Parameters:

```
name: publish_date
value: ={{ $json.publish_date }}
```

---

## 7. Публикация из Telegram канала

### Описание
Автоматическая публикация сообщений из Telegram канала в VK.

### Шаги

1. **Добавьте Telegram Trigger**
   - Updates: Message
   - Chat ID: ваш канал

2. **Добавьте узел обработки**

```javascript
// Получаем сообщение из Telegram
const telegramMessage = $json.message.text || "";
const telegramPhoto = $json.message.photo;

// Форматируем для VK
let vkMessage = telegramMessage;

// Добавляем ссылку на Telegram канал
vkMessage += "\n\n📱 Больше контента в нашем Telegram: t.me/your_channel";

// Обрабатываем фото (если есть)
let attachments = "";
if (telegramPhoto && telegramPhoto.length > 0) {
  // Здесь нужно загрузить фото в VK
  // См. пример 3
}

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: vkMessage,
    attachments: attachments
  }
};
```

---

## 8. A/B тестирование контента

### Описание
Публикация разных вариантов контента для тестирования эффективности.

### Код

```javascript
// Варианты контента
const variants = [
  {
    id: "A",
    message: "🚀 Вариант A: Начните свой путь к успеху сегодня! #мотивация #успех",
    emoji_style: "modern"
  },
  {
    id: "B",
    message: "💪 Вариант B: Каждый день - шаг к вашей цели! #цели #достижения",
    emoji_style: "classic"
  }
];

// Выбираем вариант (можно по времени, случайно, или по очереди)
const hour = new Date().getHours();
const variant = variants[hour % 2]; // Чередуем по часам

// Добавляем метку для отслеживания
const message = variant.message + `\n\n[Test: ${variant.id}]`;

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: "",
    test_variant: variant.id,
    test_timestamp: new Date().toISOString()
  }
};
```

### Анализ результатов

Через несколько часов соберите статистику:

```javascript
// Узел для сбора статистики
const postId = $json.post_id;
const testVariant = $json.test_variant;

// Получаем статистику через VK API (wall.getById)
// Сохраняем в БД вместе с test_variant
// Анализируем какой вариант эффективнее
```

---

## 9. Автоматические хештеги

### Описание
Автоматическое добавление релевантных хештегов на основе контента.

### Код

```javascript
const message = "Сегодня отличный день для саморазвития и обучения!";

// Словарь ключевых слов и хештегов
const hashtagMap = {
  "саморазвитие": ["#саморазвитие", "#развитие", "#личностныйрост"],
  "обучение": ["#обучение", "#образование", "#знания"],
  "мотивация": ["#мотивация", "#мотивациякаждыйдень", "#успех"],
  "здоровье": ["#зож", "#здоровье", "#спорт"],
  "бизнес": ["#бизнес", "#предпринимательство", "#стартап"]
};

// Находим релевантные хештеги
let hashtags = new Set();
const lowerMessage = message.toLowerCase();

for (const [keyword, tags] of Object.entries(hashtagMap)) {
  if (lowerMessage.includes(keyword)) {
    tags.forEach(tag => hashtags.add(tag));
  }
}

// Ограничиваем количество хештегов (максимум 5)
const selectedHashtags = Array.from(hashtags).slice(0, 5).join(" ");

// Добавляем хештеги к сообщению
const finalMessage = `${message}\n\n${selectedHashtags}`;

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: finalMessage,
    attachments: ""
  }
};
```

---

## 10. Модерация контента

### Описание
Отправка контента на модерацию перед публикацией через Telegram бота.

### Шаги

1. **Генерация контента**

```javascript
const message = "Ваш сгенерированный контент";

return {
  json: {
    owner_id: "-YOUR_GROUP_ID",
    message: message,
    attachments: "",
    moderation_id: Date.now().toString()
  }
};
```

2. **Отправка в Telegram для модерации**

```javascript
// Telegram узел
// Message:
const moderationId = $json.moderation_id;
const message = $json.message;

const telegramMessage = `🔍 Новый пост на модерацию:\n\n${message}\n\n✅ Одобрить: /approve_${moderationId}\n❌ Отклонить: /reject_${moderationId}`;

// Отправляем модератору
```

3. **Telegram Trigger для команд**

```javascript
// Обрабатываем команды /approve_* и /reject_*
const command = $json.message.text;

if (command.startsWith('/approve_')) {
  const moderationId = command.replace('/approve_', '');
  
  // Публикуем пост
  return {
    json: {
      action: "publish",
      moderation_id: moderationId
    }
  };
} else if (command.startsWith('/reject_')) {
  const moderationId = command.replace('/reject_', '');
  
  // Отклоняем пост
  return {
    json: {
      action: "reject",
      moderation_id: moderationId
    }
  };
}
```

4. **Условная публикация**

```javascript
// IF узел проверяет action === "publish"
// Если да - публикуем в VK
// Если нет - логируем отклонение
```

---

## 🎯 Комбинированные сценарии

### Сценарий 1: AI + Изображения + Модерация

1. AI генерирует текст
2. DALL-E генерирует изображение
3. Отправляется на модерацию в Telegram
4. После одобрения публикуется в VK

### Сценарий 2: RSS + AI улучшение + Публикация

1. Получаем новости из RSS
2. AI переписывает в более интересном стиле
3. Добавляем автоматические хештеги
4. Публикуем в VK

### Сценарий 3: Telegram → VK → Статистика

1. Получаем контент из Telegram
2. Публикуем в VK
3. Через час собираем статистику
4. Отправляем отчет в Telegram

---

## 📊 Шаблоны для разных ниш

### Фитнес и ЗОЖ

```javascript
const fitnessContent = [
  "🏃‍♂️ Совет дня: 10 минут зарядки утром = заряд энергии на весь день! #зож #фитнес #здоровье",
  "🥗 Правильное питание - это не диета, а образ жизни! #пп #здоровоепитание #зож",
  "💪 Тренировка сегодня = здоровье завтра! Не откладывай! #тренировки #спорт #мотивация"
];
```

### Бизнес и предпринимательство

```javascript
const businessContent = [
  "💼 Совет предпринимателю: Начните с малого, но начните сегодня! #бизнес #предпринимательство #стартап",
  "📈 Инвестируйте в себя - это лучшая инвестиция! #бизнес #развитие #инвестиции",
  "🎯 Ваша цель - ваш компас в мире бизнеса! #бизнес #цели #успех"
];
```

### Образование

```javascript
const educationContent = [
  "📚 Учитесь каждый день - знания никогда не бывают лишними! #образование #обучение #знания",
  "🎓 Инвестиция в знания приносит наибольший доход! #образование #саморазвитие #учеба",
  "💡 Любопытство - двигатель прогресса! #образование #развитие #знания"
];
```

---

## 🔧 Полезные функции

### Функция обрезки текста

```javascript
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + "...";
}

const longText = "Очень длинный текст...";
const shortText = truncateText(longText, 200);
```

### Функция форматирования даты

```javascript
function formatDate(date) {
  return new Date(date).toLocaleString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

const formattedDate = formatDate(new Date());
```

### Функция случайного выбора

```javascript
function randomChoice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

const items = ["item1", "item2", "item3"];
const selected = randomChoice(items);
```

---

**Больше примеров и идей в [VK_WORKFLOW_README.md](./VK_WORKFLOW_README.md)**
