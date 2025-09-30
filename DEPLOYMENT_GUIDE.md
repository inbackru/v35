# 🚀 Инструкция по переносу и запуску сайта InBack

## 📋 Обзор проекта

**InBack** - это платформа недвижимости с кэшбек-сервисом, построенная на Flask с базой данных PostgreSQL. Сайт специализируется на новостройках в Краснодаре с интерактивными картами, поиском и системой кэшбека.

## 🎯 Требования к системе

### Минимальные требования сервера:
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM**: 2GB (рекомендуется 4GB+)
- **CPU**: 2 ядра (рекомендуется 4+)
- **Диск**: 20GB свободного места
- **Python**: 3.8+
- **PostgreSQL**: 12+

### Необходимые сервисы:
- Nginx (веб-сервер)
- PostgreSQL (база данных)
- Gunicorn (WSGI сервер)
- Supervisor (управление процессами)

## 📦 Шаг 1. Подготовка сервера

### 1.1 Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Установка зависимостей
```bash
# Основные пакеты
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx supervisor git

# Инструменты разработки
sudo apt install -y build-essential libpq-dev python3-dev
```

### 1.3 Создание пользователя для приложения
```bash
sudo adduser inback
sudo usermod -aG sudo inback
```

## 🗄️ Шаг 2. Настройка PostgreSQL

### 2.1 Создание базы данных и пользователя
```bash
sudo -u postgres psql

-- В PostgreSQL консоли:
CREATE DATABASE inback_db;
CREATE USER inback_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE inback_db TO inback_user;
ALTER USER inback_user CREATEDB;
\q
```

### 2.2 Настройка подключения
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```
Добавить строку:
```
local   inback_db    inback_user                     md5
```

Перезапустить PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## 📁 Шаг 3. Перенос файлов проекта

### 3.1 Создание директории проекта
```bash
sudo mkdir -p /var/www/inback
sudo chown inback:inback /var/www/inback
cd /var/www/inback
```

### 3.2 Список файлов для переноса

**Критически важные файлы:**
- `app.py` (499KB) - основное приложение Flask
- `models.py` (1759 строк) - модели базы данных
- `main.py` - точка входа
- `requirements.txt` - зависимости Python

**Директории для переноса:**
- `templates/` (67 HTML шаблонов)
- `static/` (CSS, JS, изображения)
- `attached_assets/` (Excel файлы с данными)

**Дополнительные файлы:**
- `.env` или переменные окружения
- `replit.md` (документация проекта)
- `SYSTEM_BACKUP_RESTORE_GUIDE.md`
- `DATABASE_BACKUP_COMMANDS.sql`

### 3.3 Команды для переноса
```bash
# Если перенос с Replit через архив:
wget [URL_архива] -O inback_project.zip
unzip inback_project.zip
rm inback_project.zip

# Или через git (если настроен):
git clone [repository_url] .
```

## 🐍 Шаг 4. Настройка Python окружения

### 4.1 Создание виртуального окружения
```bash
cd /var/www/inback
python3 -m venv venv
source venv/bin/activate
```

### 4.2 Установка зависимостей
```bash
pip install --upgrade pip

# Установка из requirements.txt или вручную:
pip install flask==3.0.0
pip install flask-sqlalchemy==3.1.1
pip install flask-login==0.6.3
pip install flask-dance==7.0.0
pip install gunicorn==21.2.0
pip install psycopg2-binary==2.9.9
pip install requests==2.31.0
pip install pandas==2.1.4
pip install openpyxl==3.1.2
pip install numpy==1.26.2
pip install sendgrid==6.11.0
pip install python-telegram-bot==20.7
pip install email-validator==2.1.0
pip install pyjwt==2.8.0
pip install werkzeug==3.0.1
pip install sqlalchemy==2.0.23
pip install oauthlib==3.2.2
pip install telegram==0.0.1
```

## 🔧 Шаг 5. Настройка переменных окружения

### 5.1 Создание файла .env
```bash
nano /var/www/inback/.env
```

### 5.2 Содержимое .env файла:
```env
# Database
DATABASE_URL=postgresql://inback_user:your_secure_password_here@localhost/inback_db
PGHOST=localhost
PGPORT=5432
PGDATABASE=inback_db
PGUSER=inback_user
PGPASSWORD=your_secure_password_here

# Flask
SESSION_SECRET=your_very_long_random_secret_key_here
FLASK_ENV=production
FLASK_DEBUG=False

