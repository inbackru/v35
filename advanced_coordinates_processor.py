#!/usr/bin/env python3
"""
Продвинутый процессор координат для массовой обработки районов и улиц
Поддерживает пакетную обработку, кэширование, возобновление и лимиты API
"""

import os
import time
import json
import sqlite3
import requests
from datetime import datetime
from models import db, District, Street
from app import app

class AdvancedCoordinatesProcessor:
    def __init__(self):
        self.api_key = os.environ.get('YANDEX_MAPS_API_KEY')
        self.cache_file = 'coordinates_cache.json'
        self.progress_file = 'coordinates_progress.json'
        self.batch_size = 50  # обрабатываем по 50 объектов
        self.daily_limit = 25000  # дневной лимит API запросов (Яндекс Геокодер)
        self.requests_per_second = 10  # максимум 10 запросов в секунду
        self.cache = self.load_cache()
        self.progress = self.load_progress()
        
    def load_cache(self):
        """Загружает кэш координат из файла"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Ошибка загрузки кэша: {e}")
        return {}
    
    def save_cache(self):
        """Сохраняет кэш координат в файл"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Ошибка сохранения кэша: {e}")
    
    def load_progress(self):
        """Загружает прогресс обработки"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Ошибка загрузки прогресса: {e}")
        return {
            'districts_processed': 0,
            'streets_processed': 0,
            'last_run': None,
            'daily_requests_count': 0,
            'last_request_date': None
        }
    
    def save_progress(self):
        """Сохраняет прогресс обработки"""
        try:
            self.progress['last_run'] = datetime.now().isoformat()
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Ошибка сохранения прогресса: {e}")
    
    def check_daily_limit(self):
        """Проверяет дневной лимит API запросов"""
        today = datetime.now().strftime('%Y-%m-%d')
        if self.progress.get('last_request_date') != today:
            self.progress['daily_requests_count'] = 0
            self.progress['last_request_date'] = today
        
        return self.progress['daily_requests_count'] < self.daily_limit
    
    def get_coordinates_cached(self, query):
        """Получает координаты с использованием кэша"""
        # Проверяем кэш
        cache_key = query.lower().strip()
        if cache_key in self.cache:
            print(f"  💾 Из кэша: {query}")
            return self.cache[cache_key]
        
        # Проверяем дневной лимит
        if not self.check_daily_limit():
            print(f"  ⚠️ Превышен дневной лимит API запросов ({self.daily_limit})")
            return None
        
        # Делаем запрос к API
        coordinates = self.get_yandex_coordinates(query)
        
        # Сохраняем в кэш
        if coordinates:
            self.cache[cache_key] = coordinates
        else:
            self.cache[cache_key] = None
            
        # Обновляем счетчик запросов
        self.progress['daily_requests_count'] += 1
        
        # Соблюдаем лимит скорости
        time.sleep(1 / self.requests_per_second)
        
        return coordinates
    
    def get_yandex_coordinates(self, query):
        """Получает координаты через Yandex Geocoder API"""
        try:
            geocoder_url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                'apikey': self.api_key,
                'geocode': query,
                'format': 'json',
                'results': 1,
                'lang': 'ru_RU'
            }
            
            response = requests.get(geocoder_url, params=params, timeout=15)
            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code} for: {query}")
                return None
                
            data = response.json()
            
            if 'response' not in data:
                return None
                
            geo_objects = data['response']['GeoObjectCollection']['featureMember']
            
            if not geo_objects:
                return None
                
            point = geo_objects[0]['GeoObject']['Point']['pos']
            lng, lat = map(float, point.split())
            
            return {'latitude': lat, 'longitude': lng}
            
        except Exception as e:
            print(f"  ❌ Ошибка: {str(e)}")
            return None
    
    def process_districts_batch(self, batch_size=None):
        """Обрабатывает пакет районов"""
        if batch_size is None:
            batch_size = self.batch_size
            
        # Получаем районы без координат, начиная с последней позиции
        districts = District.query.filter(
            (District.latitude.is_(None)) | 
            (District.longitude.is_(None))
        ).offset(self.progress['districts_processed']).limit(batch_size).all()
        
        if not districts:
            print("✅ Все районы уже имеют координаты")
            return True
        
        print(f"🏘️ Обрабатываю пакет районов: {len(districts)} шт.")
        processed = 0
        
        for district in districts:
            if not self.check_daily_limit():
                print(f"⚠️ Достигнут дневной лимит API запросов")
                break
                
            print(f"📍 Обрабатываю район: {district.name}")
            
            queries = [
                f"{district.name} микрорайон Краснодар",
                f"{district.name} район Краснодар", 
                f"{district.name} Краснодар",
                f"микрорайон {district.name} Краснодар"
            ]
            
            coordinates = None
            for query in queries:
                coordinates = self.get_coordinates_cached(query)
                if coordinates:
                    break
            
            if coordinates:
                district.latitude = coordinates['latitude']
                district.longitude = coordinates['longitude']
                db.session.commit()
                print(f"  ✅ Обновлен: {district.name}")
                processed += 1
            else:
                print(f"  ❌ Не найдены координаты: {district.name}")
            
            self.progress['districts_processed'] += 1
            
            # Сохраняем прогресс каждые 5 записей
            if processed % 5 == 0:
                self.save_progress()
                self.save_cache()
        
        self.save_progress()
        self.save_cache()
        
        return len(districts) < batch_size  # True если все обработано
    
    def process_streets_batch(self, batch_size=None):
        """Обрабатывает пакет улиц"""
        if batch_size is None:
            batch_size = self.batch_size
            
        streets = Street.query.filter(
            (Street.latitude.is_(None)) | 
            (Street.longitude.is_(None))
        ).offset(self.progress['streets_processed']).limit(batch_size).all()
        
        if not streets:
            print("✅ Все улицы уже имеют координаты")
            return True
        
        print(f"🛣️ Обрабатываю пакет улиц: {len(streets)} шт.")
        processed = 0
        
        for street in streets:
            if not self.check_daily_limit():
                print(f"⚠️ Достигнут дневной лимит API запросов")
                break
                
            print(f"📍 Обрабатываю улицу: {street.name}")
            
            queries = [
                f"улица {street.name} Краснодар",
                f"{street.name} улица Краснодар",
                f"{street.name} Краснодар"
            ]
            
            coordinates = None
            for query in queries:
                coordinates = self.get_coordinates_cached(query)
                if coordinates:
                    break
            
            if coordinates:
                street.latitude = coordinates['latitude']
                street.longitude = coordinates['longitude']
                db.session.commit()
                print(f"  ✅ Обновлена: {street.name}")
                processed += 1
            else:
                print(f"  ❌ Не найдены координаты: {street.name}")
            
            self.progress['streets_processed'] += 1
            
            # Сохраняем прогресс каждые 10 записей
            if processed % 10 == 0:
                self.save_progress()
                self.save_cache()
        
        self.save_progress()
        self.save_cache()
        
        return len(streets) < batch_size  # True если все обработано
    
    def get_stats(self):
        """Получает статистику обработки"""
        with app.app_context():
            total_districts = District.query.count()
            districts_with_coords = District.query.filter(
                District.latitude.isnot(None), 
                District.longitude.isnot(None)
            ).count()
            
            total_streets = Street.query.count()
            streets_with_coords = Street.query.filter(
                Street.latitude.isnot(None),
                Street.longitude.isnot(None)
            ).count()
            
            return {
                'districts': {
                    'total': total_districts,
                    'with_coords': districts_with_coords,
                    'remaining': total_districts - districts_with_coords
                },
                'streets': {
                    'total': total_streets,
                    'with_coords': streets_with_coords,
                    'remaining': total_streets - streets_with_coords
                },
                'api_usage': {
                    'daily_requests': self.progress['daily_requests_count'],
                    'daily_limit': self.daily_limit,
                    'remaining': self.daily_limit - self.progress['daily_requests_count']
                }
            }
    
    def run_incremental_processing(self):
        """Запускает инкрементальную обработку"""
        print("🚀 Запуск инкрементальной обработки координат...")
        
        if not self.api_key:
            print("❌ YANDEX_MAPS_API_KEY не найден")
            return
        
        # Показываем статистику
        stats = self.get_stats()
        print(f"""
