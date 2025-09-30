"""
Финальный надежный импорт квартир
С обработкой дубликатов и ошибок
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

def import_properties_final():
    """Финальный импорт всех квартир"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} квартир из Excel")
        
        # Полностью очищаем таблицу
        db.session.execute(text("TRUNCATE TABLE excel_properties RESTART IDENTITY CASCADE"))
        db.session.commit()
        print("Таблица очищена")
        
        imported = 0
        errors = 0
        
        for idx, row in df.iterrows():
            try:
                # Проверяем обязательный inner_id
                inner_id = safe_int(row.get('inner_id'))
                if not inner_id:
                    continue
                
                # Проверяем что такой inner_id еще не добавлен
                existing = db.session.execute(
                    text("SELECT 1 FROM excel_properties WHERE inner_id = :id LIMIT 1"), 
                    {"id": inner_id}
                ).fetchone()
                
                if existing:
                    continue  # Пропускаем дубликат
                
                # Подготавливаем данные
                data = {
                    'inner_id': inner_id,
                    'url': safe_value(row.get('url')),
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'price': safe_int(row.get('price')),
                    'complex_id': safe_int(row.get('complex_id')),
                    'developer_id': safe_int(row.get('developer_id')),
                    'developer_name': safe_value(row.get('developer_name')),
                    'object_area': safe_value(row.get('object_area')),
                    'object_rooms': safe_int(row.get('object_rooms')),
                    'object_max_floor': safe_int(row.get('object_max_floor')),
                    'object_min_floor': safe_int(row.get('object_min_floor'))
                }
                
                # Убираем None значения
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data and 'inner_id' in clean_data:
                    columns = ', '.join(clean_data.keys())
                    placeholders = ', '.join([f':{k}' for k in clean_data.keys()])
                    
                    sql = f"INSERT INTO excel_properties ({columns}) VALUES ({placeholders})"
                    db.session.execute(text(sql), clean_data)
                    
                    # Коммитим каждую запись отдельно для надежности  
                    db.session.commit()
                    imported += 1
                    
                    if imported % 50 == 0:
                        print(f"Импортировано {imported} квартир...")
                        
            except Exception as e:
                errors += 1
                db.session.rollback()
                if "duplicate key" not in str(e) and errors < 10:
                    print(f"Ошибка на записи {idx}: {e}")
                continue
                
        print(f"\nИМПОРТ ЗАВЕРШЕН:")
        print(f"Успешно: {imported} квартир")
        print(f"Ошибок: {errors}")
        
        # Финальная проверка
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties"))
        final_count = result.scalar()
        print(f"В базе итого: {final_count} квартир")
        
        # Показываем примеры
        result = db.session.execute(text("""
            SELECT inner_id, address_display_name, complex_name, price 
            FROM excel_properties 
            ORDER BY inner_id 
            LIMIT 5
        """))
        
        print("\nПримеры квартир:")
        for row in result:
            print(f"ID: {row[0]}, Адрес: {row[1][:50]}..., ЖК: {row[2]}, Цена: {row[3]:,} руб")
        
        return imported
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        db.session.rollback()
        return 0

# Запуск
with app.app_context():
    import_properties_final()