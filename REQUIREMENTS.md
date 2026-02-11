# Требования и зависимости

## Системные требования

### n8n

- **Минимальная версия:** 1.0.0
- **Рекомендуемая версия:** 1.20.0 или выше
- **Node.js:** 18.x или выше
- **NPM:** 9.x или выше

### Операционная система

- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- macOS 11+ (Big Sur или новее)
- Windows 10/11 (с WSL2 для лучшей производительности)

### Аппаратные требования

**Минимальные:**
- CPU: 1 ядро
- RAM: 512 MB
- Диск: 1 GB свободного места

**Рекомендуемые:**
- CPU: 2+ ядра
- RAM: 2 GB
- Диск: 5 GB свободного места
- SSD для лучшей производительности

## Программные зависимости

### n8n Nodes (встроенные)

Следующие узлы используются в workflow и входят в стандартную поставку n8n:

- `n8n-nodes-base.scheduleTrigger` - для планирования запусков
- `n8n-nodes-base.httpRequest` - для HTTP запросов
- `n8n-nodes-base.filter` - для фильтрации данных
- `n8n-nodes-base.if` - для условной логики
- `n8n-nodes-base.code` - для выполнения JavaScript кода
- `n8n-nodes-base.merge` - для объединения данных
- `n8n-nodes-base.vk` - для работы с VK API

### Дополнительные узлы (опционально)

Если вы хотите расширить функциональность:

```bash
# Для работы с базами данных
npm install n8n-nodes-postgres
npm install n8n-nodes-mysql
npm install n8n-nodes-mongodb

# Для уведомлений
npm install n8n-nodes-telegram
npm install n8n-nodes-slack

# Для работы с файлами
npm install n8n-nodes-google-drive
npm install n8n-nodes-dropbox
```

## VK API требования

### VK приложение

1. **Тип приложения:** Standalone приложение
2. **Права доступа (scope):**
   - `wall` - публикация на стене
   - `photos` - загрузка и управление фотографиями
   - `groups` - управление группами (для публикации от имени группы)

### API версия

- **Минимальная:** 5.131
- **Рекомендуемая:** 5.131 или выше

### Ограничения VK API

- **Rate Limiting:** 3 запроса в секунду
- **Максимальный размер изображения:** 50 МБ
- **Поддерживаемые форматы изображений:** JPG, PNG, GIF
- **Максимальная длина текста поста:** 16384 символа
- **Максимальное количество вложений:** 10

## Сетевые требования

### Исходящие соединения

Workflow требует доступа к следующим доменам:

```
api.vk.com          - VK API
oauth.vk.com        - VK OAuth
your-api.com        - Ваш источник контента (настраивается)
```

### Порты

- **HTTP:** 80
- **HTTPS:** 443

### Firewall правила

Если используется firewall, разрешите исходящие соединения на порты 80 и 443.

## Установка n8n

### Вариант 1: npm (рекомендуется для разработки)

```bash
# Глобальная установка
npm install n8n -g

# Запуск
n8n start
```

### Вариант 2: Docker (рекомендуется для production)

```bash
# Создание docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
      - N8N_HOST=your-domain.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://your-domain.com/
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows

volumes:
  n8n_data:
EOF

# Запуск
docker-compose up -d
```

### Вариант 3: npx (для быстрого старта)

```bash
npx n8n
```

### Вариант 4: Desktop приложение

Скачайте n8n Desktop с официального сайта: https://n8n.io/download

## Настройка окружения

### Переменные окружения n8n

```bash
# Базовая конфигурация
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=your_secure_password

# Webhook конфигурация
export WEBHOOK_URL=https://your-domain.com/

# Timezone
export GENERIC_TIMEZONE=Europe/Moscow

# Execution mode
export EXECUTIONS_PROCESS=main

# Logging
export N8N_LOG_LEVEL=info
export N8N_LOG_OUTPUT=console,file
export N8N_LOG_FILE_LOCATION=/var/log/n8n/

# Encryption key (для production)
export N8N_ENCRYPTION_KEY=your_encryption_key_here
```

### Переменные для VK Automation

```bash
# VK Configuration
export VK_GROUP_ID=123456789
export VK_API_VERSION=5.131

# Content Source
export CONTENT_API_URL=https://your-api.com/posts
export CONTENT_API_KEY=your_api_key

# Schedule
export SCHEDULE_INTERVAL_HOURS=1
```

## База данных (опционально)

n8n использует SQLite по умолчанию, но для production рекомендуется PostgreSQL или MySQL.

### PostgreSQL (рекомендуется)

```bash
# Установка PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres createdb n8n

# Настройка n8n для PostgreSQL
export DB_TYPE=postgresdb
export DB_POSTGRESDB_HOST=localhost
export DB_POSTGRESDB_PORT=5432
export DB_POSTGRESDB_DATABASE=n8n
export DB_POSTGRESDB_USER=n8n_user
export DB_POSTGRESDB_PASSWORD=n8n_password
```

### MySQL

