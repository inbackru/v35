#!/usr/bin/env python3
"""
Полный импорт всех недостающих данных из XLSX файлов
"""

import pandas as pd
import os
import json
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

def import_all_saved_searches():
    """Импортирует ВСЕ 27 сохраненных поисков"""
    print("Импортирую все сохраненные поиски...")
    
    df = pd.read_excel('attached_assets/saved_searches (2)_1755110853172.xlsx')
    imported_count = 0
    
    for index, row in df.iterrows():
        search_id = int(row['id'])
        user_id = int(row['user_id']) if not pd.isna(row['user_id']) else 2
        
        # Создаем имя поиска
        search_name = str(row.get('search_name', '')) if not pd.isna(row.get('search_name')) else f'Поиск #{search_id}'
        if search_name == 'nan' or search_name == '':
            search_name = f'Поиск недвижимости #{search_id}'
        
        # Создаем описание из доступных данных
        description_parts = []
        if not pd.isna(row.get('location')):
            description_parts.append(f"Район: {row['location']}")
        if not pd.isna(row.get('property_type')):
            description_parts.append(f"Тип: {row['property_type']}")
        if not pd.isna(row.get('price_min')):
            description_parts.append(f"От: {int(row['price_min'])} ₽")
        if not pd.isna(row.get('price_max')):
            description_parts.append(f"До: {int(row['price_max'])} ₽")
        
        description = '; '.join(description_parts) if description_parts else 'Автоматически созданный поиск'
        
        try:
            sql = """INSERT INTO saved_searches (
                id, user_id, name, description, search_type, location, property_type,
                price_min, price_max, size_min, size_max, developer, complex_name,
                notify_new_matches, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING"""
            
            values = (
                search_id,
                user_id, 
                search_name,
                description,
                str(row.get('search_type', 'apartment')),
                str(row.get('location', 'Краснодар')),
                str(row.get('property_type', 'квартира')),
                int(row['price_min']) if not pd.isna(row.get('price_min')) else None,
                int(row['price_max']) if not pd.isna(row.get('price_max')) else None,
                float(row['size_min']) if not pd.isna(row.get('size_min')) else None,
                float(row['size_max']) if not pd.isna(row.get('size_max')) else None,
                str(row.get('developer', '')) if not pd.isna(row.get('developer')) else '',
                str(row.get('complex_name', '')) if not pd.isna(row.get('complex_name')) else '',
                bool(row.get('notify_new_matches', False)),
                safe_convert_datetime(row['created_at']),
                safe_convert_datetime(row['updated_at'])
            )
            
            db.session.execute(db.text(sql), values)
            imported_count += 1
            print(f"Импортирован поиск {search_id}: {search_name} для пользователя {user_id}")
            
        except Exception as e:
            print(f"Ошибка импорта поиска {search_id}: {e}")
            continue
    
    db.session.commit()
    print(f"Импортировано поисков: {imported_count}")

def import_all_recommendations():
    """Импортирует ВСЕ 21 рекомендацию"""
    print("Импортирую все рекомендации...")
    
    df = pd.read_excel('attached_assets/recommendations (2)_1755110853173.xlsx')
    imported_count = 0
    
    for index, row in df.iterrows():
        rec_id = int(row['id'])
        client_id = int(row.get('client_id', row.get('user_id', 2)))
        manager_id = int(row.get('manager_id', 1))
        
        title = str(row.get('title', f'Рекомендация #{rec_id}'))
        if title == 'nan' or title == '':
            title = f'Рекомендация объекта #{rec_id}'
            
        description = str(row.get('description', 'Рекомендуемый объект недвижимости'))
        if description == 'nan' or description == '':
            description = 'Рекомендуемый объект недвижимости от менеджера'
        
        item_id = str(row.get('item_id', row.get('property_id', str(rec_id))))
        item_name = str(row.get('item_name', f'Объект недвижимости #{item_id}'))
        if item_name == 'nan' or item_name == '':
            item_name = f'Рекомендуемый объект #{item_id}'
        
        try:
            sql = """INSERT INTO recommendations (
                id, manager_id, client_id, title, description, recommendation_type,
                item_id, item_name, status, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING"""
            
            values = (
                rec_id,
                manager_id,
                client_id,
                title,
                description,
                str(row.get('recommendation_type', 'property')),
                item_id,
                item_name,
                str(row.get('status', 'pending')),
                safe_convert_datetime(row['created_at'])
            )
            
            db.session.execute(db.text(sql), values)
            imported_count += 1
            print(f"Импортирована рекомендация {rec_id}: {title} для клиента {client_id}")
            
        except Exception as e:
            print(f"Ошибка импорта рекомендации {rec_id}: {e}")
            continue
    
    db.session.commit()
    print(f"Импортировано рекомендаций: {imported_count}")

def import_all_favorites():
    """Импортирует ВСЕ 28 избранных объектов"""
    print("Импортирую все избранные объекты...")
    
    df = pd.read_excel('attached_assets/favorite_properties (2)_1755110853173.xlsx')
    imported_count = 0
    
    for index, row in df.iterrows():
        try:
            user_id = int(row['user_id'])
            property_id = int(row['property_id'])
            
            sql = """INSERT INTO favorite_properties (
                user_id, property_id, created_at
            ) VALUES (%s, %s, %s)
            ON CONFLICT (user_id, property_id) DO NOTHING"""
            
            values = (
                user_id,
                property_id,
                safe_convert_datetime(row.get('created_at', datetime.utcnow()))
            )
            
            db.session.execute(db.text(sql), values)
            imported_count += 1
            print(f"Добавлен в избранное: объект {property_id} пользователем {user_id}")
            
        except Exception as e:
            print(f"Ошибка добавления в избранное строка {index}: {e}")
            continue
    
    db.session.commit()
    print(f"Импортировано избранных: {imported_count}")

def main():
    """Главная функция импорта всех данных"""
    print("=== ПОЛНЫЙ ИМПОРТ ВСЕХ НЕДОСТАЮЩИХ ДАННЫХ ===")
    
    with app.app_context():
        # Импортируем все данные
        import_all_saved_searches()
        import_all_recommendations() 
        import_all_favorites()
        
        # Обновляем sequence
        try:
            db.session.execute(db.text("SELECT setval('saved_searches_id_seq', (SELECT MAX(id) FROM saved_searches))"))
            db.session.execute(db.text("SELECT setval('recommendations_id_seq', (SELECT MAX(id) FROM recommendations))"))
            db.session.commit()
            print("Sequences обновлены!")
        except Exception as e:
            print(f"Ошибка обновления sequences: {e}")
        
        # Финальная статистика
        results = db.session.execute(db.text("""
            SELECT 
                'saved_searches' as table_name, COUNT(*) as count FROM saved_searches
            UNION ALL SELECT 
                'recommendations', COUNT(*) FROM recommendations
            UNION ALL SELECT 
                'favorite_properties', COUNT(*) FROM favorite_properties
            ORDER BY table_name
        """)).fetchall()
        
        print("\n=== ФИНАЛЬНАЯ СТАТИСТИКА ===")
        for table_name, count in results:
            print(f"{table_name}: {count}")
        
        print("\n✅ Импорт всех данных завершен!")

if __name__ == '__main__':
    main()