# Optional: External APIs
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
SENDGRID_API_KEY=your_sendgrid_api_key
```

### 5.3 Защита файла окружения
```bash
chmod 600 /var/www/inback/.env
chown inback:inback /var/www/inback/.env
```

## 🗃️ Шаг 6. Импорт данных в базу

### 6.1 Создание структуры базы данных
```bash
cd /var/www/inback
source venv/bin/activate
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database tables created!')"
```

### 6.2 Импорт данных (если есть Excel файлы)
```bash
# Запуск Flask приложения для импорта данных через веб-интерфейс
# Или выполнение SQL скриптов:
psql -U inback_user -d inback_db -f DATABASE_BACKUP_COMMANDS.sql
```

## 🌐 Шаг 7. Настройка Gunicorn

### 7.1 Создание конфигурации Gunicorn
```bash
nano /var/www/inback/gunicorn.conf.py
```

```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "inback"
group = "inback"
tmp_upload_dir = None
errorlog = "/var/www/inback/logs/gunicorn_error.log"
accesslog = "/var/www/inback/logs/gunicorn_access.log"
loglevel = "info"
```

### 7.2 Создание директории для логов
```bash
mkdir -p /var/www/inback/logs
chown inback:inback /var/www/inback/logs
```

### 7.3 Тест запуска Gunicorn
```bash
cd /var/www/inback
source venv/bin/activate
gunicorn --config gunicorn.conf.py main:app
```

## 🔄 Шаг 8. Настройка Supervisor

### 8.1 Создание конфигурации Supervisor
```bash
sudo nano /etc/supervisor/conf.d/inback.conf
```

```ini
[program:inback]
command=/var/www/inback/venv/bin/gunicorn --config /var/www/inback/gunicorn.conf.py main:app
directory=/var/www/inback
user=inback
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/inback/logs/supervisor.log
environment=PATH="/var/www/inback/venv/bin"
```

### 8.2 Применение конфигурации
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start inback
sudo supervisorctl status
```

## 🌍 Шаг 9. Настройка Nginx

### 9.1 Создание конфигурации сайта
```bash
sudo nano /etc/nginx/sites-available/inback
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    location /static/ {
        alias /var/www/inback/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /attached_assets/ {
        alias /var/www/inback/attached_assets/;
        expires 1d;
    }
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### 9.2 Активация сайта
```bash
sudo ln -s /etc/nginx/sites-available/inback /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Шаг 10. SSL сертификат (рекомендуется)

### 10.1 Установка Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### 10.2 Получение SSL сертификата
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🚀 Шаг 11. Запуск и проверка

### 11.1 Проверка всех сервисов
```bash
# PostgreSQL
sudo systemctl status postgresql

# Supervisor
sudo supervisorctl status inback

# Nginx
sudo systemctl status nginx

# Проверка портов
netstat -tlnp | grep :80
netstat -tlnp | grep :5000
```

### 11.2 Проверка логов
```bash
# Логи приложения
tail -f /var/www/inback/logs/gunicorn_error.log
tail -f /var/www/inback/logs/supervisor.log

# Логи Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### 11.3 Тестирование сайта
```bash
curl http://localhost
curl -I http://your-domain.com
```

## 🔧 Управление сайтом

### Перезапуск приложения:
```bash
sudo supervisorctl restart inback
```

### Перезапуск Nginx:
```bash
sudo systemctl restart nginx
```

### Просмотр логов в реальном времени:
```bash
sudo supervisorctl tail -f inback
```

### Обновление кода:
```bash
cd /var/www/inback
# Загрузка новых файлов
sudo supervisorctl restart inback
```

## ⚠️ Возможные проблемы и решения

### 1. Ошибка подключения к базе данных
```bash
# Проверить статус PostgreSQL
sudo systemctl status postgresql

# Проверить права пользователя
sudo -u postgres psql -c "\du"

# Проверить настройки в .env
cat /var/www/inback/.env
```

### 2. Ошибка импорта модулей Python
```bash
# Переустановить зависимости
cd /var/www/inback
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### 3. Ошибки прав доступа
```bash
# Исправить права на файлы проекта
sudo chown -R inback:inback /var/www/inback
sudo chmod -R 755 /var/www/inback
sudo chmod 600 /var/www/inback/.env
```

### 4. Высокая нагрузка
```bash
# Увеличить количество воркеров Gunicorn
nano /var/www/inback/gunicorn.conf.py
# workers = 8

sudo supervisorctl restart inback
```

## 📊 Мониторинг

### Установка htop для мониторинга:
```bash
sudo apt install htop
htop
```

### Мониторинг дискового пространства:
```bash
df -h
du -sh /var/www/inback/*
```

### Проверка использования памяти:
```bash
free -h
ps aux | grep gunicorn
```

## 📋 Контрольный список

- [ ] Сервер подготовлен и обновлен
- [ ] PostgreSQL установлен и настроен
- [ ] Файлы проекта перенесены
- [ ] Python окружение создано
- [ ] Зависимости установлены
- [ ] Переменные окружения настроены
- [ ] База данных создана и заполнена
- [ ] Gunicorn настроен и работает
- [ ] Supervisor настроен
- [ ] Nginx настроен и работает
- [ ] SSL сертификат установлен
- [ ] Сайт доступен и работает корректно
- [ ] Логи настроены и отслеживаются

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `/var/www/inback/logs/`
2. Убедитесь, что все сервисы запущены
3. Проверьте права доступа к файлам
4. Убедитесь в корректности переменных окружения

---

**📧 Контакты для технической поддержки:**
- Email: tech@inback.ru
- Телефон: +7 (800) 123-45-67

**🔗 Полезные ссылки:**
- [Документация Flask](https://flask.palletsprojects.com/)
- [Документация PostgreSQL](https://postgresql.org/docs/)
- [Документация Nginx](https://nginx.org/ru/docs/)

---
*Инструкция создана: {{ current_date }}*
*Версия: 1.0*