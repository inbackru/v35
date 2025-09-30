#!/usr/bin/env python3
"""
Простой скрипт импорта данных недвижимости из Excel файла
"""
import pandas as pd
import os
import sys
from sqlalchemy import text
from datetime import datetime

# Добавляем путь для импорта модулей приложения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def safe_value(value, default=None):
    """Безопасное получение значения"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    return str(value).strip()

def safe_int(value, default=None):
    """Безопасное преобразование в int"""
    if pd.isna(value) or value == '':
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=None):
    """Безопасное преобразование в float"""
    if pd.isna(value) or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def import_excel_properties():
    """Импорт данных недвижимости из Excel"""
    
    # Пробуем найти самый свежий файл
    excel_files = [
        'attached_assets/excel_properties_1756658927673.xlsx',
        'attached_assets/excel_properties_1756658357106.xlsx',
        'attached_assets/domclick_krasnodar_20250829_210722.xlsx'
    ]
    
    file_path = None
    for f in excel_files:
        if os.path.exists(f):
            file_path = f
            break
    
    if not file_path:
        print("❌ Не найден файл с данными недвижимости")
        return False
    
    print(f"📁 Импортируем данные из файла: {file_path}")
    
    # Загружаем данные
    try:
        df = pd.read_excel(file_path)
        print(f"📊 Найдено {len(df)} записей")
    except Exception as e:
        print(f"❌ Ошибка загрузки файла: {e}")
        return False
    
    # Очищаем таблицу перед импортом
    with app.app_context():
        try:
            db.session.execute(text("DELETE FROM excel_properties"))
            db.session.commit()
            print("🗑️ Очищена таблица excel_properties")
        except Exception as e:
            print(f"⚠️ Ошибка очистки: {e}")
            db.session.rollback()
    
        imported_count = 0
        error_count = 0
        
        print("🚀 Начинаем импорт...")
        
        for index, row in df.iterrows():
            try:
                # Подготавливаем данные для вставки
                insert_data = {
                    'inner_id': safe_int(row.get('inner_id')),
                    'url': safe_value(row.get('url')),
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'complex_id': safe_int(row.get('complex_id')),
                    'price': safe_int(row.get('price')),
                    'max_price': safe_int(row.get('max_price')),
                    'min_price': safe_int(row.get('min_price')),
                    'square_price': safe_int(row.get('square_price')),
                    'object_area': safe_float(row.get('object_area')),
                    'object_rooms': safe_int(row.get('object_rooms')),
                    'object_max_floor': safe_int(row.get('object_max_floor')),
                    'object_min_floor': safe_int(row.get('object_min_floor')),
                    'developer_name': safe_value(row.get('developer_name')),
                    'developer_id': safe_int(row.get('developer_id')),
                    'address_position_lat': safe_float(row.get('address_position_lat')),
                    'address_position_lon': safe_float(row.get('address_position_lon')),
                    'parsed_city': safe_value(row.get('parsed_city')),
                    'parsed_region': safe_value(row.get('parsed_region')),
                    'parsed_district': safe_value(row.get('parsed_district')),
                    'deal_type': safe_value(row.get('deal_type')),
                    'renovation_type': safe_value(row.get('renovation_type')),
                    'description': safe_value(row.get('description')),
                    'photos': safe_value(row.get('photos')),
                    'is_auction': bool(row.get('is_auction', False)),
                    'published_dt': safe_value(row.get('published_dt')),
                    'chat_available': bool(row.get('chat_available', False)),
                }
                
                # Убираем None значения 
                insert_data = {k: v for k, v in insert_data.items() if v is not None}
                
                if not insert_data.get('inner_id'):
                    print(f"⚠️ Пропускаем строку {index + 2}: нет inner_id")
                    continue
                
                # Вставляем запись
                columns = ', '.join(insert_data.keys())
                placeholders = ', '.join([f':{k}' for k in insert_data.keys()])
                
                sql = f"""
                INSERT INTO excel_properties ({columns}) 
                VALUES ({placeholders})
                ON CONFLICT (inner_id) DO NOTHING
                """
                
                db.session.execute(text(sql), insert_data)
                imported_count += 1
                
                if imported_count % 50 == 0:
                    print(f"✅ Импортировано {imported_count} записей...")
                    db.session.commit()
                
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Показываем только первые 5 ошибок
                    print(f"❌ Ошибка в строке {index + 2}: {e}")
                continue
        
        # Коммитим финальные данные
        try:
            db.session.commit()
            print(f"✅ Импорт завершен!")
            print(f"📊 Импортировано: {imported_count} записей")
            print(f"❌ Ошибок: {error_count}")
            
            # Проверяем результат
            result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties")).scalar()
            print(f"🏠 Всего записей в базе: {result}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка коммита: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    with app.app_context():
        success = import_excel_properties()
        if success:
            print("🎉 Импорт данных недвижимости завершен успешно!")
        else:
            print("💥 Импорт данных завершился с ошибками")