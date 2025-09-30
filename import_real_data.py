"""
Импорт ВСЕХ реальных данных из Excel файлов
Без искусственных данных - только то что в файлах
"""
import pandas as pd
import os
import sys
from sqlalchemy import text
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db

def safe_value(value, default=None):
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    return str(value).strip() if value is not None else default

def safe_int(value, default=None):
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def import_all_properties():
    """Импорт ВСЕХ квартир из Excel файла"""
    file_path = 'attached_assets/excel_properties_1756658927673.xlsx'
    print(f"Импорт всех квартир из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} квартир в Excel файле")
        
        # Удаляем искусственные данные и импортируем реальные
        db.session.execute(text("DELETE FROM excel_properties"))
        
        imported = 0
        batch_size = 100
        
        for idx, row in df.iterrows():
            try:
                # Берем только реальные данные из Excel
                data = {}
                
                # Основные поля - используем точные названия из Excel
                for col in df.columns:
                    value = row.get(col)
                    if col in ['inner_id', 'price'] and value is not None:
                        data[col] = safe_int(value)
                    elif col == 'photos' and value is not None:
                        # photos может быть списком или строкой
                        if isinstance(value, str):
                            data[col] = value
                        else:
                            data[col] = safe_value(value)
                    else:
                        data[col] = safe_value(value)
                
                # Создаем SQL запрос динамически на основе реальных данных
                if data:
                    columns = [k for k, v in data.items() if v is not None]
                    values_placeholders = [f":{k}" for k in columns]
                    
                    sql = f"INSERT INTO excel_properties ({', '.join(columns)}) VALUES ({', '.join(values_placeholders)})"
                    filtered_data = {k: v for k, v in data.items() if v is not None}
                    
                    db.session.execute(text(sql), filtered_data)
                    imported += 1
                    
                    # Показываем прогресс
                    if imported % batch_size == 0:
                        db.session.commit()
                        print(f"  Импортировано {imported} квартир...")
                        
            except Exception as e:
                if "duplicate key" not in str(e).lower():
                    print(f"Ошибка импорта квартиры {idx}: {e}")
                continue
        
        db.session.commit()
        print(f"ИТОГО импортировано {imported} реальных квартир из Excel")
        return imported
        
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        db.session.rollback()
        return 0

def import_all_residential_complexes():
    """Импорт всех ЖК из Excel"""
    file_path = 'attached_assets/residential_complexes (6)_1756658927674.xlsx'
    print(f"Импорт ЖК из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} ЖК в Excel файле")
        
        # Удаляем искусственные данные
        db.session.execute(text("DELETE FROM residential_complexes"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                data = {}
                for col in df.columns:
                    value = row.get(col)
                    if col in ['id', 'district_id', 'developer_id'] and value is not None:
                        data[col] = safe_int(value)
                    elif col == 'cashback_rate' and value is not None:
                        data[col] = float(value) if not pd.isna(value) else 3.0
                    else:
                        data[col] = safe_value(value)
                
                if data:
                    columns = [k for k, v in data.items() if v is not None]
                    values_placeholders = [f":{k}" for k in columns]
                    
                    sql = f"INSERT INTO residential_complexes ({', '.join(columns)}) VALUES ({', '.join(values_placeholders)})"
                    filtered_data = {k: v for k, v in data.items() if v is not None}
                    
                    db.session.execute(text(sql), filtered_data)
                    imported += 1
                    
            except Exception as e:
                if "duplicate key" not in str(e).lower():
                    print(f"Ошибка импорта ЖК {idx}: {e}")
                continue
        
        db.session.commit()
        print(f"Импортировано {imported} реальных ЖК")
        return imported
        
    except Exception as e:
        print(f"Ошибка чтения ЖК: {e}")
        return 0

def main():
    with app.app_context():
        print("=== ИМПОРТ ВСЕХ РЕАЛЬНЫХ ДАННЫХ ===")
        
        total = 0
        total += import_all_properties()
        total += import_all_residential_complexes()
        
        print(f"\n=== ИМПОРТ ЗАВЕРШЕН ===")
        print(f"Всего импортировано: {total} записей")
        
        # Итоговая статистика
        result = db.session.execute(text("SELECT COUNT(*) FROM excel_properties"))
        properties_count = result.scalar()
        
        result = db.session.execute(text("SELECT COUNT(*) FROM residential_complexes"))
        complexes_count = result.scalar()
        
        print(f"В базе данных:")
        print(f"  Квартиры: {properties_count}")
        print(f"  ЖК: {complexes_count}")

if __name__ == '__main__':
    main()