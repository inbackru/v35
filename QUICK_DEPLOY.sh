#!/bin/bash
# InBack Platform Quick Deploy Script
# Автоматическое развертывание на Ubuntu/Debian

set -e

echo "🚀 InBack Platform Quick Deploy Script"
echo "======================================"

# Проверка прав
if [[ $EUID -eq 0 ]]; then
   echo "❌ Не запускайте скрипт от root! Используйте sudo только когда нужно."
   exit 1
fi

# Создаем рабочую директорию
PROJECT_DIR="inback-platform"
echo "📁 Создаем директорию проекта: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Установка системных зависимостей
echo "📦 Установка системных зависимостей..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl

# Создание виртуального окружения
echo "🐍 Создание Python виртуального окружения..."
python3 -m venv venv
source venv/bin/activate

# Установка Python пакетов
echo "📦 Установка Python зависимостей..."
pip install --upgrade pip
pip install email-validator flask flask-dance flask-login flask-sqlalchemy
pip install gunicorn numpy oauthlib openai openpyxl pandas psycopg2-binary
pip install pyjwt python-telegram-bot requests sendgrid sqlalchemy werkzeug

# Создание базы данных
echo "🗄️  Настройка PostgreSQL..."
DB_NAME="inback_production"
DB_USER="inback_user"
DB_PASSWORD=$(openssl rand -hex 16)

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# Создание .env файла
echo "⚙️  Создание файла конфигурации..."
cat > .env << EOF
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME
SECRET_KEY=$(openssl rand -hex 32)
SESSION_SECRET=$(openssl rand -hex 32)
FLASK_ENV=production
TELEGRAM_BOT_TOKEN=7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE
TELEGRAM_CHAT_ID=730764738
EOF

echo "✅ Базовая настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Распакуйте архив inback_complete_backup.tar.gz в эту директорию"
echo "2. Восстановите базу данных: psql -d $DB_NAME -f database_export.sql"
echo "3. Запустите приложение: source venv/bin/activate && python3 app.py"
echo ""
echo "🔐 Созданные учетные данные:"
echo "База данных: $DB_NAME"
echo "Пользователь: $DB_USER"
echo "Пароль: $DB_PASSWORD"
echo ""
echo "💾 Файл .env создан с необходимыми переменными"
echo "✨ Готово к развертыванию!"