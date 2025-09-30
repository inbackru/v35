# InBack Real Estate Platform - Полная инструкция по установке

## 📋 Описание проекта
InBack - современная платформа недвижимости с системой кэшбека для покупки квартир в новостройках Краснодара. Включает административную панель, систему уведомлений Telegram/Email, поиск недвижимости, управление клиентами и блог-систему.

## 🛠️ Технологический стек
- **Backend**: Python 3.11 + Flask
- **База данных**: PostgreSQL
- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **ORM**: SQLAlchemy
- **Уведомления**: Telegram Bot API, SMTP Email
- **Развертывание**: Gunicorn + Replit/любой VPS

## 📦 Требования к системе
- Python 3.11+
- PostgreSQL 12+
- Node.js 18+ (для сборки фронтенда)
- Git

## 🚀 Пошаговая установка

### 1. Клонирование и подготовка

```bash
# Скачиваем все файлы проекта
git clone <your-repo-url> inback-platform
cd inback-platform

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей

```bash
# Python зависимости
pip install -r requirements.txt

# Если requirements.txt отсутствует, установите вручную:
pip install flask flask-sqlalchemy flask-login flask-dance
pip install gunicorn psycopg2-binary werkzeug sqlalchemy
pip install requests python-telegram-bot sendgrid email-validator
pip install pyjwt oauthlib pandas numpy openpyxl
```

### 3. Настройка базы данных PostgreSQL

```bash
# Создайте базу данных
createdb inback_production

# Восстановите данные из экспорта
psql -d inback_production -f database_export.sql

# Или создайте базу с нуля и импортируйте данные
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created!')
"
```

### 4. Переменные окружения

Создайте файл `.env`:

```env
# База данных
DATABASE_URL=postgresql://username:password@localhost:5432/inback_production

# Flask
SECRET_KEY=your-super-secret-key-here
SESSION_SECRET=your-session-secret-here
FLASK_ENV=production

# Telegram Bot
TELEGRAM_BOT_TOKEN=7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE
TELEGRAM_CHAT_ID=730764738

# Email (опционально)
SENDGRID_API_KEY=your-sendgrid-key
SMTP_SERVER=your-smtp-server
SMTP_PORT=587
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-password

# Домены
REPLIT_DOMAINS=your-domain.com,www.your-domain.com
```

### 5. Структура проекта

```
inback-platform/
├── app.py                 # Главное Flask приложение
├── main.py               # Entry point для Gunicorn
├── models.py             # Модели базы данных
├── requirements.txt      # Python зависимости
├── database_export.sql   # Экспорт базы данных
├── .env                  # Переменные окружения
├── data/                 # JSON файлы с данными
│   ├── streets.json
│   ├── properties.json
│   ├── developers.json
│   └── ...
├── templates/            # HTML шаблоны
│   ├── base.html
│   ├── index.html
│   ├── streets.html
│   └── ...
├── static/              # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
├── includes/            # PHP includes (для миграции)
└── scripts/             # Утилиты и скрипты
    ├── add_streets_g.py
    ├── add_streets_dezhi.py
    └── ...
```

### 6. Запуск приложения

#### Для разработки:
```bash
python3 app.py
# Или
flask run --host=0.0.0.0 --port=5000
```

#### Для продакшена:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

#### Systemd сервис (Linux):
```ini
# /etc/systemd/system/inback.service
[Unit]
Description=InBack Real Estate Platform
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/inback-platform
ExecStart=/path/to/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable inback
sudo systemctl start inback
```

### 7. Настройка Nginx (опционально)

```nginx
# /etc/nginx/sites-available/inback
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/inback-platform/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 👥 Пользователи и доступы

### Менеджеры:
- **admin@inback.ru** / demo123 (Администратор)
- **manager@inback.ru** / demo123 (Менеджер)

### Telegram Bot:
- **Token**: 7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE
- **Chat ID**: 730764738

## 📊 Данные и контент

### База данных включает:
- ✅ 214+ улиц (буквы Г, Д, Е, Ж, З, И)
- ✅ 195+ объектов недвижимости
- ✅ 50+ жилых комплексов
- ✅ 20+ застройщиков
- ✅ Полная блог-система с статьями
- ✅ Система пользователей и менеджеров
- ✅ Настройки уведомлений

### JSON файлы:
- `streets.json` - 1641 улица с координатами
- `properties.json` - недвижимость с фильтрами
- `developers.json` - застройщики
- `residential_complexes.json` - ЖК
- `blog_articles.json` - статьи блога

## 🔧 Администрирование

### Добавление улиц по буквам:
```bash
# Пример скриптов для массового добавления
python3 add_streets_g.py      # Буква Г
python3 add_streets_dezhi.py  # Буквы Д,Е,Ж,З,И
```

### Управление контентом:
- Админ-панель: `/manager/dashboard`
- Блог-система: `/manager/blog`
- Управление объектами: `/manager/properties`

### Резервное копирование:
```bash
# Экспорт базы данных
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Архив всего проекта
tar -czf inback_backup_$(date +%Y%m%d).tar.gz .
```

## 🚨 Важные моменты

1. **Безопасность**: Измените все пароли и ключи
2. **SSL**: Настройте HTTPS сертификат
3. **Backup**: Регулярное резервное копирование
4. **Мониторинг**: Логи приложения в `/var/log/`
5. **Updates**: Регулярные обновления зависимостей

## 📞 Поддержка

При вопросах по установке:
1. Проверьте логи: `tail -f /var/log/inback.log`
2. Проверьте статус: `systemctl status inback`
3. Проверьте соединение с БД: `psql $DATABASE_URL`

## 🎯 Готовые функции

✅ Поиск недвижимости с фильтрами
✅ Система кэшбека до 500 000₽
✅ Telegram/Email уведомления
✅ Административная панель
✅ Блог-система с TinyMCE
✅ Карты и геолокация
✅ SEO оптимизация
✅ Мобильная адаптация
✅ Система избранного
✅ Сравнение объектов

Платформа полностью готова к продакшену!