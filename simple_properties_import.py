"""
Простой импорт квартир - только существующие поля
"""
import pandas as pd
import os
import sys
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db

def safe_value(value):
    if pd.isna(value) or value == '':
        return None
    return str(value).strip()

def safe_int(value):
    if pd.isna(value) or value == '':
        return None
    try:
        return int(float(value))
    except:
        return None

def import_properties_simple():
    """Импорт квартир в существующие поля"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    
    try:
        df = pd.read_excel(file_path)
        print(f"Excel файл: {len(df)} квартир")
        
        # Очищаем и импортируем по простой схеме
        db.session.execute(text("DELETE FROM excel_properties"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                # Используем только базовые поля которые точно есть
                inner_id = safe_int(row.get('inner_id'))
                if not inner_id:
                    continue
                    
                data = {
                    'inner_id': inner_id,
                    'url': safe_value(row.get('url')),
                    'address_display_name': safe_value(row.get('address_display_name')),
                    'complex_name': safe_value(row.get('complex_name')),
                    'price': safe_int(row.get('price'))
                }
                
                # Убираем None значения
                clean_data = {k: v for k, v in data.items() if v is not None}
                
                if clean_data:
                    columns = ', '.join(clean_data.keys())
                    placeholders = ', '.join([f':{k}' for k in clean_data.keys()])
                    
                    sql = f"INSERT INTO excel_properties ({columns}) VALUES ({placeholders})"
                    db.session.execute(text(sql), clean_data)
                    imported += 1
                    
                    if imported % 50 == 0:
                        print(f"Импортировано {imported}...")
                        
            except Exception as e:
                print(f"Ошибка {idx}: {e}")
                continue
                
        db.session.commit()
        print(f"ИТОГО: {imported} квартир")
        return imported
        
    except Exception as e:
        print(f"Ошибка: {e}")
        db.session.rollback()
        return 0

with app.app_context():
    import_properties_simple()
    
    # Проверяем результат
    result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties"))
    count = result.scalar()
    print(f"В базе: {count} квартир")