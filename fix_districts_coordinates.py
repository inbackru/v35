#!/usr/bin/env python3
"""
Скрипт для исправления координат районов Краснодара через Nominatim API
Запрос: 1 в секунду (как требует Nominatim)
"""

import requests
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import District

# Номинатим API с ограничением 1 запрос в секунду
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "InBack Real Estate Platform/1.0"

def geocode_district(district_name):
    """Получить координаты района через Nominatim API"""
    
    # Формируем запрос для поиска района в Краснодаре
    queries = [
        f"{district_name}, Краснодар, Россия",
        f"микрорайон {district_name}, Краснодар", 
        f"{district_name}, Krasnodar, Russia",
        f"{district_name}, Краснодар"
    ]
    
    for query in queries:
        try:
            params = {
                'q': query,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ru',
                'bounded': 1,
                'viewbox': '38.8,44.9,39.2,45.2',  # Краснодар bbox
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': USER_AGENT
            }
            
            print(f"🔍 Поиск: {query}")
            response = requests.get(NOMINATIM_BASE_URL, params=params, headers=headers)
            
            if response.status_code == 200:
                results = response.json()
                if results:
                    result = results[0]
                    lat = float(result['lat'])
                    lon = float(result['lon'])
                    
                    # Проверяем что координаты в пределах Краснодара
                    if 44.9 <= lat <= 45.2 and 38.8 <= lon <= 39.2:
                        print(f"✅ Найден: {lat}, {lon}")
                        return lat, lon
                    else:
                        print(f"⚠️  Координаты вне Краснодара: {lat}, {lon}")
            
            # Задержка 1 секунда между запросами
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Ошибка геокодирования {query}: {e}")
            time.sleep(1)
    
    print(f"❌ Не найден: {district_name}")
    return None, None

def fix_duplicate_coordinates():
    """Исправляем дублирующиеся координаты"""
    
    with app.app_context():
        print("🚀 Запуск исправления координат районов...")
        
        # Находим районы с дублирующимися координатами
        duplicates = db.session.execute("""
            SELECT latitude, longitude, COUNT(*) as count,
                   array_agg(id) as district_ids,
                   array_agg(name) as district_names
            FROM districts 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY latitude, longitude 
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """).fetchall()
        
        print(f"📍 Найдено {len(duplicates)} групп дублирующихся координат")
        
        # Также исправляем явно неправильные координаты (аэропорт)
        airport_coords = [45.127581, 39.36184]  # Координаты аэропорта
        airport_districts = District.query.filter_by(
            latitude=airport_coords[0], 
            longitude=airport_coords[1]
        ).all()
        
        print(f"✈️  Найдено {len(airport_districts)} районов с координатами аэропорта")
        
        # Исправляем координаты аэропорта
        for district in airport_districts:
            if district.name not in ["Район аэропорта", "Пашковский"]:  # Эти могут быть рядом с аэропортом
                print(f"\n🔄 Исправляем район: {district.name}")
                
                lat, lon = geocode_district(district.name)
                if lat and lon:
                    district.latitude = lat
                    district.longitude = lon
                    print(f"✅ Обновлен {district.name}: {lat}, {lon}")
                else:
                    print(f"⚠️  Не удалось найти {district.name}")
        
        # Исправляем другие дубликаты (оставляем первый, остальным ищем новые координаты)
        for dup in duplicates:
            if dup.latitude not in airport_coords:  # Уже исправили аэропорт выше
                district_ids = dup.district_ids
                district_names = dup.district_names
                
                print(f"\n📍 Исправляем дубликаты на координатах {dup.latitude}, {dup.longitude}:")
                print(f"   Районы: {', '.join(district_names)}")
                
                # Пропускаем первый район, исправляем остальные
                for i in range(1, len(district_ids)):
                    district = District.query.get(district_ids[i])
                    if district:
                        print(f"\n🔄 Исправляем дубликат: {district.name}")
                        lat, lon = geocode_district(district.name)
                        if lat and lon:
                            district.latitude = lat
                            district.longitude = lon
                            print(f"✅ Обновлен {district.name}: {lat}, {lon}")
        
        # Сохраняем изменения
        try:
            db.session.commit()
            print("\n🎉 Координаты успешно обновлены!")
        except Exception as e:
            print(f"\n❌ Ошибка сохранения: {e}")
            db.session.rollback()

if __name__ == "__main__":
    fix_duplicate_coordinates()