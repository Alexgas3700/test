# Email Templates для n8n Workflow

Коллекция готовых HTML-шаблонов для email-рассылок.

## 📧 Шаблон 1: Промо-акция

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }
    .container {
      max-width: 600px;
      margin: 20px auto;
      background-color: #ffffff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 40px 20px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 28px;
      font-weight: bold;
    }
    .content {
      padding: 40px 30px;
    }
    .content h2 {
      color: #667eea;
      font-size: 24px;
      margin-top: 0;
    }
    .highlight-box {
      background-color: #f8f9ff;
      border-left: 4px solid #667eea;
      padding: 20px;
      margin: 20px 0;
    }
    .cta-button {
      display: inline-block;
      padding: 15px 40px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-decoration: none;
      border-radius: 50px;
      font-weight: bold;
      margin: 20px 0;
      transition: transform 0.3s;
    }
    .cta-button:hover {
      transform: scale(1.05);
    }
    .features {
      display: table;
      width: 100%;
      margin: 20px 0;
    }
    .feature-item {
      display: table-row;
    }
    .feature-icon {
      display: table-cell;
      width: 40px;
      padding: 10px;
      vertical-align: top;
    }
    .feature-text {
      display: table-cell;
      padding: 10px;
      vertical-align: top;
    }
    .footer {
      background-color: #f8f9fa;
      padding: 30px;
      text-align: center;
      font-size: 14px;
      color: #666;
    }
    .footer a {
      color: #667eea;
      text-decoration: none;
    }
    .social-links {
      margin: 20px 0;
    }
    .social-links a {
      display: inline-block;
      margin: 0 10px;
      color: #667eea;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎉 Специальное предложение!</h1>
    </div>
    
    <div class="content">
      <h2>Здравствуйте, {{ $json.Name }}!</h2>
      
      <p>Мы рады представить эксклюзивное предложение специально для {{ $json.Company }}.</p>
      
      <div class="highlight-box">
        <h3 style="margin-top: 0; color: #667eea;">🔥 Только до конца месяца!</h3>
        <p style="font-size: 18px; margin: 10px 0;"><strong>Скидка 30%</strong> на все наши услуги</p>
      </div>
      
      <div class="features">
        <div class="feature-item">
          <div class="feature-icon">✅</div>
          <div class="feature-text">
            <strong>Премиум поддержка</strong><br>
            Круглосуточная помощь от наших экспертов
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">✅</div>
          <div class="feature-text">
            <strong>Бесплатное обучение</strong><br>
            Полный курс по использованию наших продуктов
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">✅</div>
          <div class="feature-text">
            <strong>Приоритетный доступ</strong><br>
            Первыми узнавайте о новых функциях
          </div>
        </div>
      </div>
      
      <center>
        <a href="https://example.com/promo?email={{ $json.Email }}" class="cta-button">
          Воспользоваться предложением
        </a>
      </center>
      
      <p style="color: #666; font-size: 14px; margin-top: 30px;">
        Это предложение действительно только для {{ $json.Company }} и истекает 28 февраля 2026.
      </p>
    </div>
    
    <div class="footer">
      <div class="social-links">
        <a href="https://facebook.com/yourcompany">Facebook</a> |
        <a href="https://twitter.com/yourcompany">Twitter</a> |
        <a href="https://linkedin.com/company/yourcompany">LinkedIn</a>
      </div>
      
      <p>© 2026 Ваша Компания. Все права защищены.</p>
      
      <p style="margin-top: 20px;">
        <a href="https://example.com/unsubscribe?email={{ $json.Email }}">Отписаться от рассылки</a> |
        <a href="https://example.com/preferences?email={{ $json.Email }}">Настройки рассылки</a>
      </p>
      
      <p style="font-size: 12px; color: #999; margin-top: 20px;">
        Вы получили это письмо, потому что зарегистрированы на нашем сайте.<br>
        Адрес: г. Москва, ул. Примерная, д. 123, офис 456
      </p>
    </div>
  </div>
</body>
</html>
```

## 📰 Шаблон 2: Новостная рассылка

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: Georgia, 'Times New Roman', serif;
      line-height: 1.7;
      color: #2c3e50;
      margin: 0;
      padding: 0;
      background-color: #ecf0f1;
    }
    .container {
      max-width: 650px;
      margin: 20px auto;
      background-color: #ffffff;
    }
    .header {
      background-color: #2c3e50;
      color: white;
      padding: 30px;
      border-bottom: 4px solid #e74c3c;
    }
    .logo {
      font-size: 32px;
      font-weight: bold;
      margin: 0;
    }
    .tagline {
      font-size: 14px;
      margin: 5px 0 0 0;
      opacity: 0.8;
    }
    .content {
      padding: 40px 30px;
    }
    .greeting {
      font-size: 18px;
      color: #e74c3c;
      margin-bottom: 20px;
    }
    .article {
      margin-bottom: 40px;
      padding-bottom: 30px;
      border-bottom: 1px solid #ecf0f1;
    }
    .article:last-child {
      border-bottom: none;
    }
    .article-title {
      font-size: 24px;
      color: #2c3e50;
      margin: 0 0 10px 0;
    }
    .article-meta {
      font-size: 13px;
      color: #95a5a6;
      margin-bottom: 15px;
    }
    .article-excerpt {
      font-size: 16px;
      line-height: 1.6;
      margin-bottom: 15px;
    }
    .read-more {
      display: inline-block;
      color: #e74c3c;
      text-decoration: none;
      font-weight: bold;
      border-bottom: 2px solid #e74c3c;
      padding-bottom: 2px;
    }
    .footer {
      background-color: #34495e;
      color: white;
      padding: 30px;
      font-size: 14px;
    }
    .footer a {
      color: #e74c3c;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="logo">📰 Новости Компании</h1>
      <p class="tagline">Еженедельный дайджест | 11 февраля 2026</p>
    </div>
    
    <div class="content">
      <p class="greeting">Добрый день, {{ $json.Name }}!</p>
      
      <p>Представляем вашему вниманию главные новости этой недели.</p>
      
      <div class="article">
        <h2 class="article-title">Запуск нового продукта</h2>
        <p class="article-meta">10 февраля 2026 • Продукты</p>
        <p class="article-excerpt">
          Мы рады объявить о запуске нашего нового продукта, который революционизирует 
          способ работы с данными. Благодаря инновационным технологиям и интуитивному 
          интерфейсу, теперь вы сможете достигать результатов в 3 раза быстрее.
        </p>
        <a href="https://example.com/news/new-product" class="read-more">Читать далее →</a>
      </div>
      
      <div class="article">
        <h2 class="article-title">Успешный кейс: {{ $json.Company }}</h2>
        <p class="article-meta">8 февраля 2026 • Кейсы</p>
        <p class="article-excerpt">
          Узнайте, как компании из вашей отрасли используют наши решения для 
          оптимизации бизнес-процессов и увеличения прибыли. Реальные цифры и 
          конкретные результаты.
        </p>
        <a href="https://example.com/case-studies" class="read-more">Читать далее →</a>
      </div>
      
      <div class="article">
        <h2 class="article-title">Вебинар: Лучшие практики 2026</h2>
        <p class="article-meta">15 февраля 2026, 14:00 МСК • События</p>
        <p class="article-excerpt">
          Приглашаем вас на бесплатный вебинар, где наши эксперты поделятся 
          актуальными трендами и практическими советами. Регистрация обязательна.
        </p>
        <a href="https://example.com/webinar-registration" class="read-more">Зарегистрироваться →</a>
      </div>
    </div>
    
    <div class="footer">
      <p><strong>Ваша Компания</strong></p>
      <p>г. Москва, ул. Примерная, д. 123</p>
      <p>
        <a href="https://example.com">Сайт</a> | 
        <a href="https://example.com/blog">Блог</a> | 
        <a href="https://example.com/contact">Контакты</a>
      </p>
      <p style="margin-top: 20px; font-size: 12px; opacity: 0.8;">
        <a href="https://example.com/unsubscribe?email={{ $json.Email }}">Отписаться</a> | 
        <a href="https://example.com/preferences?email={{ $json.Email }}">Настройки</a>
      </p>
    </div>
  </div>
</body>
</html>
```

## 🎓 Шаблон 3: Образовательный контент

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
      background-color: #f0f4f8;
    }
    .container {
      max-width: 600px;
      margin: 20px auto;
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: white;
      padding: 40px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 26px;
    }
    .content {
      padding: 40px 30px;
    }
    .tip-box {
      background-color: #e3f2fd;
      border-left: 4px solid #2196f3;
      padding: 20px;
      margin: 20px 0;
      border-radius: 4px;
    }
    .tip-box h3 {
      margin-top: 0;
      color: #1976d2;
    }
    .steps {
      counter-reset: step-counter;
      list-style: none;
      padding: 0;
    }
    .steps li {
      counter-increment: step-counter;
      margin-bottom: 30px;
      padding-left: 60px;
      position: relative;
    }
    .steps li::before {
      content: counter(step-counter);
      position: absolute;
      left: 0;
      top: 0;
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: white;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 18px;
    }
    .cta-button {
      display: block;
      text-align: center;
      padding: 15px 30px;
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: white;
      text-decoration: none;
      border-radius: 4px;
      font-weight: bold;
      margin: 30px 0;
    }
    .footer {
      background-color: #f8f9fa;
      padding: 30px;
      text-align: center;
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>💡 Совет недели</h1>
      <p style="margin: 10px 0 0 0; opacity: 0.9;">Повышайте эффективность вместе с нами</p>
    </div>
    
    <div class="content">
      <p>Здравствуйте, {{ $json.Name }}!</p>
      
      <p>На этой неделе мы подготовили для вас практическое руководство по оптимизации рабочих процессов.</p>
      
      <div class="tip-box">
        <h3>💡 Совет эксперта</h3>
        <p>
          Автоматизация рутинных задач может сэкономить до 40% рабочего времени. 
          Начните с малого и постепенно расширяйте автоматизацию.
        </p>
      </div>
      
      <h2 style="color: #1e3c72;">5 шагов к автоматизации</h2>
      
      <ol class="steps">
        <li>
          <strong>Определите повторяющиеся задачи</strong><br>
          Проанализируйте свой рабочий день и выделите задачи, которые повторяются регулярно.
        </li>
        <li>
          <strong>Оцените потенциал автоматизации</strong><br>
          Не все задачи подходят для автоматизации. Выберите те, которые занимают много времени.
        </li>
        <li>
          <strong>Выберите подходящие инструменты</strong><br>
          Изучите доступные решения и выберите те, которые лучше всего подходят для ваших задач.
        </li>
        <li>
          <strong>Начните с пилотного проекта</strong><br>
          Автоматизируйте одну задачу и оцените результаты перед масштабированием.
        </li>
        <li>
          <strong>Измеряйте и оптимизируйте</strong><br>
          Отслеживайте эффективность автоматизации и вносите улучшения.
        </li>
      </ol>
      
      <a href="https://example.com/automation-guide" class="cta-button">
        Скачать полное руководство
      </a>
      
      <p style="background-color: #fff3cd; padding: 15px; border-radius: 4px; border-left: 4px solid #ffc107;">
        <strong>📅 Предстоящее событие:</strong><br>
        Бесплатный мастер-класс по автоматизации<br>
        18 февраля 2026, 15:00 МСК
      </p>
    </div>
    
    <div class="footer">
      <p><strong>Ваша Компания</strong></p>
      <p>Помогаем бизнесу работать эффективнее</p>
      <p style="margin-top: 20px;">
        <a href="https://example.com/unsubscribe?email={{ $json.Email }}" style="color: #1e3c72;">Отписаться</a> |
        <a href="https://example.com/preferences?email={{ $json.Email }}" style="color: #1e3c72;">Настройки</a>
      </p>
    </div>
  </div>
</body>
</html>
```

## 🎁 Шаблон 4: Приветственное письмо

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Arial', sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
      background-color: #f5f5f5;
    }
    .container {
      max-width: 600px;
      margin: 20px auto;
      background-color: #ffffff;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .header {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
      padding: 50px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 32px;
    }
    .content {
      padding: 40px 30px;
    }
    .welcome-message {
      font-size: 18px;
      text-align: center;
      margin-bottom: 30px;
      color: #f5576c;
    }
    .feature-grid {
      display: table;
      width: 100%;
      margin: 30px 0;
    }
    .feature-row {
      display: table-row;
    }
    .feature-cell {
      display: table-cell;
      width: 50%;
      padding: 20px;
      text-align: center;
      vertical-align: top;
    }
    .feature-icon {
      font-size: 48px;
      margin-bottom: 10px;
    }
    .cta-button {
      display: block;
      text-align: center;
      padding: 18px 40px;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
      text-decoration: none;
      border-radius: 50px;
      font-weight: bold;
      font-size: 16px;
      margin: 30px auto;
      max-width: 300px;
    }
    .footer {
      background-color: #f8f9fa;
      padding: 30px;
      text-align: center;
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎉 Добро пожаловать!</h1>
      <p style="margin: 10px 0 0 0; font-size: 18px;">Мы рады видеть вас в нашем сообществе</p>
    </div>
    
    <div class="content">
      <p class="welcome-message">
        <strong>Здравствуйте, {{ $json.Name }}!</strong>
      </p>
      
      <p>
        Спасибо, что присоединились к нам! Мы в {{ $json.Company }} стремимся предоставить 
        вам лучший опыт и помочь достичь ваших целей.
      </p>
      
      <h2 style="text-align: center; color: #f5576c;">Что вас ждет?</h2>
      
      <div class="feature-grid">
        <div class="feature-row">
          <div class="feature-cell">
            <div class="feature-icon">📚</div>
            <h3 style="margin: 10px 0;">Обучение</h3>
            <p>Доступ к базе знаний и обучающим материалам</p>
          </div>
          <div class="feature-cell">
            <div class="feature-icon">🎯</div>
            <h3 style="margin: 10px 0;">Поддержка</h3>
            <p>Помощь экспертов 24/7</p>
          </div>
        </div>
        <div class="feature-row">
          <div class="feature-cell">
            <div class="feature-icon">🚀</div>
            <h3 style="margin: 10px 0;">Инновации</h3>
            <p>Первыми узнавайте о новых функциях</p>
          </div>
          <div class="feature-cell">
            <div class="feature-icon">👥</div>
            <h3 style="margin: 10px 0;">Сообщество</h3>
            <p>Общайтесь с единомышленниками</p>
          </div>
        </div>
      </div>
      
      <a href="https://example.com/get-started?email={{ $json.Email }}" class="cta-button">
        Начать работу
      </a>
      
      <div style="background-color: #fff9e6; padding: 20px; border-radius: 8px; margin-top: 30px;">
        <h3 style="margin-top: 0; color: #f5576c;">🎁 Специальный бонус</h3>
        <p>
          В качестве приветствия мы дарим вам <strong>скидку 15%</strong> на первую покупку!<br>
          Используйте промокод: <strong style="color: #f5576c;">WELCOME2026</strong>
        </p>
      </div>
      
      <p style="margin-top: 30px; text-align: center;">
        Если у вас есть вопросы, не стесняйтесь обращаться к нам.<br>
        Мы всегда рады помочь!
      </p>
    </div>
    
    <div class="footer">
      <p><strong>С уважением,<br>Команда Вашей Компании</strong></p>
      <p style="margin-top: 20px;">
        <a href="https://example.com" style="color: #f5576c;">Сайт</a> |
        <a href="https://example.com/help" style="color: #f5576c;">Помощь</a> |
        <a href="https://example.com/contact" style="color: #f5576c;">Контакты</a>
      </p>
      <p style="margin-top: 20px; font-size: 12px;">
        <a href="https://example.com/unsubscribe?email={{ $json.Email }}" style="color: #666;">Отписаться</a>
      </p>
    </div>
  </div>
</body>
</html>
```

## 📝 Как использовать шаблоны

### В узле "Personalize Emails"

1. Откройте workflow в n8n
2. Найдите узел "Personalize Emails" (тип: Code)
3. Замените содержимое переменной `body` на выбранный шаблон
4. Убедитесь, что все переменные персонализации корректны:
   - `{{ $json.Name }}` - имя получателя
   - `{{ $json.Company }}` - название компании
   - `{{ $json.Email }}` - email получателя

### Переменные персонализации

Все шаблоны поддерживают следующие переменные:

- `{{ $json.Name }}` - Имя контакта
- `{{ $json.Company }}` - Название компании
- `{{ $json.Email }}` - Email адрес
- `{{ $json.LastContact }}` - Дата последнего контакта

### Тестирование шаблонов

Перед использованием рекомендуется:

1. Отправить тестовое письмо себе
2. Проверить отображение в разных почтовых клиентах:
   - Gmail
   - Outlook
   - Apple Mail
   - Мобильные клиенты
3. Проверить все ссылки
4. Убедиться, что персонализация работает корректно

## 🎨 Кастомизация

### Изменение цветовой схемы

Найдите в CSS секции `background` и `color` и замените цвета:

```css
/* Градиент */
background: linear-gradient(135deg, #ВАШ_ЦВЕТ_1 0%, #ВАШ_ЦВЕТ_2 100%);

/* Сплошной цвет */
background-color: #ВАШ_ЦВЕТ;
```

### Добавление логотипа

Вставьте в секцию header:

```html
<img src="https://example.com/logo.png" alt="Logo" style="max-width: 200px; height: auto;">
```

### Изменение шрифтов

Замените в `font-family`:

```css
font-family: 'Ваш шрифт', Arial, sans-serif;
```

Для использования Google Fonts добавьте в `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
```

## 📱 Адаптивность

Все шаблоны адаптированы для мобильных устройств благодаря:

- `max-width: 600px` для основного контейнера
- `<meta name="viewport">` для корректного масштабирования
- Относительные размеры шрифтов
- Гибкие изображения с `max-width: 100%`

## ✅ Чек-лист перед отправкой

- [ ] Все ссылки работают корректно
- [ ] Персонализация настроена
- [ ] Ссылка отписки присутствует
- [ ] Контактная информация актуальна
- [ ] Тема письма привлекательна
- [ ] Протестировано на мобильных устройствах
- [ ] Проверена орфография и грамматика
- [ ] CTA (призыв к действию) четкий и понятный

---

**Совет:** Регулярно обновляйте шаблоны на основе аналитики открытий и кликов!
