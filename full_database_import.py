"""
Полный импорт всех данных из Excel файлов в базу данных
Импортирует ВСЕ таблицы с реальными данными
"""
import pandas as pd
import os
import sys
from sqlalchemy import text
from datetime import datetime
import json
import re

# Добавляем путь для импорта модулей приложения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def safe_value(value, default=None):
    """Безопасное получение значения"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    return str(value).strip() if value is not None else default

def safe_int(value, default=None):
    """Безопасное преобразование в int"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=None):
    """Безопасное преобразование в float"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_bool(value, default=False):
    """Безопасное преобразование в bool"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    if isinstance(value, bool):
        return value
    value_str = str(value).lower()
    return value_str in ['true', '1', 'да', 'yes', 'истина', 't']

def generate_slug(name):
    """Создание slug из названия"""
    if not name:
        return None
    # Транслитерация кириллицы
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-', '.': '', ',': '', '!': '', '?': '', '"': '', "'": '',
        '(': '', ')': '', '[': '', ']': '', '{': '', '}': ''
    }
    
    slug = name.lower()
    for char, replacement in translit_map.items():
        slug = slug.replace(char, replacement)
    
    # Удаляем все нелатинские символы и оставляем только буквы, цифры и дефисы
    slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug)  # Убираем множественные дефисы
    slug = slug.strip('-')  # Убираем дефисы в начале и конце
    
    return slug if slug else None

def import_regions():
    """Импорт регионов"""
    file_path = 'attached_assets/regions_1756658927672.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт регионов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} регионов")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM regions WHERE id > 0"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                region_name = safe_value(row.get('name') or row.get('region_name') or row.get('region'))
                if not region_name:
                    continue
                    
                data = {
                    'name': region_name,
                    'code': safe_value(row.get('code') or row.get('region_code'))
                }
                
                sql = "INSERT INTO regions (name, code) VALUES (:name, :code)"
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта региона {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} регионов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла регионов: {e}")
        return 0

def import_cities():
    """Импорт городов"""
    file_path = 'attached_assets/cities (1)_1756658927672.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт городов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} городов")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM cities WHERE id > 0"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                city_name = safe_value(row.get('name') or row.get('city_name') or row.get('city'))
                if not city_name:
                    continue
                    
                data = {
                    'name': city_name,
                    'region_id': safe_int(row.get('region_id'))
                }
                
                sql = "INSERT INTO cities (name, region_id) VALUES (:name, :region_id)"
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта города {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} городов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла городов: {e}")
        return 0

def import_districts():
    """Импорт районов с перезаписью существующих"""
    file_path = 'attached_assets/districts (5)_1756658927673.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт районов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} районов")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM districts WHERE id > 0"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                district_name = safe_value(row.get('name') or row.get('district_name') or row.get('district'))
                if not district_name:
                    continue
                    
                data = {
                    'name': district_name,
                    'slug': generate_slug(district_name)
                }
                
                sql = "INSERT INTO districts (name, slug) VALUES (:name, :slug)"
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта района {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} районов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла районов: {e}")
        return 0

def import_developers():
    """Импорт застройщиков"""
    file_path = 'attached_assets/developers (7)_1756658927673.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт застройщиков из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} застройщиков")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM developers WHERE id > 0"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                dev_name = safe_value(row.get('name') or row.get('developer_name') or row.get('developer'))
                if not dev_name:
                    continue
                    
                data = {
                    'name': dev_name,
                    'slug': generate_slug(dev_name),
                    'description': safe_value(row.get('description')),
                    'phone': safe_value(row.get('phone')),
                    'email': safe_value(row.get('email')),
                    'website': safe_value(row.get('website'))
                }
                
                sql = """INSERT INTO developers (name, slug, description, phone, email, website) 
                         VALUES (:name, :slug, :description, :phone, :email, :website)"""
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта застройщика {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} застройщиков")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла застройщиков: {e}")
        return 0

