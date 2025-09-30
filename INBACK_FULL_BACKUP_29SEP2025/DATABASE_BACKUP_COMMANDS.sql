-- INBACK.RU DATABASE BACKUP COMMANDS
-- Дата создания: 29 сентября 2025

-- ===== ПРОВЕРКА ЦЕЛОСТНОСТИ БАЗЫ ДАННЫХ =====

-- 1. Проверка всех таблиц
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
ORDER BY table_name, ordinal_position;

-- 2. Количество записей в каждой таблице  
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY tablename, attname;

-- 3. Проверка основных данных
SELECT 'districts' as table_name, COUNT(*) as count FROM districts
UNION ALL
SELECT 'streets' as table_name, COUNT(*) as count FROM streets  
UNION ALL
SELECT 'residential_complexes' as table_name, COUNT(*) as count FROM residential_complexes
UNION ALL
SELECT 'excel_properties' as table_name, COUNT(*) as count FROM excel_properties
UNION ALL
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'managers' as table_name, COUNT(*) as count FROM managers
UNION ALL
SELECT 'deals' as table_name, COUNT(*) as count FROM deals;

-- ===== РЕЗЕРВНОЕ КОПИРОВАНИЕ КРИТИЧЕСКИХ ДАННЫХ =====

-- 4. Экспорт ЖК с настройками кешбека
SELECT 
    id, 
    name, 
    complex_id,
    cashback_rate,
    apartments_count,
    price_from,
    price_to,
    created_at
FROM residential_complexes 
ORDER BY id;

-- 5. Экспорт районов с координатами
SELECT 
    id,
    name, 
    slug,
    center_lat,
    center_lon,
    zoom_level,
    created_at
FROM districts 
ORDER BY name;

-- 6. Экспорт менеджеров (без паролей)
SELECT 
    id,
    username,
    email,
    full_name,
    phone,
    is_active,
    created_at
FROM managers 
ORDER BY id;

-- 7. Экспорт пользователей (без паролей)  
SELECT 
    id,
    username,
    email,
    created_at
FROM users 
ORDER BY id;

-- ===== ВОССТАНОВЛЕНИЕ ДАННЫХ =====

-- 8. Исправление дублированных ЖК (если нужно)
-- ВНИМАНИЕ: Запускать только при проблемах с дублированием

-- Показать дублированные complex_id
SELECT 
    complex_id, 
    COUNT(*) as count,
    STRING_AGG(name, ', ') as names
FROM residential_complexes 
WHERE complex_id IS NOT NULL 
GROUP BY complex_id 
HAVING COUNT(*) > 1;

-- Удаление дубликатов (ОСТОРОЖНО!)
/*
DELETE FROM residential_complexes 
WHERE id NOT IN (
    SELECT MIN(id) 
    FROM residential_complexes 
    GROUP BY complex_id
);
*/

-- ===== НАСТРОЙКА ПОСЛЕ ВОССТАНОВЛЕНИЯ =====

-- 9. Проверка настроек кешбека
SELECT 
    name,
    cashback_rate,
    CASE 
        WHEN cashback_rate IS NULL THEN '❌ Не настроено'
        WHEN cashback_rate = 5.0 THEN '✅ Стандартный (5%)'
        ELSE '🎯 Индивидуальный (' || cashback_rate || '%)'
    END as status
FROM residential_complexes 
ORDER BY cashback_rate DESC NULLS LAST;

-- 10. Обновление стандартного кешбека для новых ЖК
UPDATE residential_complexes 
SET cashback_rate = 5.0 
WHERE cashback_rate IS NULL;

-- ===== МОНИТОРИНГ ПРОИЗВОДИТЕЛЬНОСТИ =====

-- 11. Размер таблиц
SELECT 
    schemaname as schema,
    tablename as table,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 12. Индексы
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- ===== КОМАНДЫ ДЛЯ ЭКСТРЕННОГО ВОССТАНОВЛЕНИЯ =====

-- 13. Пересоздание таблиц (если критическая ошибка)
/*
-- ВНИМАНИЕ: Это удалит ВСЕ данные!
DROP TABLE IF EXISTS deals CASCADE;
DROP TABLE IF EXISTS manager_favorite_complexes CASCADE;
DROP TABLE IF EXISTS manager_favorite_properties CASCADE;
DROP TABLE IF EXISTS user_favorite_properties CASCADE;
DROP TABLE IF EXISTS user_favorite_complexes CASCADE;
DROP TABLE IF EXISTS managers CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS streets CASCADE;
DROP TABLE IF EXISTS districts CASCADE;
DROP TABLE IF EXISTS excel_properties CASCADE;
DROP TABLE IF EXISTS residential_complexes CASCADE;

-- После этого перезапустите приложение - таблицы создадутся автоматически
*/

-- ===== ПРОВЕРКА ГОТОВНОСТИ СИСТЕМЫ =====

-- 14. Финальная проверка всех компонентов
SELECT 
    'СИСТЕМА ГОТОВА' as status,
    'districts: ' || (SELECT COUNT(*) FROM districts) as districts,
    'complexes: ' || (SELECT COUNT(*) FROM residential_complexes) as complexes,
    'properties: ' || (SELECT COUNT(*) FROM excel_properties) as properties,
    'users: ' || (SELECT COUNT(*) FROM users) as users,
    'managers: ' || (SELECT COUNT(*) FROM managers) as managers;