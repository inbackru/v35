"""
Excel Database Import - заполнение базы данных из Excel файлов
Импортирует все данные из загруженных Excel файлов в соответствии с реальной структурой БД
"""
import pandas as pd
import os
import sys
from sqlalchemy import text
from datetime import datetime
import json

# Добавляем путь для импорта модулей приложения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def safe_value(value, default=None):
    """Безопасное получение значения"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    return value

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
    return value_str in ['true', '1', 'да', 'yes', 'истина']

def import_excel_properties():
    """Импорт данных недвижимости"""
    file_path = 'attached_assets/excel_properties_1756658357106.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт объектов недвижимости из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} объектов недвижимости")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                # Подготавливаем данные для вставки (только основные поля)
                data = {
                    'inner_id': safe_int(row.get('inner_id')),
                    'url': safe_value(row.get('url')),
                    'photos': safe_value(row.get('photos')),
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'price': safe_int(row.get('price')),
                    'rooms_count': safe_int(row.get('rooms_count')),
                    'area': safe_float(row.get('area')),
                    'floor': safe_int(row.get('floor')),
                    'floors_count': safe_int(row.get('floors_count'))
                }
                
                # Фильтруем None значения
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data:
                    columns = list(clean_data.keys())
                    placeholders = [f":{k}" for k in columns]
                    
                    sql = f"""INSERT INTO excel_properties ({', '.join(columns)}) 
                             VALUES ({', '.join(placeholders)})"""
                    
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
            except Exception as e:
                print(f"Ошибка импорта строки {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} объектов недвижимости")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0

def import_managers():
    """Импорт менеджеров"""
    file_path = 'attached_assets/managers (6)_1756658357103.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт менеджеров из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} менеджеров")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                data = {
                    'first_name': safe_value(row.get('first_name')),
                    'last_name': safe_value(row.get('last_name')),
                    'email': safe_value(row.get('email')),
                    'phone': safe_value(row.get('phone')),
                    'is_active': safe_bool(row.get('is_active'), True)
                }
                
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data:
                    columns = list(clean_data.keys())
                    placeholders = [f":{k}" for k in columns]
                    
                    sql = f"""INSERT INTO managers ({', '.join(columns)}) 
                             VALUES ({', '.join(placeholders)})"""
                    
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
            except Exception as e:
                print(f"Ошибка импорта менеджера {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} менеджеров")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0

def import_buildings():
    """Импорт зданий"""
    file_path = 'attached_assets/buildings (1)_1756658357103.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт зданий из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} зданий")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                data = {
                    'name': safe_value(row.get('name')),
                    'address': safe_value(row.get('address')),
                    'floors_count': safe_int(row.get('floors_count')),
                    'apartments_count': safe_int(row.get('apartments_count'))
                }
                
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data:
                    columns = list(clean_data.keys())
                    placeholders = [f":{k}" for k in columns]
                    
                    sql = f"""INSERT INTO buildings ({', '.join(columns)}) 
                             VALUES ({', '.join(placeholders)})"""
                    
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
            except Exception as e:
                print(f"Ошибка импорта здания {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} зданий")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0

def import_cities():
    """Импорт городов"""
    file_path = 'attached_assets/cities (1)_1756658357104.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт городов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} городов")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                data = {
                    'name': safe_value(row.get('name')),
                    'region_id': safe_int(row.get('region_id'))
                }
                
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data and clean_data.get('name'):
                    columns = list(clean_data.keys())
                    placeholders = [f":{k}" for k in columns]
                    
                    sql = f"""INSERT INTO cities ({', '.join(columns)}) 
                             VALUES ({', '.join(placeholders)})"""
                    
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта города {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} городов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0

def import_regions():
    """Импорт регионов"""
    file_path = 'attached_assets/regions_1756658357105.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт регионов из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} регионов")
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                data = {
                    'name': safe_value(row.get('name')),
                    'code': safe_value(row.get('code'))
                }
                
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data and clean_data.get('name'):
                    columns = list(clean_data.keys())
                    placeholders = [f":{k}" for k in columns]
                    
                    sql = f"""INSERT INTO regions ({', '.join(columns)}) 
                             VALUES ({', '.join(placeholders)})"""
                    
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e):
                    print(f"Ошибка импорта региона {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"Импортировано {imported} регионов")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return 0

def main_import():
    """Основная функция импорта"""
    print("=== ИМПОРТ ДАННЫХ ИЗ EXCEL ФАЙЛОВ ===")
    print()
    
    with app.app_context():
        total_imported = 0
        
        # Импортируем данные в правильном порядке (с учетом зависимостей)
        total_imported += import_regions()
        total_imported += import_cities()  
        total_imported += import_buildings()
        total_imported += import_managers()
        total_imported += import_excel_properties()
        
        print(f"\n=== ИТОГО ИМПОРТИРОВАНО: {total_imported} записей ===")
        
        # Показываем финальную статистику
        print("\n=== СТАТИСТИКА БАЗЫ ДАННЫХ ===")
        
        tables = [
            'users', 'districts', 'developers', 'residential_complexes',
            'excel_properties', 'managers', 'buildings', 'cities', 'regions'
        ]
        
        for table in tables:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"{table}: {count}")
            except Exception as e:
                print(f"{table}: Ошибка - {e}")

if __name__ == '__main__':
    main_import()