```bash
# Установка MySQL
sudo apt-get install mysql-server

# Создание базы данных
mysql -u root -p
CREATE DATABASE n8n;
CREATE USER 'n8n_user'@'localhost' IDENTIFIED BY 'n8n_password';
GRANT ALL PRIVILEGES ON n8n.* TO 'n8n_user'@'localhost';
FLUSH PRIVILEGES;

# Настройка n8n для MySQL
export DB_TYPE=mysqldb
export DB_MYSQLDB_HOST=localhost
export DB_MYSQLDB_PORT=3306
export DB_MYSQLDB_DATABASE=n8n
export DB_MYSQLDB_USER=n8n_user
export DB_MYSQLDB_PASSWORD=n8n_password
```

## Безопасность

### SSL/TLS сертификаты

Для production обязательно используйте HTTPS:

```bash
# Let's Encrypt (рекомендуется)
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com

# Настройка n8n
export N8N_PROTOCOL=https
export N8N_SSL_KEY=/etc/letsencrypt/live/your-domain.com/privkey.pem
export N8N_SSL_CERT=/etc/letsencrypt/live/your-domain.com/fullchain.pem
```

### Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 5678/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 5678 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## Мониторинг и логирование

### Логи n8n

```bash
# Просмотр логов (Docker)
docker-compose logs -f n8n

# Просмотр логов (systemd)
sudo journalctl -u n8n -f

# Просмотр файлов логов
tail -f /var/log/n8n/n8n.log
```

### Мониторинг производительности

```bash
# Установка PM2 для мониторинга
npm install pm2 -g

# Запуск n8n через PM2
pm2 start n8n

# Мониторинг
pm2 monit

# Логи
pm2 logs n8n
```

## Резервное копирование

### Backup workflow

```bash
# Экспорт workflow
# В n8n UI: Settings → Export Workflow

# Backup базы данных (PostgreSQL)
pg_dump -U n8n_user n8n > n8n_backup_$(date +%Y%m%d).sql

# Backup базы данных (MySQL)
mysqldump -u n8n_user -p n8n > n8n_backup_$(date +%Y%m%d).sql

# Backup credentials и данных
tar -czf n8n_data_backup_$(date +%Y%m%d).tar.gz ~/.n8n/
```

### Восстановление

```bash
# Восстановление базы данных (PostgreSQL)
psql -U n8n_user n8n < n8n_backup_20260211.sql

# Восстановление базы данных (MySQL)
mysql -u n8n_user -p n8n < n8n_backup_20260211.sql

# Восстановление данных
tar -xzf n8n_data_backup_20260211.tar.gz -C ~/
```

## Обновление

### Обновление n8n (npm)

```bash
# Проверка текущей версии
n8n --version

# Обновление до последней версии
npm update -g n8n

# Обновление до конкретной версии
npm install -g n8n@1.20.0
```

### Обновление n8n (Docker)

```bash
# Остановка контейнера
docker-compose down

# Обновление образа
docker-compose pull

# Запуск с новой версией
docker-compose up -d
```

## Производительность

### Оптимизация для большого количества постов

```bash
# Увеличение лимитов Node.js
export NODE_OPTIONS="--max-old-space-size=4096"

# Настройка очереди выполнения
export EXECUTIONS_MODE=queue
export QUEUE_BULL_REDIS_HOST=localhost
export QUEUE_BULL_REDIS_PORT=6379
```

### Redis для очереди (опционально)

```bash
# Установка Redis
sudo apt-get install redis-server

# Настройка n8n для использования Redis
export EXECUTIONS_MODE=queue
export QUEUE_BULL_REDIS_HOST=localhost
export QUEUE_BULL_REDIS_PORT=6379
export QUEUE_BULL_REDIS_DB=0
```

## Проверка установки

### Checklist

- [ ] n8n установлен и запущен
- [ ] n8n доступен через браузер (http://localhost:5678)
- [ ] VK приложение создано и настроено
- [ ] VK OAuth2 credentials добавлены в n8n
- [ ] Workflow импортирован
- [ ] Переменные окружения настроены
- [ ] Источник контента настроен и доступен
- [ ] Тестовый запуск workflow выполнен успешно
- [ ] Пост опубликован в VK
- [ ] Логирование работает корректно

### Тестовая команда

```bash
# Проверка доступности n8n
curl http://localhost:5678/healthz

# Проверка VK API
curl "https://api.vk.com/method/groups.getById?group_id=YOUR_GROUP_ID&access_token=YOUR_TOKEN&v=5.131"
```

## Поддержка

### Документация

- n8n: https://docs.n8n.io/
- VK API: https://dev.vk.com/reference

### Сообщество

- n8n Community: https://community.n8n.io/
- VK Developers: https://vk.com/dev

### Известные проблемы

1. **VK API rate limiting** - используйте задержки между запросами
2. **Большие изображения** - оптимизируйте размер перед загрузкой
3. **Timeout при загрузке** - увеличьте timeout в HTTP Request узлах

## Версии компонентов

Протестировано с:

- n8n: 1.20.0
- Node.js: 18.19.0
- npm: 9.8.1
- VK API: 5.131
- Docker: 24.0.7 (опционально)
- PostgreSQL: 14.10 (опционально)

---

**Дата последнего обновления:** 11 февраля 2026
