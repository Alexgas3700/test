# SMTP Configuration Examples

## Gmail SMTP

```
Host: smtp.gmail.com
Port: 587 (TLS) or 465 (SSL)
User: your-email@gmail.com
Password: App Password (not your regular password)
Secure: true
```

### Настройка App Password для Gmail:

1. Перейдите в Google Account Settings
2. Security → 2-Step Verification (включите, если не включено)
3. App passwords → Select app: Mail → Select device: Other
4. Скопируйте сгенерированный пароль
5. Используйте этот пароль в n8n

**Примечание**: Gmail имеет лимит 500 писем в день для бесплатных аккаунтов.

---

## Yandex SMTP

```
Host: smtp.yandex.ru
Port: 587 (TLS) or 465 (SSL)
User: your-email@yandex.ru
Password: your-password
Secure: true
```

### Особенности:

- Лимит: 500 писем в день
- Требуется подтверждение email
- Поддержка DKIM

---

## Mail.ru SMTP

```
Host: smtp.mail.ru
Port: 587 (TLS) or 465 (SSL)
User: your-email@mail.ru
Password: your-password
Secure: true
```

### Особенности:

- Лимит: 300 писем в день
- Требуется включить "Доступ по протоколу IMAP/POP3/SMTP"
- Настройки → Почта → Клиенты

---

## Microsoft 365 / Outlook SMTP

```
Host: smtp.office365.com
Port: 587
User: your-email@outlook.com
Password: your-password
Secure: true
```

### Особенности:

- Лимит: 300 писем в день (для личных аккаунтов)
- Лимит: 10,000 писем в день (для бизнес аккаунтов)
- Поддержка OAuth2

---

## Amazon SES SMTP

```
Host: email-smtp.us-east-1.amazonaws.com (зависит от региона)
Port: 587 (TLS) or 465 (SSL)
User: Your SMTP Username
Password: Your SMTP Password
Secure: true
```

### Настройка:

1. Создайте аккаунт AWS
2. Перейдите в Amazon SES
3. Verify your domain или email
4. Create SMTP credentials
5. Выйдите из sandbox mode для production

### Особенности:

- Sandbox: 200 писем в день
- Production: до 50,000 писем в день (можно увеличить)
- Очень низкая стоимость: $0.10 за 1,000 писем

---

## Mailjet SMTP

```
Host: in-v3.mailjet.com
Port: 587 (TLS) or 465 (SSL)
User: Your Mailjet API Key
Password: Your Mailjet Secret Key
Secure: true
```

### Особенности:

- Free tier: 6,000 писем в месяц, 200 писем в день
- Отличная доставляемость
- Встроенная аналитика

---

## Sendinblue (Brevo) SMTP

```
Host: smtp-relay.sendinblue.com
Port: 587
User: your-email@example.com
Password: Your SMTP Key
Secure: true
```

### Особенности:

- Free tier: 300 писем в день
- Встроенная аналитика
- SMS интеграция

---

## Custom SMTP Server

```
Host: mail.yourdomain.com
Port: 587 (TLS) or 465 (SSL) or 25 (без шифрования)
User: your-username
Password: your-password
Secure: true (рекомендуется)
```

### Рекомендации для собственного SMTP:

1. **Настройте SPF запись**:
   ```
   v=spf1 ip4:YOUR_SERVER_IP ~all
   ```

2. **Настройте DKIM**:
   - Сгенерируйте DKIM ключи
   - Добавьте TXT запись в DNS

3. **Настройте DMARC**:
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
   ```

4. **Настройте reverse DNS (PTR)**:
   - Убедитесь, что IP сервера имеет правильную PTR запись

5. **Мониторинг репутации**:
   - Проверяйте blacklist: https://mxtoolbox.com/blacklists.aspx
   - Следите за bounce rate

---

## Сравнительная таблица

| Провайдер | Free Tier | Цена | Лимит | Доставляемость | Сложность |
|-----------|-----------|------|-------|----------------|-----------|
| Gmail | 500/день | Бесплатно | 500/день | Отличная | Легко |
| Yandex | 500/день | Бесплатно | 500/день | Хорошая | Легко |
| Mail.ru | 300/день | Бесплатно | 300/день | Хорошая | Легко |
| Outlook | 300/день | Бесплатно | 300/день | Отличная | Легко |
| Amazon SES | 200/день | $0.10/1000 | 50,000/день+ | Отличная | Средне |
| Mailjet | 6,000/месяц | $15/месяц+ | 30,000/месяц+ | Отличная | Легко |
| Sendinblue | 300/день | $25/месяц+ | 20,000/месяц+ | Отличная | Легко |
| Custom | - | Стоимость сервера | Зависит | Зависит | Сложно |

---

## Рекомендации по выбору

### Для тестирования и разработки:
- **Gmail** или **Yandex** - просто и бесплатно

### Для малого бизнеса (до 10,000 писем/месяц):
- **Mailjet** или **Sendinblue** - хорошее соотношение цена/качество

### Для среднего бизнеса (10,000 - 100,000 писем/месяц):
- **Amazon SES** - самый дешевый вариант
- **SendGrid** - больше функций и аналитики

### Для крупного бизнеса (100,000+ писем/месяц):
- **Amazon SES** - масштабируемость и низкая цена
- **SendGrid** или **Mailgun** - профессиональные функции

### Для транзакционных писем:
- **Amazon SES** или **Mailgun** - высокая надежность

### Для маркетинговых рассылок:
- **SendGrid**, **Mailjet**, или **Sendinblue** - встроенная аналитика

---

## Устранение проблем

### Письма попадают в спам

1. Настройте SPF, DKIM, DMARC
2. Используйте подтвержденный домен отправителя
3. Избегайте спам-слов в теме
4. Добавьте физический адрес компании
5. Всегда добавляйте ссылку отписки

### Низкая скорость отправки

1. Используйте rate limiting
2. Проверьте лимиты провайдера
3. Рассмотрите использование нескольких SMTP серверов
4. Используйте dedicated IP (для больших объемов)

### Ошибки аутентификации

1. Проверьте username и password
2. Для Gmail используйте App Password
3. Проверьте, включен ли доступ для "менее безопасных приложений"
4. Проверьте firewall и порты

### Таймауты соединения

1. Проверьте firewall
2. Убедитесь, что порт открыт
3. Попробуйте другой порт (587 вместо 465)
4. Проверьте DNS резолюцию

---

## Безопасность

### Лучшие практики:

1. **Всегда используйте TLS/SSL**
2. **Не храните пароли в коде** - используйте переменные окружения
3. **Используйте App Passwords** вместо основных паролей
4. **Ротация credentials** - меняйте пароли регулярно
5. **Мониторинг** - отслеживайте подозрительную активность
6. **Rate limiting** - защита от злоупотреблений
7. **Логирование** - храните логи отправок

### Хранение credentials в n8n:

n8n шифрует все credentials. Убедитесь, что:

1. Используете сильный `N8N_ENCRYPTION_KEY`
2. Регулярно делаете backup базы данных n8n
3. Ограничиваете доступ к n8n instance
4. Используете HTTPS для веб-интерфейса
