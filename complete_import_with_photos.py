"""
ПОЛНЫЙ импорт с фотографиями и всеми данными
"""
import pandas as pd
import os
import sys
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db

def safe_value(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    return str(value).strip()

def safe_int(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        return int(float(value))
    except:
        return None

def safe_float(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    try:
        return float(value)
    except:
        return None

def safe_bool(value):
    if pd.isna(value) or value == '' or str(value) == 'nan':
        return None
    if str(value).lower() in ['true', '1', 'yes', 'да']:
        return True
    elif str(value).lower() in ['false', '0', 'no', 'нет']:
        return False
    return None

def import_complete_properties():
    """Полный импорт ВСЕХ полей включая фотографии"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} квартир из Excel")
        
        # Очищаем полностью
        db.session.execute(text("TRUNCATE TABLE excel_properties RESTART IDENTITY CASCADE"))
        db.session.commit()
        print("Таблица очищена")
        
        imported = 0
        with_photos = 0
        
        for idx, row in df.iterrows():
            try:
                # Обязательный inner_id
                inner_id = safe_int(row.get('inner_id'))
                if not inner_id:
                    continue
                
                # Все основные поля
                data = {
                    'inner_id': inner_id,
                    'url': safe_value(row.get('url')),
                    'photos': safe_value(row.get('photos')),  # ВАЖНО: Фотографии!
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'address_short_display_name': safe_value(row.get('address_short_display_name')),
                    'complex_id': safe_int(row.get('complex_id')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'complex_phone': safe_value(row.get('complex_phone')),
                    'developer_id': safe_int(row.get('developer_id')),
                    'developer_name': safe_value(row.get('developer_name')),
                    'price': safe_int(row.get('price')),
                    'max_price': safe_int(row.get('max_price')),
                    'min_price': safe_int(row.get('min_price')),
                    'square_price': safe_int(row.get('square_price')),
                    'mortgage_price': safe_int(row.get('mortgage_price')),
                    'object_area': safe_float(row.get('object_area')),
                    'object_rooms': safe_int(row.get('object_rooms')),
                    'object_max_floor': safe_int(row.get('object_max_floor')),
                    'object_min_floor': safe_int(row.get('object_min_floor')),
                    'renovation_type': safe_value(row.get('renovation_type')),
                    'renovation_display_name': safe_value(row.get('renovation_display_name')),
                    'description': safe_value(row.get('description')),
                    'complex_object_class_display_name': safe_value(row.get('complex_object_class_display_name')),
                    'complex_end_build_year': safe_int(row.get('complex_end_build_year')),
                    'address_position_lat': safe_float(row.get('address_position_lat')),
                    'address_position_lon': safe_float(row.get('address_position_lon'))
                }
                
                # Убираем None и пустые значения
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data and 'inner_id' in clean_data:
                    # Подсчет фотографий
                    if 'photos' in clean_data and clean_data['photos']:
                        with_photos += 1
                    
                    columns = ', '.join(clean_data.keys())
                    placeholders = ', '.join([f':{k}' for k in clean_data.keys()])
                    
                    sql = f"INSERT INTO excel_properties ({columns}) VALUES ({placeholders})"
                    db.session.execute(text(sql), clean_data)
                    
                    # Коммитим каждую запись
                    db.session.commit()
                    imported += 1
                    
                    if imported % 50 == 0:
                        print(f"Импортировано {imported} квартир (с фото: {with_photos})...")
                        
            except Exception as e:
                db.session.rollback()
                if imported < 10:  # Показываем только первые ошибки
                    print(f"Ошибка на записи {idx}: {e}")
                continue
                
        print(f"\nПОЛНЫЙ ИМПОРТ ЗАВЕРШЕН:")
        print(f"Успешно: {imported} квартир")
        print(f"С фотографиями: {with_photos} квартир")
        
        # Проверка результата
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties"))
        total = result.scalar()
        
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties WHERE photos IS NOT NULL"))
        photos_count = result.scalar()
        
        print(f"В базе итого: {total} квартир")
        print(f"С фотографиями в базе: {photos_count} квартир")
        
        # Примеры с фотографиями
        result = db.session.execute(text("""
            SELECT inner_id, complex_name, photos 
            FROM excel_properties 
            WHERE photos IS NOT NULL 
            LIMIT 3
        """))
        
        print("\nПримеры квартир с фотографиями:")
        for row in result:
            photos_preview = str(row[2])[:100] + "..." if row[2] else "Нет фото"
            print(f"ID: {row[0]}, ЖК: {row[1]}, Фото: {photos_preview}")
        
        return imported
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        db.session.rollback()
        return 0

# Запуск полного импорта
with app.app_context():
    import_complete_properties()