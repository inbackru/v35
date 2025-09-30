"""
Импорт IT-компаний для ипотечных программ
"""
import pandas as pd
import os
import sys
from sqlalchemy import text

# Добавляем путь для импорта модулей приложения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def safe_value(value, default=None):
    """Безопасное получение значения"""
    if pd.isna(value) or value == '' or str(value).strip() == '':
        return default
    return str(value).strip() if value is not None else default

def import_it_companies():
    """Импорт IT компаний"""
    file_path = 'attached_assets/it_companies (1)_1756658927673.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return 0
        
    print(f"Импорт IT компаний из {file_path}...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Найдено {len(df)} IT компаний")
        
        # Очищаем существующие данные
        db.session.execute(text("DELETE FROM it_companies WHERE id > 0"))
        
        imported = 0
        for idx, row in df.iterrows():
            try:
                company_name = safe_value(row.get('name') or row.get('company_name') or row.get('organization'))
                if not company_name:
                    continue
                    
                # Базовые данные компании
                data = {
                    'name': company_name,
                    'inn': safe_value(row.get('inn')),
                    'ogrn': safe_value(row.get('ogrn')),
                    'status': safe_value(row.get('status'), 'active'),
                    'region': safe_value(row.get('region') or row.get('region_name'), 'Краснодарский край')
                }
                
                sql = """INSERT INTO it_companies (name, inn, ogrn, status, region) 
                         VALUES (:name, :inn, :ogrn, :status, :region)"""
                db.session.execute(text(sql), data)
                imported += 1
                
                if imported % 500 == 0:  # Показываем прогресс каждые 500 записей
                    print(f"  Импортировано {imported} IT компаний...")
                    
            except Exception as e:
                if "duplicate key" not in str(e).lower() and "unique constraint" not in str(e).lower():
                    print(f"Ошибка импорта IT компании {idx}: {e}")
                continue
        
        db.session.commit()
        print(f"Импортировано {imported} IT компаний")
        return imported
        
    except Exception as e:
        print(f"Ошибка при чтении файла IT компаний: {e}")
        db.session.rollback()
        return 0

def main():
    with app.app_context():
        print("=== ИМПОРТ IT КОМПАНИЙ ===")
        total = import_it_companies()
        
        # Финальная статистика
        result = db.session.execute(text("SELECT COUNT(*) FROM it_companies"))
        count = result.scalar()
        print(f"ИТОГО в базе IT компаний: {count}")

if __name__ == '__main__':
    main()