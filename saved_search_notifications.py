#!/usr/bin/env python3
"""
Система уведомлений для сохраненных поисков
Отправляет уведомления пользователям о новых объектах по их критериям поиска
"""

import os
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from email_service import send_notification

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("DATABASE_URL not set")
    sys.exit(1)

def load_properties():
    """Load properties from JSON file"""
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Properties file not found")
        return []

def check_saved_search_results():
    """
    Проверяет сохраненные поиски и отправляет уведомления о новых результатах
    """
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Получаем активные сохраненные поиски
        saved_searches = conn.execute(text("""
            SELECT s.*, u.email, u.full_name, u.preferred_contact
            FROM manager_saved_searches s
            JOIN users u ON s.user_id = u.id
            WHERE s.notify_new_results = true
            AND (s.last_notification_sent IS NULL OR s.last_notification_sent < NOW() - INTERVAL '1 day')
        """)).fetchall()
        
        properties = load_properties()
        current_time = datetime.now()
        
        for search in saved_searches:
            try:
                # Парсим фильтры поиска
                filters = json.loads(search.additional_filters) if search.additional_filters else {}
                
                # Применяем фильтры к объектам недвижимости
                matching_properties = filter_properties(properties, filters)
                
                # Если есть подходящие объекты, отправляем уведомление
                if matching_properties:
                    # Ограничиваем до 10 объектов для уведомления
                    properties_for_notification = matching_properties[:10]
                    
                    # Подготавливаем данные для уведомления
                    properties_list = []
                    for prop in properties_for_notification:
                        properties_list.append({
                            'title': prop.get('title', f"Объект {prop['id']}"),
                            'name': prop.get('name', f"Объект {prop['id']}"),
                            'rooms': prop.get('rooms'),
                            'area': prop.get('area'),
                            'price': prop.get('price'),
                            'district': prop.get('district'),
                            'complex_name': prop.get('complex_name')
                        })
                    
                    # Отправляем уведомление
                    notification_sent = send_notification(
                        recipient_email=search.email,
                        subject=f"Новые объекты по поиску \"{search.name}\"",
                        message=f"По вашему поиску найдено {len(matching_properties)} новых объектов",
                        notification_type='saved_search_results',
                        user_id=search.user_id,
                        search_name=search.name,
                        properties_list=properties_list,
                        properties_count=len(matching_properties),
                        search_url=f"/properties?search_id={search.id}"
                    )
                    
                    # Обновляем время последнего уведомления
                    if notification_sent:
                        conn.execute(text("""
                            UPDATE manager_saved_searches 
                            SET last_notification_sent = NOW()
                            WHERE id = :search_id
                        """), {'search_id': search.id})
                        conn.commit()
                        
                        print(f"Sent notification for search '{search.name}' to {search.email}")
                    
            except Exception as e:
                print(f"Error processing search {search.id}: {e}")
                continue

def filter_properties(properties, filters):
    """
    Применяет фильтры к списку объектов недвижимости
    
    Args:
        properties: Список объектов недвижимости
        filters: Словарь с фильтрами
    
    Returns:
        Отфильтрованный список объектов
    """
    filtered = properties.copy()
    
    # Фильтр по комнатам
    if filters.get('rooms'):
        rooms_list = filters['rooms']
        if isinstance(rooms_list, str):
            rooms_list = [rooms_list]
        filtered = [p for p in filtered if str(p.get('rooms', '')) in rooms_list]
    
    # Фильтр по цене
    if filters.get('priceFrom'):
        try:
            price_from = float(filters['priceFrom']) * 1000000  # Конвертируем млн в рубли
            filtered = [p for p in filtered if p.get('price', 0) >= price_from]
        except (ValueError, TypeError):
            pass
    
    if filters.get('priceTo'):
        try:
            price_to = float(filters['priceTo']) * 1000000
            filtered = [p for p in filtered if p.get('price', 0) <= price_to]
        except (ValueError, TypeError):
            pass
    
    # Фильтр по району
    if filters.get('districts') and filters['districts']:
        districts = filters['districts']
        filtered = [p for p in filtered if p.get('district') in districts]
    
    # Фильтр по застройщику
    if filters.get('developers') and filters['developers']:
        developers = filters['developers']
        filtered = [p for p in filtered if p.get('developer') in developers]
    
    # Фильтр по площади
    if filters.get('areaFrom'):
        try:
            area_from = float(filters['areaFrom'])
            filtered = [p for p in filtered if p.get('area', 0) >= area_from]
        except (ValueError, TypeError):
            pass
    
    if filters.get('areaTo'):
        try:
            area_to = float(filters['areaTo'])
            filtered = [p for p in filtered if p.get('area', 0) <= area_to]
        except (ValueError, TypeError):
            pass
    
    return filtered

def setup_notification_schedule():
    """
    Настраивает расписание для автоматических уведомлений
    Эта функция может быть вызвана через cron или другой планировщик
    """
    print(f"[{datetime.now()}] Checking for saved search notifications...")
    check_saved_search_results()
    print(f"[{datetime.now()}] Saved search notifications check completed.")

if __name__ == "__main__":
    # Запуск проверки уведомлений
    setup_notification_schedule()