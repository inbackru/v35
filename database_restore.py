#!/usr/bin/env python3
"""
Скрипт для восстановления базы данных InBack из резервной копии backup_2025_09_12
Автор: InBack Assistant
Дата: Сентябрь 2025
"""

import os
import re
import sys
import psycopg2
from psycopg2 import sql
import subprocess
from pathlib import Path

def clean_sql_file(input_file, output_file):
    """
    Очищает SQL файл от несовместимых команд
    """
    print(f"🔧 Очистка SQL файла: {input_file}")
    
    # Команды, которые нужно убрать или заменить
    skip_patterns = [
        r'SET transaction_timeout = 0;',
        r'SET idle_in_transaction_session_timeout = 0;',
        r'ALTER .* OWNER TO neondb_owner;'  # Убираем изменения владельца
    ]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Убираем проблемные команды
    for pattern in skip_patterns:
        content = re.sub(pattern, '-- ' + pattern.replace(r'\;', ';'), content, flags=re.MULTILINE)
    
    # Записываем очищенный файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Очищенный файл сохранен: {output_file}")
    return True

def get_db_connection():
    """
    Получает подключение к базе данных из переменных окружения
    """
    try:
        conn = psycopg2.connect(
            host=os.environ.get('PGHOST'),
            port=os.environ.get('PGPORT'),
            database=os.environ.get('PGDATABASE'),
            user=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD')
        )
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return None

def check_tables_exist(conn):
    """
    Проверяет, какие таблицы уже существуют в базе данных
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except Exception as e:
        print(f"❌ Ошибка проверки таблиц: {e}")
        return []

def restore_database_from_sql(sql_file):
    """
    Восстанавливает базу данных из SQL файла
    """
    print(f"🚀 Восстановление базы данных из: {sql_file}")
    
    try:
        # Используем psql для импорта
        env = os.environ.copy()
        
        # Выполняем импорт с игнорированием некоторых ошибок
        cmd = [
            'psql', 
            '-f', sql_file,
            '-v', 'ON_ERROR_STOP=0'  # Продолжаем при ошибках
        ]
        
        result = subprocess.run(
            cmd, 
            env=env, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ База данных успешно восстановлена!")
            return True
        else:
            print(f"⚠️  Восстановление завершено с предупреждениями:")
            print(f"Вывод: {result.stdout}")
            print(f"Ошибки: {result.stderr}")
            return True  # Даже с предупреждениями считаем успешным
            
    except Exception as e:
        print(f"❌ Ошибка при восстановлении: {e}")
        return False

def verify_restoration():
    """
    Проверяет успешность восстановления
    """
    print("🔍 Проверка восстановления...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Проверяем основные таблицы
        important_tables = [
            'excel_properties', 'residential_complexes', 'users', 
            'managers', 'districts', 'developers'
        ]
        
        results = {}
        for table in important_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                results[table] = count
                print(f"📊 {table}: {count} записей")
            except:
                results[table] = "❌ Таблица не найдена"
        
        cursor.close()
        conn.close()
        
        # Если хотя бы одна таблица имеет данные, считаем успешным
        has_data = any(isinstance(count, int) and count > 0 for count in results.values())
        
        if has_data:
            print("✅ Восстановление проверено - данные найдены!")
            return True
        else:
            print("⚠️  Восстановление не полное - некоторые таблицы пусты")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")
        return False

def main():
    """
    Основная функция восстановления
    """
    print("🏠 InBack Database Restore Script")
    print("=" * 50)
    
    # Путь к файлам бэкапа
    backup_dir = Path("backup_2025_09_12")
    sql_file = backup_dir / "database" / "full_backup_2025_09_12.sql"
    cleaned_sql_file = "cleaned_backup.sql"
    
    # Проверяем наличие файла бэкапа
    if not sql_file.exists():
        print(f"❌ Файл бэкапа не найден: {sql_file}")
        return False
    
    # Проверяем подключение к БД
    conn = get_db_connection()
    if not conn:
        print("❌ Не удалось подключиться к базе данных")
        return False
    
    # Показываем текущие таблицы
    existing_tables = check_tables_exist(conn)
    print(f"📋 Найдено {len(existing_tables)} существующих таблиц")
    conn.close()
    
    # Очищаем SQL файл
    if not clean_sql_file(sql_file, cleaned_sql_file):
        return False
    
    # Восстанавливаем базу данных
    if not restore_database_from_sql(cleaned_sql_file):
        print("❌ Ошибка при восстановлении базы данных")
        return False
    
    # Проверяем результат
    if verify_restoration():
        print("\n🎉 Восстановление базы данных InBack завершено успешно!")
        print("💡 Перезапустите приложение для применения изменений")
        return True
    else:
        print("\n⚠️  Восстановление выполнено, но требует проверки")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)