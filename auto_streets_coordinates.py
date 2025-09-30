#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import logging
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_yandex_coordinates(query, api_key, max_retries=3):
    """Получение координат через Yandex Geocoder API"""
    
    for attempt in range(max_retries):
        try:
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                'apikey': api_key,
                'geocode': query,
                'format': 'json',
                'results': 1,
                'kind': 'street'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Извлекаем координаты
                try:
                    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                    lng, lat = map(float, pos.split())
                    return lat, lng
                except (KeyError, IndexError):
                    return None, None
            else:
                logging.warning(f"Ошибка API (попытка {attempt + 1}): {response.status_code}")
                
        except Exception as e:
            logging.warning(f"Ошибка запроса (попытка {attempt + 1}): {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Экспоненциальная задержка
    
    return None, None

def process_streets_batch(batch_size=25):
    """
    Обрабатывает улицы пакетами для получения координат
    """
    
    database_url = os.environ.get('DATABASE_URL')
    api_key = os.environ.get('YANDEX_MAPS_API_KEY')
    
    if not database_url or not api_key:
        logging.error("❌ Отсутствуют необходимые переменные окружения")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Получаем улицы без координат
        streets_query = text("""
            SELECT id, name 
            FROM streets 
            WHERE latitude IS NULL OR longitude IS NULL
            ORDER BY name
            LIMIT :batch_size
        """)
        
        streets = session.execute(streets_query, {'batch_size': batch_size}).fetchall()
        
        if not streets:
            logging.info("✅ Все улицы уже имеют координаты!")
            return True
        
        logging.info(f"🛣️ Обрабатываю пакет из {len(streets)} улиц")
        
        success_count = 0
        error_count = 0
        
        for i, street in enumerate(streets, 1):
            street_id, name = street
            
            # Формируем поисковой запрос
            query = f"{name}, Краснодар"
            
            logging.info(f"[{i}/{len(streets)}] Обрабатываю: {name}")
            
            try:
                lat, lng = get_yandex_coordinates(query, api_key)
                
                if lat and lng:
                    # Обновляем координаты
                    update_query = text("""
                        UPDATE streets 
                        SET latitude = :lat, longitude = :lng, updated_at = NOW()
                        WHERE id = :street_id
                    """)
                    
                    session.execute(update_query, {
                        'lat': lat,
                        'lng': lng,
                        'street_id': street_id
                    })
                    
                    success_count += 1
                    logging.info(f"  ✅ {name}: {lat:.6f}, {lng:.6f}")
                else:
                    error_count += 1
                    logging.warning(f"  ⚠️ Координаты не найдены для: {name}")
                
                # Пауза для API
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"  ❌ Ошибка для улицы {name}: {e}")
                error_count += 1
                continue
        
        session.commit()
        session.close()
        
        logging.info(f"\\n📈 Пакет обработан:")
        logging.info(f"   ✅ Успешно: {success_count}")
        logging.info(f"   ⚠️ Ошибки: {error_count}")
        
        return success_count > 0
        
    except Exception as e:
        logging.error(f"❌ Общая ошибка: {e}")
        return False

def main():
    """Основная функция - обрабатывает один пакет"""
    logging.info("🚀 Запуск обработки координат улиц")
    
    # Обрабатываем один пакет
    success = process_streets_batch(batch_size=25)
    
    if success:
        logging.info("✅ Пакет обработан успешно")
        exit(0)
    else:
        logging.info("⚠️ Обработка завершена (возможно, нет данных для обработки)")
        exit(0)

if __name__ == "__main__":
    main()