# Руководство по развертыванию VK Content Workflow

## Содержание

- [Быстрый старт](#быстрый-старт)
- [Развертывание с Docker](#развертывание-с-docker)
- [Развертывание без Docker](#развертывание-без-docker)
- [Настройка VK API](#настройка-vk-api)
- [Импорт workflow](#импорт-workflow)
- [Настройка credentials](#настройка-credentials)
- [Тестирование](#тестирование)
- [Production deployment](#production-deployment)
- [Мониторинг](#мониторинг)
- [Резервное копирование](#резервное-копирование)

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose (для Docker-развертывания)
- Node.js 18+ (для развертывания без Docker)
- PostgreSQL 12+ (опционально)
- VK API токен

### Шаг 1: Клонирование репозитория

```bash
git clone <repository-url>
cd vk-content-workflow
```

### Шаг 2: Настройка переменных окружения

```bash
cp .env.example .env
nano .env  # Отредактируйте файл с вашими настройками
```

### Шаг 3: Запуск с Docker

```bash
# Базовая конфигурация
docker-compose up -d

# С дополнительными сервисами (pgAdmin)
docker-compose --profile dev up -d

# Production конфигурация (с Redis и Nginx)
docker-compose --profile production up -d
```

### Шаг 4: Доступ к n8n

Откройте браузер и перейдите по адресу:
- Development: http://localhost:5678
- Production: https://your-domain.com

Логин и пароль указаны в `.env` файле.

## Развертывание с Docker

### Структура Docker Compose

```
services:
  - n8n (основной сервис)
  - postgres (база данных)
  - redis (опционально, для queue mode)
  - pgadmin (опционально, для управления БД)
  - nginx (опционально, reverse proxy)
  - backup (опционально, резервное копирование)
```

### Базовое развертывание

```bash
# 1. Создайте .env файл
cp .env.example .env

# 2. Отредактируйте переменные
nano .env

# 3. Запустите сервисы
docker-compose up -d

# 4. Проверьте статус
docker-compose ps

# 5. Просмотр логов
docker-compose logs -f n8n
```

### Development режим

```bash
# Запуск с pgAdmin для управления БД
docker-compose --profile dev up -d

# Доступ к pgAdmin: http://localhost:5050
# Email: admin@example.com (из .env)
# Password: admin (из .env)
```

### Production режим

```bash
# Запуск с Redis и Nginx
docker-compose --profile production up -d

# Проверка статуса
docker-compose --profile production ps
```

### Управление контейнерами

```bash
# Остановка сервисов
docker-compose down

# Остановка с удалением volumes (ВНИМАНИЕ: удалит данные!)
docker-compose down -v

# Перезапуск сервиса
docker-compose restart n8n

# Просмотр логов конкретного сервиса
docker-compose logs -f n8n

# Выполнение команды в контейнере
docker-compose exec n8n /bin/sh

# Обновление образов
docker-compose pull
docker-compose up -d
```

## Развертывание без Docker

### Установка n8n

```bash
# Глобальная установка
npm install n8n -g

# Или локальная установка
npm install n8n
```

### Настройка PostgreSQL

```bash
# Создание базы данных
createdb vk_content

# Импорт схемы
psql -d vk_content -f database/schema.sql

# Или через psql
psql -U postgres
CREATE DATABASE vk_content;
\c vk_content
\i database/schema.sql
```

### Настройка переменных окружения

```bash
# Linux/Mac
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=secure_password
export DB_TYPE=postgresdb
export DB_POSTGRESDB_HOST=localhost
export DB_POSTGRESDB_PORT=5432
export DB_POSTGRESDB_DATABASE=vk_content
export DB_POSTGRESDB_USER=postgres
export DB_POSTGRESDB_PASSWORD=your_password

# Windows
set N8N_BASIC_AUTH_ACTIVE=true
set N8N_BASIC_AUTH_USER=admin
# ... и т.д.
```

### Запуск n8n

```bash
# Запуск в обычном режиме
n8n start

# Запуск с указанием порта
n8n start --port 5678

# Запуск в production режиме
NODE_ENV=production n8n start

# Запуск с webhook URL
n8n start --tunnel
```

### Запуск как системный сервис (Linux)

```bash
# Создайте systemd unit файл
sudo nano /etc/systemd/system/n8n.service
```

```ini
[Unit]
Description=n8n - Workflow Automation
After=network.target

[Service]
Type=simple
User=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/n8n start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Активируйте и запустите сервис
sudo systemctl daemon-reload
sudo systemctl enable n8n
sudo systemctl start n8n

# Проверка статуса
sudo systemctl status n8n

# Просмотр логов
sudo journalctl -u n8n -f
```

## Настройка VK API

### Создание приложения VK

1. Перейдите на https://vk.com/apps?act=manage
2. Нажмите "Создать приложение"
3. Выберите тип "Standalone-приложение"
4. Заполните название и категорию
5. Нажмите "Создать"

### Получение токена доступа

#### Способ 1: Через OAuth (рекомендуется)

```bash
# 1. Получите authorization code
https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,photos,video,groups&response_type=code&v=5.131

# 2. Обменяйте code на access_token
curl "https://oauth.vk.com/access_token?client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&redirect_uri=https://oauth.vk.com/blank.html&code=AUTHORIZATION_CODE"
```

#### Способ 2: Через токен сервиса (для групп)

1. Откройте настройки группы
2. Перейдите в "Управление" → "Работа с API"
3. Создайте ключ доступа
4. Выберите необходимые права:
   - Управление сообществом
   - Фотографии
   - Видеозаписи

### Настройка прав доступа

Необходимые права (scope):
- `wall` - публикация постов
- `photos` - загрузка фотографий
- `video` - загрузка видео
- `groups` - управление группами

### Получение ID группы

```bash
# Способ 1: Из URL
# https://vk.com/club123456 → group_id = -123456
# https://vk.com/public123456 → group_id = -123456

# Способ 2: Через API
curl "https://api.vk.com/method/groups.getById?group_id=your_screen_name&access_token=YOUR_TOKEN&v=5.131"
```

## Импорт workflow

### Через UI

1. Откройте n8n (http://localhost:5678)
2. Войдите с учетными данными
3. Нажмите "Workflows" в левом меню
4. Нажмите "Import from File"
5. Выберите файл `vk-content-workflow.json`
6. Нажмите "Import"

### Через API

```bash
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -u admin:password \
  --data-binary @vk-content-workflow.json
```

### Через CLI

```bash
n8n import:workflow --input=vk-content-workflow.json
```

## Настройка credentials

### VK OAuth2 API

1. В n8n перейдите в "Credentials" → "New"
2. Выберите "VK OAuth2 API"
3. Заполните поля:
   - **Name**: VK OAuth2 API
   - **Client ID**: ID вашего приложения
   - **Client Secret**: Защищенный ключ
   - **Access Token**: Токен доступа
4. Нажмите "Save"

### PostgreSQL

1. В n8n перейдите в "Credentials" → "New"
2. Выберите "Postgres"
3. Заполните поля:
   - **Name**: PostgreSQL
   - **Host**: localhost (или postgres для Docker)
   - **Database**: vk_content
   - **User**: postgres
   - **Password**: ваш пароль
   - **Port**: 5432
4. Нажмите "Test connection"
5. Нажмите "Save"

### OpenAI (опционально)

1. В n8n перейдите в "Credentials" → "New"
2. Выберите "OpenAI API"
3. Заполните поля:
   - **Name**: OpenAI API
   - **API Key**: ваш API ключ
4. Нажмите "Save"

## Тестирование

### Тест базового workflow

1. Откройте workflow "VK Content Creation Workflow"
2. Нажмите "Execute Workflow"
3. В узле "Webhook Trigger" скопируйте URL
4. Отправьте тестовый запрос:

```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Тестовый пост из n8n",
    "from_group": 1
  }'
```

5. Проверьте результат в VK

### Тест расширенного workflow

```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "-123456789",
    "message": "Расширенный тестовый пост",
    "hashtags": ["тест", "n8n", "автоматизация"],
    "from_group": 1,
    "close_comments": 0
  }'
```

### Проверка базы данных

```sql
-- Проверка опубликованных постов
SELECT * FROM vk_posts ORDER BY created_at DESC LIMIT 10;

-- Проверка ошибок
SELECT * FROM vk_posts_errors WHERE resolved = false;

-- Статистика
SELECT * FROM vk_posts_stats_30d;
```

## Production Deployment

### Требования для production

- HTTPS (SSL/TLS сертификаты)
- Reverse proxy (Nginx/Traefik)
- Мониторинг и логирование
- Резервное копирование
- Rate limiting
- Firewall настройки

### Настройка Nginx

Создайте файл `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream n8n {
        server n8n:5678;
    }

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        client_max_body_size 50M;

        location / {
            proxy_pass http://n8n;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### Получение SSL сертификата (Let's Encrypt)

```bash
# Установка certbot
sudo apt-get update
sudo apt-get install certbot

# Получение сертификата
sudo certbot certonly --standalone -d your-domain.com

# Копирование сертификатов
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Автоматическое обновление
sudo crontab -e
# Добавьте: 0 0 * * * certbot renew --quiet
```

### Настройка firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### Оптимизация производительности

```bash
# В .env файле
EXECUTIONS_PROCESS=main
EXECUTIONS_MODE=queue  # Для высоконагруженных систем
QUEUE_BULL_REDIS_HOST=redis
```

## Мониторинг

### Healthcheck endpoints

```bash
# n8n healthcheck
curl http://localhost:5678/healthz

# PostgreSQL healthcheck
docker-compose exec postgres pg_isready

# Redis healthcheck
docker-compose exec redis redis-cli ping
```

### Логирование

```bash
# Docker logs
docker-compose logs -f n8n

# Логи в файл
docker-compose logs n8n > logs/n8n.log

# Ротация логов
docker-compose logs --tail=1000 n8n
```

### Prometheus + Grafana (опционально)

Добавьте в `docker-compose.yml`:

```yaml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Резервное копирование

### Автоматическое резервное копирование

Создайте скрипт `scripts/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vk_content_$DATE.sql"

# Создание резервной копии
pg_dump -h postgres -U $PGUSER -d $PGDATABASE > $BACKUP_FILE

# Сжатие
gzip $BACKUP_FILE

# Удаление старых копий (старше 30 дней)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

### Запуск резервного копирования

```bash
# Вручную
docker-compose run --rm backup

# По расписанию (cron)
0 2 * * * cd /path/to/project && docker-compose run --rm backup
```

### Восстановление из резервной копии

```bash
# Распаковка
gunzip backups/vk_content_20260207_020000.sql.gz

# Восстановление
docker-compose exec -T postgres psql -U postgres -d vk_content < backups/vk_content_20260207_020000.sql
```

## Обновление

### Обновление n8n

```bash
# Остановка сервисов
docker-compose down

# Обновление образов
docker-compose pull n8n

# Запуск с новой версией
docker-compose up -d

# Проверка версии
docker-compose exec n8n n8n --version
```

### Обновление workflow

1. Экспортируйте текущий workflow (резервная копия)
2. Импортируйте новую версию
3. Проверьте настройки и credentials
4. Протестируйте workflow

## Troubleshooting

### n8n не запускается

```bash
# Проверка логов
docker-compose logs n8n

# Проверка портов
netstat -tulpn | grep 5678

# Проверка прав доступа
ls -la volumes/n8n_data
```

### Ошибки подключения к БД

```bash
# Проверка статуса PostgreSQL
docker-compose exec postgres pg_isready

# Проверка подключения
docker-compose exec postgres psql -U postgres -d vk_content -c "SELECT 1"

# Проверка переменных окружения
docker-compose exec n8n env | grep DB_
```

### Проблемы с VK API

```bash
# Проверка токена
curl "https://api.vk.com/method/users.get?access_token=YOUR_TOKEN&v=5.131"

# Проверка прав доступа
curl "https://api.vk.com/method/account.getAppPermissions?access_token=YOUR_TOKEN&v=5.131"
```

## Поддержка

Если у вас возникли проблемы:

1. Проверьте логи: `docker-compose logs -f`
2. Изучите документацию: [n8n docs](https://docs.n8n.io/)
3. Проверьте [VK API docs](https://dev.vk.com/reference)
4. Создайте issue в репозитории

---

**Успешного развертывания!**
