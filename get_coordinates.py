#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для получения координат районов и улиц Краснодара через Nominatim API
Соблюдает ограничение: 1 запрос в секунду
"""

import requests
import time
import json
from datetime import datetime
from app import app, db
from models import District, Street

# Nominatim API settings
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
REQUEST_DELAY = 1.0  # 1 секунда между запросами
TIMEOUT = 10  # таймаут для HTTP запросов

# User Agent для Nominatim (обязательный параметр)
USER_AGENT = "InBack Real Estate App / 1.0 (https://inback.ru; info@inback.ru)"

# Список районов Краснодара (из app.py)
KRASNODAR_DISTRICTS = [
    ('Центральный', 'tsentralnyy'),
    ('Западный', 'zapadny'), 
    ('Карасунский', 'karasunsky'),
    ('Прикубанский', 'prikubansky'),
    ('Фестивальный', 'festivalny'),
    ('Юбилейный', 'yubileynyy'),
    ('Гидростроителей', 'gidrostroitelei'),
    ('Солнечный', 'solnechny'),
    ('Панорама', 'panorama'),
    ('Музыкальный', 'muzykalnyy'),
    ('9-й километр', '9-y-kilometr'),
    ('40 лет Победы', '40-let-pobedy'),
    ('Авиагородок', 'aviagorodok'),
    ('Аврора', 'avrora'),
    ('Баскет Холл', 'basket-hall'),
    ('Березовый', 'berezovy'),
    ('Комсомольский', 'komsomolsky')
]

def get_coordinates(location_name, location_type="district"):
    """
    Получить координаты локации через Nominatim API
    
    Args:
        location_name (str): Название локации
        location_type (str): Тип локации ("district" или "street")
    
    Returns:
        dict: {"lat": float, "lon": float} или None если не найдено
    """
    print(f"🔍 Поиск координат для: {location_name} ({location_type})")
    
    # Подготовка запроса
    if location_type == "district":
        query = f"{location_name} район Краснодар"
        # Альтернативные варианты поиска
        alternative_queries = [
            f"{location_name} микрорайон Краснодар",
            f"{location_name} Краснодар",
            f"Краснодар {location_name}"
        ]
    else:  # street
        query = f"{location_name} улица Краснодар"
        alternative_queries = [
            f"улица {location_name} Краснодар",
            f"{location_name} Краснодар Краснодарский край"
        ]
    
    # Попытка поиска с основным запросом
    coords = _search_nominatim(query)
    if coords:
        return coords
    
    # Попытка альтернативных запросов
    for alt_query in alternative_queries:
        print(f"  📋 Альтернативный запрос: {alt_query}")
        time.sleep(REQUEST_DELAY)  # Ждем перед следующим запросом
        coords = _search_nominatim(alt_query)
        if coords:
            return coords
    
    print(f"  ❌ Координаты не найдены для: {location_name}")
    return None

def _search_nominatim(query):
    """
    Выполнить запрос к Nominatim API
    
    Args:
        query (str): Поисковый запрос
    
    Returns:
        dict: {"lat": float, "lon": float} или None
    """
    params = {
        'q': query,
        'format': 'json',
        'limit': 5,  # Получаем несколько результатов для выбора лучшего
        'countrycodes': 'ru',  # Ограничиваем поиск Россией
        'addressdetails': 1,
        'bounded': 1,
        'viewbox': '38.8,44.9,39.1,45.1',  # Примерные границы Краснодара
    }
    
    headers = {
        'User-Agent': USER_AGENT
    }
    
    try:
        response = requests.get(
            NOMINATIM_BASE_URL,
            params=params,
            headers=headers,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        results = response.json()
        
        if not results:
            return None
        
        # Выбираем лучший результат
        best_result = None
        for result in results:
            # Проверяем, что результат относится к Краснодару
            address = result.get('address', {})
            city = address.get('city', '').lower()
            town = address.get('town', '').lower()
            
            if 'краснодар' in city or 'krasnodar' in city or 'краснодар' in town:
                best_result = result
                break
        
        if best_result:
            lat = float(best_result['lat'])
            lon = float(best_result['lon'])
            display_name = best_result.get('display_name', '')
            print(f"  ✅ Найдено: {lat:.6f}, {lon:.6f} - {display_name}")
            return {'lat': lat, 'lon': lon}
    
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Ошибка HTTP запроса: {e}")
    except (ValueError, KeyError) as e:
        print(f"  ❌ Ошибка парсинга ответа: {e}")
    except Exception as e:
        print(f"  ❌ Неожиданная ошибка: {e}")
    
    return None

def update_district_coordinates():
    """Обновить координаты всех районов"""
    print("🏘️  Обновление координат районов...")
    updated_count = 0
    
    with app.app_context():
        for district_name, district_slug in KRASNODAR_DISTRICTS:
            district = District.query.filter_by(slug=district_slug).first()
            
            if not district:
                # Создаем район если его нет
                print(f"  📍 Создание района: {district_name}")
                district = District(name=district_name, slug=district_slug)
                db.session.add(district)
                db.session.commit()
            
            # Пропускаем если координаты уже есть
            if district.latitude and district.longitude:
                print(f"  ⏩ У района {district_name} уже есть координаты: {district.latitude:.6f}, {district.longitude:.6f}")
                continue
            
            # Получаем координаты
            coords = get_coordinates(district_name, "district")
            
            if coords:
                district.latitude = coords['lat']
                district.longitude = coords['lon']
                district.updated_at = datetime.utcnow()
                
                try:
                    db.session.commit()
                    updated_count += 1
                    print(f"  ✅ Обновлен район: {district_name} -> {coords['lat']:.6f}, {coords['lon']:.6f}")
                except Exception as e:
                    print(f"  ❌ Ошибка сохранения района {district_name}: {e}")
                    db.session.rollback()
            else:
                print(f"  ❌ Не удалось получить координаты для района: {district_name}")
            
            # Задержка между запросами
            if coords:  # Только если был запрос к API
                time.sleep(REQUEST_DELAY)
    
    print(f"✅ Обновлено районов: {updated_count}")

def update_street_coordinates():
    """Обновить координаты улиц из функции load_streets"""
    print("🛣️  Обновление координат улиц...")
    
    updated_count = 0
    
    with app.app_context():
        # Импортируем функцию load_streets из app.py
        from app import load_streets
        
        # Загружаем данные об улицах  
        try:
            streets_data = load_streets()
            print(f"  📂 Загружено улиц: {len(streets_data)}")
        except Exception as e:
            print(f"  ❌ Ошибка загрузки данных об улицах: {e}")
            return
        
        if not streets_data:
            print("  ❌ Нет данных об улицах для обработки")
            return
        
        # Обрабатываем только первые 20 улиц для тестирования
        sample_streets = streets_data[:20] if len(streets_data) > 20 else streets_data
        total_streets = len(sample_streets)
        
        print(f"  📊 Обрабатываем {total_streets} улиц из {len(streets_data)} (первые для тестирования)")
        
        for i, street_data in enumerate(sample_streets, 1):
            street_name = street_data.get('name', '').strip()
            
            if not street_name:
                continue
                
            print(f"  📍 [{i}/{total_streets}] Обработка улицы: {street_name}")
            
            # Найти или создать улицу в базе
            street = Street.query.filter_by(name=street_name).first()
            if not street:
                # Создаем slug для новой улицы
                street_slug = street_name.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '').replace(',', '')
                street = Street(name=street_name, slug=street_slug)
                db.session.add(street)
                db.session.commit()
            
            # Пропускаем если координаты уже есть
            if street.latitude and street.longitude:
                print(f"    ⏩ У улицы уже есть координаты: {street.latitude:.6f}, {street.longitude:.6f}")
                continue
            
            # Получаем координаты
            coords = get_coordinates(street_name, "street")
            
            if coords:
                street.latitude = coords['lat']
                street.longitude = coords['lon']
                street.updated_at = datetime.utcnow()
                
                try:
                    db.session.commit()
                    updated_count += 1
                    print(f"    ✅ Обновлена улица: {street_name} -> {coords['lat']:.6f}, {coords['lon']:.6f}")
                except Exception as e:
                    print(f"    ❌ Ошибка сохранения улицы {street_name}: {e}")
                    db.session.rollback()
            else:
                print(f"    ❌ Не удалось получить координаты для улицы: {street_name}")
            
            # Задержка между запросами
            time.sleep(REQUEST_DELAY)
    
    print(f"✅ Обновлено улиц: {updated_count}")

def main():
    """Основная функция"""
    print("🚀 Запуск скрипта получения координат для районов и улиц")
    print("⏱️  Учитывается ограничение Nominatim: 1 запрос в секунду")
    print("=" * 60)
    
    start_time = time.time()
    
    # Обновляем координаты районов
    update_district_coordinates()
    print()
    
    # Обновляем координаты улиц (первые 20 для теста)
    update_street_coordinates()
    print()
    
    # Итоговая статистика
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 60)
    print(f"🎉 Скрипт завершен за {duration:.1f} секунд")
    
    # Показываем статистику из базы данных
    with app.app_context():
        districts_with_coords = District.query.filter(
            District.latitude.isnot(None),
            District.longitude.isnot(None)
        ).count()
        
        streets_with_coords = Street.query.filter(
            Street.latitude.isnot(None),
            Street.longitude.isnot(None)
        ).count()
        
        print(f"📊 Районов с координатами: {districts_with_coords}")
        print(f"📊 Улиц с координатами: {streets_with_coords}")

if __name__ == "__main__":
    main()