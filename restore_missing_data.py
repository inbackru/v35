#!/usr/bin/env python3
"""
Восстановление сохраненных поисков и рекомендаций из XLSX файлов
"""

import pandas as pd
import os
from datetime import datetime
from app import app, db
from models import SavedSearch, Recommendation

def safe_convert_datetime(date_str):
    """Безопасное преобразование строки в datetime"""
    if pd.isna(date_str) or date_str is None or date_str == '':
        return datetime.utcnow()
    
    if isinstance(date_str, datetime):
        return date_str
    
    try:
        date_str = str(date_str)
        if 'GMT' in date_str:
            date_str = date_str.split(' GMT')[0]
        
        for fmt in ['%a %b %d %Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d.%m.%Y']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.utcnow()
    except:
        return datetime.utcnow()

def restore_saved_searches():
    """Восстанавливает сохраненные поиски"""
    print("Восстанавливаю сохраненные поиски...")
    
    file_path = 'attached_assets/saved_searches (2)_1755110853172.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} сохраненных поисков")
        
        imported_count = 0
        
        for index, row in df.iterrows():
            try:
                # Создаем фильтры JSON из данных XLSX
                filters_json = {
                    'search_type': str(row['search_type']) if not pd.isna(row['search_type']) else '',
                    'location': str(row['location']) if not pd.isna(row['location']) else '',
                    'property_type': str(row['property_type']) if not pd.isna(row['property_type']) else '',
                    'price_min': str(row['price_min']) if not pd.isna(row['price_min']) else '',
                    'price_max': str(row['price_max']) if not pd.isna(row['price_max']) else '',
                    'developer': str(row['developer']) if not pd.isna(row['developer']) else '',
                    'complex_name': str(row['complex_name']) if not pd.isna(row['complex_name']) else ''
                }
                
                search_data = {
                    'id': int(row['id']) if not pd.isna(row['id']) else None,
                    'user_id': int(row['user_id']) if not pd.isna(row['user_id']) else None,
                    'name': str(row['search_name']) if not pd.isna(row['search_name']) else str(row['name']) if not pd.isna(row['name']) else 'Поиск',
                    'filters': str(filters_json).replace("'", '"'),
                    'notification_enabled': bool(row['email_notifications']) if not pd.isna(row['email_notifications']) else bool(row['notify_new_matches']) if not pd.isna(row['notify_new_matches']) else False,
                    'notification_frequency': 'weekly',
                    'created_at': safe_convert_datetime(row['created_at']),
                    'updated_at': safe_convert_datetime(row['updated_at'])
                }
                
                # Проверяем, не существует ли уже такой поиск
                existing = SavedSearch.query.filter_by(id=search_data['id']).first() if search_data['id'] else None
                
                if not existing:
                    search = SavedSearch(**search_data)
                    db.session.add(search)
                    imported_count += 1
                    print(f"Восстановлен поиск: {search_data['name']} для пользователя {search_data['user_id']}")
                
            except Exception as e:
                print(f"Ошибка обработки строки {index}: {e}")
                continue
        
        db.session.commit()
        print(f"Восстановлено сохраненных поисков: {imported_count}")
        
    except Exception as e:
        print(f"Ошибка при восстановлении поисков: {e}")
        db.session.rollback()

def restore_recommendations():
    """Восстанавливает рекомендации"""
    print("Восстанавливаю рекомендации...")
    
    file_path = 'attached_assets/recommendations (2)_1755110853173.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} рекомендаций")
        
        imported_count = 0
        
        for index, row in df.iterrows():
            try:
                rec_data = {
                    'id': int(row['id']) if not pd.isna(row['id']) else None,
                    'user_id': int(row['client_id']) if not pd.isna(row['client_id']) else int(row['user_id']) if not pd.isna(row['user_id']) else None,
                    'manager_id': int(row['manager_id']) if not pd.isna(row['manager_id']) else int(row['created_by_manager_id']) if not pd.isna(row['created_by_manager_id']) else None,
                    'property_id': int(row['property_id']) if not pd.isna(row['property_id']) else int(row['item_id']) if not pd.isna(row['item_id']) else None,
                    'message': str(row['description']) if not pd.isna(row['description']) else str(row['recommendation_reason']) if not pd.isna(row['recommendation_reason']) else '',
                    'status': str(row['status']) if not pd.isna(row['status']) else 'pending',
                    'created_at': safe_convert_datetime(row['created_at']),
                    'updated_at': safe_convert_datetime(row['updated_at'])
                }
                
                # Проверяем, не существует ли уже такая рекомендация
                existing = Recommendation.query.filter_by(id=rec_data['id']).first() if rec_data['id'] else None
                
                if not existing:
                    recommendation = Recommendation(**rec_data)
                    db.session.add(recommendation)
                    imported_count += 1
                    print(f"Восстановлена рекомендация для пользователя {rec_data['user_id']} объект {rec_data['property_id']}")
                
            except Exception as e:
                print(f"Ошибка обработки рекомендации {index}: {e}")
                continue
        
        db.session.commit()
        print(f"Восстановлено рекомендаций: {imported_count}")
        
    except Exception as e:
        print(f"Ошибка при восстановлении рекомендаций: {e}")
        db.session.rollback()

def main():
    """Основная функция восстановления"""
    print("Начинаю восстановление данных...")
    
    with app.app_context():
        # Восстанавливаем данные
        restore_saved_searches()
        restore_recommendations()
        
        # Проверяем результаты
        searches_count = SavedSearch.query.count()
        recommendations_count = Recommendation.query.count()
        
        print(f"\nРезультаты восстановления:")
        print(f"Сохраненные поиски: {searches_count}")
        print(f"Рекомендации: {recommendations_count}")
        
        # Показываем статистику по пользователям
        print("\nСтатистика по пользователям:")
        user_searches = db.session.query(SavedSearch.user_id, db.func.count(SavedSearch.id)).group_by(SavedSearch.user_id).all()
        for user_id, count in user_searches:
            print(f"Пользователь {user_id}: {count} поисков")
        
        user_recs = db.session.query(Recommendation.user_id, db.func.count(Recommendation.id)).group_by(Recommendation.user_id).all()
        for user_id, count in user_recs:
            print(f"Пользователь {user_id}: {count} рекомендаций")
        
        print("\nВосстановление данных завершено!")

if __name__ == '__main__':
    main()