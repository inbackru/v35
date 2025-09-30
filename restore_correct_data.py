#!/usr/bin/env python3
"""
Восстановление сохраненных поисков и рекомендаций с правильной структурой
"""

import pandas as pd
import os
from datetime import datetime
from app import app, db

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

def safe_int(value, default=None):
    """Безопасное преобразование в int"""
    try:
        if pd.isna(value):
            return default
        return int(value)
    except:
        return default

def safe_str(value, default=''):
    """Безопасное преобразование в str"""
    try:
        if pd.isna(value):
            return default
        return str(value)
    except:
        return default

def restore_saved_searches():
    """Восстанавливает сохраненные поиски в правильную структуру"""
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
                # Подготавливаем данные для вставки напрямую в SQL
                search_data = {
                    'id': safe_int(row['id']),
                    'user_id': safe_int(row['user_id']),
                    'name': safe_str(row.get('search_name', row.get('name', 'Поиск'))),
                    'description': safe_str(row.get('description', '')),
                    'search_type': safe_str(row.get('search_type', '')),
                    'location': safe_str(row.get('location', '')),
                    'property_type': safe_str(row.get('property_type', '')),
                    'price_min': safe_int(row.get('price_min')),
                    'price_max': safe_int(row.get('price_max')),
                    'size_min': row.get('size_min') if not pd.isna(row.get('size_min')) else None,
                    'size_max': row.get('size_max') if not pd.isna(row.get('size_max')) else None,
                    'developer': safe_str(row.get('developer', '')),
                    'complex_name': safe_str(row.get('complex_name', '')),
                    'floor_min': safe_int(row.get('floor_min')),
                    'floor_max': safe_int(row.get('floor_max')),
                    'cashback_min': safe_int(row.get('cashback_min')),
                    'additional_filters': safe_str(row.get('additional_filters', '')),
                    'notify_new_matches': bool(row.get('notify_new_matches', False)) if not pd.isna(row.get('notify_new_matches')) else False,
                    'last_notification_sent': safe_convert_datetime(row.get('last_notification_sent')) if not pd.isna(row.get('last_notification_sent')) else None,
                    'created_from_quiz': bool(row.get('created_from_quiz', False)) if not pd.isna(row.get('created_from_quiz')) else False,
                    'created_at': safe_convert_datetime(row['created_at']),
                    'updated_at': safe_convert_datetime(row['updated_at']),
                    'last_used': safe_convert_datetime(row.get('last_used')) if not pd.isna(row.get('last_used')) else None
                }
                
                if search_data['id'] and search_data['user_id']:
                    # Используем SQL для вставки, чтобы избежать проблем с моделями
                    sql_query = """
                    INSERT INTO saved_searches (
                        id, user_id, name, description, search_type, location, property_type,
                        price_min, price_max, size_min, size_max, developer, complex_name,
                        floor_min, floor_max, cashback_min, additional_filters, notify_new_matches,
                        last_notification_sent, created_from_quiz, created_at, updated_at, last_used
                    ) VALUES (
                        %(id)s, %(user_id)s, %(name)s, %(description)s, %(search_type)s, %(location)s, %(property_type)s,
                        %(price_min)s, %(price_max)s, %(size_min)s, %(size_max)s, %(developer)s, %(complex_name)s,
                        %(floor_min)s, %(floor_max)s, %(cashback_min)s, %(additional_filters)s, %(notify_new_matches)s,
                        %(last_notification_sent)s, %(created_from_quiz)s, %(created_at)s, %(updated_at)s, %(last_used)s
                    ) ON CONFLICT (id) DO NOTHING;
                    """
                    
                    db.session.execute(db.text(sql_query), search_data)
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
    """Восстанавливает рекомендации в правильную структуру"""
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
                    'id': safe_int(row['id']),
                    'manager_id': safe_int(row.get('manager_id', row.get('created_by_manager_id'))),
                    'client_id': safe_int(row.get('client_id', row.get('user_id'))),
                    'category_id': safe_int(row.get('category_id')),
                    'title': safe_str(row.get('title', '')),
                    'description': safe_str(row.get('description', '')),
                    'recommendation_type': safe_str(row.get('recommendation_type', 'property')),
                    'item_id': safe_str(row.get('item_id', row.get('property_id', ''))),
                    'item_name': safe_str(row.get('item_name', '')),
                    'item_data': safe_str(row.get('item_data', '')),
                    'manager_notes': safe_str(row.get('manager_notes', '')),
                    'highlighted_features': safe_str(row.get('highlighted_features', '')),
                    'priority_level': safe_str(row.get('priority_level', 'medium')),
                    'status': safe_str(row.get('status', 'pending')),
                    'viewed_at': safe_convert_datetime(row.get('viewed_at')) if not pd.isna(row.get('viewed_at')) else None,
                    'responded_at': safe_convert_datetime(row.get('responded_at')) if not pd.isna(row.get('responded_at')) else None,
                    'client_response': safe_str(row.get('client_response', '')),
                    'client_notes': safe_str(row.get('client_notes', '')),
                    'viewing_requested': bool(row.get('viewing_requested', False)) if not pd.isna(row.get('viewing_requested')) else False,
                    'viewing_scheduled_at': safe_convert_datetime(row.get('viewing_scheduled_at')) if not pd.isna(row.get('viewing_scheduled_at')) else None,
                    'created_at': safe_convert_datetime(row['created_at']),
                    'sent_at': safe_convert_datetime(row.get('sent_at')) if not pd.isna(row.get('sent_at')) else None,
                    'expires_at': safe_convert_datetime(row.get('expires_at')) if not pd.isna(row.get('expires_at')) else None
                }
                
                if rec_data['id'] and rec_data['client_id']:
                    sql_query = """
                    INSERT INTO recommendations (
                        id, manager_id, client_id, category_id, title, description, recommendation_type,
                        item_id, item_name, item_data, manager_notes, highlighted_features, priority_level,
                        status, viewed_at, responded_at, client_response, client_notes, viewing_requested,
                        viewing_scheduled_at, created_at, sent_at, expires_at
                    ) VALUES (
                        %(id)s, %(manager_id)s, %(client_id)s, %(category_id)s, %(title)s, %(description)s, %(recommendation_type)s,
                        %(item_id)s, %(item_name)s, %(item_data)s, %(manager_notes)s, %(highlighted_features)s, %(priority_level)s,
                        %(status)s, %(viewed_at)s, %(responded_at)s, %(client_response)s, %(client_notes)s, %(viewing_requested)s,
                        %(viewing_scheduled_at)s, %(created_at)s, %(sent_at)s, %(expires_at)s
                    ) ON CONFLICT (id) DO NOTHING;
                    """
                    
                    db.session.execute(db.text(sql_query), rec_data)
                    imported_count += 1
                    print(f"Восстановлена рекомендация для клиента {rec_data['client_id']} объект {rec_data['item_id']}")
                
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
        searches_result = db.session.execute(db.text("SELECT COUNT(*) as count FROM saved_searches")).fetchone()
        recommendations_result = db.session.execute(db.text("SELECT COUNT(*) as count FROM recommendations")).fetchone()
        
        print(f"\nРезультаты восстановления:")
        print(f"Сохраненные поиски: {searches_result[0]}")
        print(f"Рекомендации: {recommendations_result[0]}")
        
        # Показываем статистику по пользователям
        print("\nСтатистика по пользователям:")
        user_searches = db.session.execute(db.text("SELECT user_id, COUNT(*) FROM saved_searches GROUP BY user_id")).fetchall()
        for user_id, count in user_searches:
            print(f"Пользователь {user_id}: {count} поисков")
        
        user_recs = db.session.execute(db.text("SELECT client_id, COUNT(*) FROM recommendations GROUP BY client_id")).fetchall()
        for user_id, count in user_recs:
            print(f"Пользователь {user_id}: {count} рекомендаций")
        
        print("\nВосстановление данных завершено!")

if __name__ == '__main__':
    main()