-- 🗄️ InBack.ru Database Restore Commands
-- Используйте эти команды для быстрого восстановления базы данных в новом Replit проекте

-- ===== СОЗДАНИЕ ТАБЛИЦ =====

-- Основные пользователи и менеджеры
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    full_name VARCHAR(255),
    phone VARCHAR(20),
    telegram_username VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS managers (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    full_name VARCHAR(255),
    phone VARCHAR(20),
    telegram_username VARCHAR(50),
    role VARCHAR(50) DEFAULT 'manager',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Таблицы недвижимости
CREATE TABLE IF NOT EXISTS excel_properties (
    id SERIAL PRIMARY KEY,
    property_id VARCHAR(50) UNIQUE,
    complex_name VARCHAR(255),
    complex_id INTEGER,
    district VARCHAR(100),
    street VARCHAR(255),
    house_number VARCHAR(20),
    rooms INTEGER,
    area DECIMAL(10, 2),
    floor INTEGER,
    max_floor INTEGER,
    price DECIMAL(15, 2),
    cashback_rate DECIMAL(5, 2),
    developer VARCHAR(255),
    status VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS residential_complexes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    developer VARCHAR(255),
    district VARCHAR(100),
    address TEXT,
    price_from DECIMAL(15, 2),
    price_to DECIMAL(15, 2),
    completion_date VARCHAR(100),
    status VARCHAR(100),
    description TEXT,
    infrastructure TEXT,
    transport TEXT,
    photos TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Избранное и сравнение
CREATE TABLE IF NOT EXISTS user_favorite_properties (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    property_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS manager_favorite_complexes (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER REFERENCES managers(id) ON DELETE CASCADE,
    complex_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заявки на кешбек
CREATE TABLE IF NOT EXISTS cashback_applications (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120),
    complex_id INTEGER,
    complex_name VARCHAR(255),
    property_price DECIMAL(15, 2),
    cashback_rate DECIMAL(5, 2),
    cashback_amount DECIMAL(15, 2),
    message TEXT,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    notes TEXT
);

-- Активность пользователей
CREATE TABLE IF NOT EXISTS user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(100) NOT NULL,
    description TEXT,
    property_id VARCHAR(50),
    complex_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== ВСТАВКА ТЕСТОВЫХ ДАННЫХ =====

-- Пользователи (пароль: demo123)
INSERT INTO users (username, email, password_hash, full_name, phone) VALUES
('user1', 'user1@example.com', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Иван Петров', '+7 (900) 123-45-01'),
('user2', 'user2@example.com', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Анна Сидорова', '+7 (900) 123-45-02'),
('user3', 'user3@example.com', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Алексей Козлов', '+7 (900) 123-45-03'),
('user4', 'user4@example.com', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Елена Новикова', '+7 (900) 123-45-04'),
('user5', 'user5@example.com', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Дмитрий Волков', '+7 (900) 123-45-05');

-- Менеджеры (пароль: demo123)
INSERT INTO managers (username, email, password_hash, full_name, phone, role) VALUES
('manager1', 'manager1@inback.ru', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Ольга Менеджер', '+7 (900) 555-01-01', 'senior_manager'),
('manager2', 'manager2@inback.ru', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Игорь Консультант', '+7 (900) 555-02-02', 'manager'),
('manager3', 'manager3@inback.ru', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Мария Эксперт', '+7 (900) 555-03-03', 'manager'),
('manager4', 'manager4@inback.ru', 'scrypt:32768:8:1$GbS2S6PbR5Qztr1p$8ad8ee2b1dd74b7e6e8aa9c0c8c7f0c9b5a2c8f1e7b3d4a5f6e8d9c2b1a3e4f5', 'Андрей Директор', '+7 (900) 555-04-04', 'director');

-- ===== КОМАНДЫ ДЛЯ ВОССТАНОВЛЕНИЯ =====

-- 1. Подключитесь к базе данных:
-- psql $DATABASE_URL

-- 2. Выполните команды выше для создания структуры

-- 3. Импортируйте данные из Excel файлов через app.py:
-- В Python консоли выполните:
-- from app import import_properties_from_excel, import_residential_complexes_from_excel
-- import_properties_from_excel()
-- import_residential_complexes_from_excel()

-- ===== ПРОВЕРКА ВОССТАНОВЛЕНИЯ =====

-- Проверить количество записей:
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'managers', COUNT(*) FROM managers
UNION ALL
SELECT 'excel_properties', COUNT(*) FROM excel_properties
UNION ALL
SELECT 'residential_complexes', COUNT(*) FROM residential_complexes
UNION ALL
SELECT 'cashback_applications', COUNT(*) FROM cashback_applications;

-- ===== ОЧИСТКА (если нужно) =====

-- DROP TABLE IF EXISTS user_activities CASCADE;
-- DROP TABLE IF EXISTS cashback_applications CASCADE;
-- DROP TABLE IF EXISTS manager_favorite_complexes CASCADE;
-- DROP TABLE IF EXISTS user_favorite_properties CASCADE;
-- DROP TABLE IF EXISTS residential_complexes CASCADE;
-- DROP TABLE IF EXISTS excel_properties CASCADE;
-- DROP TABLE IF EXISTS managers CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

-- Конец файла восстановления базы данных