def import_users():
    """Импорт пользователей"""
    file_path = 'attached_assets/users (7)_1756658927674.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт пользователей из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} пользователей")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM users WHERE id > 3"))  # Оставляем первых 3
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                email = safe_value(row.get('email'))
                if not email or '@' not in email:
                    continue
                    
                # Генерируем user_id
                user_id = f"user_{idx+1000}"
                
                data = {
                    'email': email,
                    'phone': safe_value(row.get('phone')),
                    'full_name': safe_value(row.get('full_name') or row.get('name') or row.get('first_name')),
                    'user_id': user_id,
                    'is_active': safe_bool(row.get('is_active'), True)
                }
                
                sql = """INSERT INTO users (email, phone, full_name, user_id, is_active) 
                         VALUES (:email, :phone, :full_name, :user_id, :is_active)"""
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта пользователя {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} пользователей")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла пользователей: {e}")
        return 0

def import_residential_complexes():
    """Импорт жилых комплексов"""
    file_path = 'attached_assets/residential_complexes (6)_1756658927674.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт жилых комплексов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} жилых комплексов")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM residential_complexes WHERE id > 3"))  # Оставляем первые 3
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                complex_name = safe_value(row.get('name') or row.get('complex_name'))
                if not complex_name:
                    continue
                    
                data = {
                    'name': complex_name,
                    'slug': generate_slug(complex_name),
                    'cashback_rate': safe_float(row.get('cashback_rate'), 3.0),
                    'district_id': safe_int(row.get('district_id')),
                    'developer_id': safe_int(row.get('developer_id'))
                }
                
                sql = """INSERT INTO residential_complexes (name, slug, cashback_rate, district_id, developer_id) 
                         VALUES (:name, :slug, :cashback_rate, :district_id, :developer_id)"""
                db.session.execute(text(sql), data)
                imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта ЖК {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} жилых комплексов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла жилых комплексов: {e}")
        return 0

def import_excel_properties():
    """Импорт объектов недвижимости"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт объектов недвижимости из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} объектов недвижимости")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM excel_properties WHERE inner_id > 1005"))  # Оставляем первые 5
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                inner_id = safe_int(row.get('inner_id') or row.get('id'))
                if not inner_id:
                    inner_id = 2000 + idx  # Генерируем ID
                    
                data = {
                    'inner_id': inner_id,
                    'url': safe_value(row.get('url')),
                    'address_display_name': safe_value(row.get('address_display_name') or row.get('address')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'price': safe_int(row.get('price'))
                }
                
                sql = """INSERT INTO excel_properties (inner_id, url, address_display_name, complex_name, price) 
                         VALUES (:inner_id, :url, :address_display_name, :complex_name, :price)"""
                db.session.execute(text(sql), data)
                imported += 1
                
                if imported % 100 == 0:  # Показываем прогресс каждые 100 записей
                    print(f"  Импортировано {imported} объектов...")
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта объекта {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} объектов недвижимости")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла объектов недвижимости: {e}")
        return 0

def main_full_import():
    """Основная функция полного импорта"""
    print("=== ПОЛНЫЙ ИМПОРТ ВСЕХ ДАННЫХ ИЗ EXCEL ===")
    print()
    
    with app.app_context():
        total_imported = 0
        
        # Импортируем в правильном порядке (с учетом зависимостей)
        print("1. Импорт базовых справочников...")
        total_imported += import_regions()
        total_imported += import_cities()
        total_imported += import_districts()
        
        print("\n2. Импорт застройщиков...")
        total_imported += import_developers()
        
        print("\n3. Импорт жилых комплексов...")
        total_imported += import_residential_complexes()
        
        print("\n4. Импорт пользователей...")
        total_imported += import_users()
        
        print("\n5. Импорт объектов недвижимости...")
        total_imported += import_excel_properties()
        
        print(f"\n=== ПОЛНЫЙ ИМПОРТ ЗАВЕРШЕН ===")
        print(f"ИТОГО ИМПОРТИРОВАНО: {total_imported} записей")
        
        # Показываем финальную статистику
        print(f"\n=== ФИНАЛЬНАЯ СТАТИСТИКА БАЗЫ ДАННЫХ ===")
        
        tables = [
            'regions', 'cities', 'districts', 'developers', 
            'residential_complexes', 'users', 'excel_properties', 'managers'
        ]
        
        for table in tables:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"{table}: {count} записей")
            except Exception as e:
                print(f"{table}: Ошибка - {e}")

if __name__ == '__main__':
    main_full_import()