📊 Текущая статистика:
   Районы: {stats['districts']['with_coords']}/{stats['districts']['total']} ({stats['districts']['remaining']} осталось)
   Улицы: {stats['streets']['with_coords']}/{stats['streets']['total']} ({stats['streets']['remaining']} осталось)
   API запросы: {stats['api_usage']['daily_requests']}/{stats['api_usage']['daily_limit']} ({stats['api_usage']['remaining']} осталось)
        """)
        
        if not self.check_daily_limit():
            print("⚠️ Дневной лимит API запросов исчерпан. Попробуйте завтра.")
            return
        
        # Сначала обрабатываем районы
        districts_done = False
        if stats['districts']['remaining'] > 0:
            districts_done = self.process_districts_batch()
        else:
            districts_done = True
            print("✅ Все районы уже имеют координаты")
        
        # Затем обрабатываем улицы
        if districts_done and stats['streets']['remaining'] > 0 and self.check_daily_limit():
            self.process_streets_batch()
        
        # Финальная статистика
        final_stats = self.get_stats()
        print(f"""
🎉 Обработка завершена!
   Районы: {final_stats['districts']['with_coords']}/{final_stats['districts']['total']}
   Улицы: {final_stats['streets']['with_coords']}/{final_stats['streets']['total']}
   Использовано API запросов: {final_stats['api_usage']['daily_requests']}/{final_stats['api_usage']['daily_limit']}
        """)

if __name__ == "__main__":
    with app.app_context():
        processor = AdvancedCoordinatesProcessor()
        processor.run_incremental_processing()