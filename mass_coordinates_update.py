#!/usr/bin/env python3
"""
Массовое обновление координат для всех районов, микрорайонов и улиц
"""

import os
import time
import requests
from models import db, District, Street
from app import app

def get_yandex_coordinates(query, api_key):
    """Получить координаты через Yandex Geocoder API"""
    try:
        geocoder_url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': api_key,
            'geocode': query,
            'format': 'json',
            'results': 1,
            'lang': 'ru_RU'
        }
        
        response = requests.get(geocoder_url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code} for: {query}")
            return None
            
        data = response.json()
        
        if 'response' not in data:
            print(f"  ❌ No response data for: {query}")
            return None
            
        geo_objects = data['response']['GeoObjectCollection']['featureMember']
        
        if not geo_objects:
            print(f"  ❌ No geo objects found for: {query}")
            return None
            
        # Извлекаем координаты из первого найденного объекта
        point = geo_objects[0]['GeoObject']['Point']['pos']
        lng, lat = map(float, point.split())
        
        print(f"  ✅ Found coordinates: {lat}, {lng} for: {query}")
        return {'latitude': lat, 'longitude': lng}
        
    except Exception as e:
        print(f"  ❌ Error geocoding {query}: {str(e)}")
        return None

def update_districts_coordinates():
    """Обновить координаты всех районов"""
    print("🏘️ Обновляю координаты районов...")
    
    api_key = os.environ.get('YANDEX_MAPS_API_KEY')
    if not api_key:
        print("❌ YANDEX_MAPS_API_KEY не найден")
        return
    
    districts = District.query.all()
    print(f"Найдено {len(districts)} районов")
    
    updated = 0
    for district in districts:
        if district.latitude and district.longitude:
            print(f"⏭️ {district.name} уже имеет координаты, пропускаю")
            continue
            
        print(f"\n📍 Обрабатываю район: {district.name}")
        
        # Пробуем разные варианты запросов
        queries = [
            f"{district.name} микрорайон Краснодар",
            f"{district.name} район Краснодар",
            f"{district.name} Краснодар",
            f"микрорайон {district.name} Краснодар"
        ]
        
        coordinates = None
        for query in queries:
            print(f"  🔍 Пробую запрос: {query}")
            coordinates = get_yandex_coordinates(query, api_key)
            if coordinates:
                break
            time.sleep(0.5)  # Избегаем превышения лимитов API
        
        if coordinates:
            district.latitude = coordinates['latitude']
            district.longitude = coordinates['longitude']
            db.session.commit()
            updated += 1
            print(f"  ✅ Обновлен район: {district.name}")
        else:
            print(f"  ❌ Не удалось найти координаты для: {district.name}")
        
        time.sleep(1)  # Пауза между запросами
    
    print(f"\n✅ Обновлено {updated} районов из {len(districts)}")

def update_streets_coordinates():
    """Обновить координаты всех улиц"""
    print("\n🛣️ Обновляю координаты улиц...")
    
    api_key = os.environ.get('YANDEX_MAPS_API_KEY')
    if not api_key:
        print("❌ YANDEX_MAPS_API_KEY не найден")
        return
    
    # Получаем улицы без координат
    streets = Street.query.filter(
        (Street.latitude.is_(None)) | 
        (Street.longitude.is_(None))
    ).all()
    
    print(f"Найдено {len(streets)} улиц без координат")
    
    updated = 0
    for i, street in enumerate(streets, 1):
        print(f"\n📍 [{i}/{len(streets)}] Обрабатываю улицу: {street.name}")
        
        # Пробуем разные варианты запросов
        queries = [
            f"улица {street.name} Краснодар",
            f"{street.name} улица Краснодар",
            f"{street.name} Краснодар"
        ]
        
        coordinates = None
        for query in queries:
            print(f"  🔍 Пробую запрос: {query}")
            coordinates = get_yandex_coordinates(query, api_key)
            if coordinates:
                break
            time.sleep(0.5)
        
        if coordinates:
            street.latitude = coordinates['latitude']
            street.longitude = coordinates['longitude']
            db.session.commit()
            updated += 1
            print(f"  ✅ Обновлена улица: {street.name}")
        else:
            print(f"  ❌ Не удалось найти координаты для: {street.name}")
        
        time.sleep(1)  # Пауза между запросами
        
        # Каждые 50 улиц делаем более длинную паузу
        if i % 50 == 0:
            print(f"\n⏸️ Пауза после {i} улиц...")
            time.sleep(5)
    
    print(f"\n✅ Обновлено {updated} улиц из {len(streets)}")

if __name__ == "__main__":
    with app.app_context():
        print("🚀 Запуск массового обновления координат...")
        
        # Сначала районы
        update_districts_coordinates()
        
        # Затем улицы
        update_streets_coordinates()
        
        print("\n🎉 Массовое обновление координат завершено!")