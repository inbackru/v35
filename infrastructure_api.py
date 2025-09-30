#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
from math import radians, cos, sin, asin, sqrt
from typing import List, Dict, Tuple, Optional

# Центр Краснодара (драматический театр - точные координаты)
KRASNODAR_CENTER = (45.035180, 38.977414)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние между двумя точками по формуле гаверсинусов
    Возвращает расстояние в километрах
    """
    # Перевод в радианы
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Формула гаверсинусов
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Радиус Земли в километрах
    r = 6371
    return c * r

def get_poi_around_coordinates(lat: float, lng: float, radius: int = 2000) -> Dict:
    """
    Получает POI (точки интереса) в радиусе от координат через Overpass API
    
    Args:
        lat, lng: координаты центра поиска
        radius: радиус поиска в метрах (по умолчанию 2км)
    
    Returns:
        Dict с категорированными POI и их данными
    """
    
    # Overpass запрос для получения различных типов POI
    overpass_query = f"""
    [out:json][timeout:25];
    (
      // Медицинские учреждения
      node["amenity"="hospital"](around:{radius},{lat},{lng});
      node["amenity"="clinic"](around:{radius},{lat},{lng});
      node["amenity"="pharmacy"](around:{radius},{lat},{lng});
      node["amenity"="doctors"](around:{radius},{lat},{lng});
      
      // Образовательные учреждения
      node["amenity"="school"](around:{radius},{lat},{lng});
      node["amenity"="kindergarten"](around:{radius},{lat},{lng});
      node["amenity"="university"](around:{radius},{lat},{lng});
      node["amenity"="college"](around:{radius},{lat},{lng});
      
      // Торговые объекты
      node["shop"](around:{radius},{lat},{lng});
      node["amenity"="marketplace"](around:{radius},{lat},{lng});
      
      // Транспорт
      node["highway"="bus_stop"](around:{radius},{lat},{lng});
      node["railway"="station"](around:{radius},{lat},{lng});
      node["amenity"="fuel"](around:{radius},{lat},{lng});
      
      // Финансовые услуги
      node["amenity"="bank"](around:{radius},{lat},{lng});
      node["amenity"="atm"](around:{radius},{lat},{lng});
      
      // Досуг и развлечения
      node["amenity"="restaurant"](around:{radius},{lat},{lng});
      node["amenity"="cafe"](around:{radius},{lat},{lng});
      node["leisure"="park"](around:{radius},{lat},{lng});
      node["amenity"="cinema"](around:{radius},{lat},{lng});
      
      // Спорт и фитнес
      node["leisure"="sports_centre"](around:{radius},{lat},{lng});
      node["leisure"="fitness_centre"](around:{radius},{lat},{lng});
      node["leisure"="swimming_pool"](around:{radius},{lat},{lng});
    );
    out geom;
    """
    
    try:
        # Отправляем запрос к Overpass API
        url = "https://overpass-api.de/api/interpreter"
        response = requests.post(url, data=overpass_query, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        elements = data.get('elements', [])
        
        # Категорируем POI
        categorized_poi = {
            'medical': [],      # Медицина
            'education': [],    # Образование
            'shopping': [],     # Торговля
            'transport': [],    # Транспорт
            'finance': [],      # Финансы
            'leisure': [],      # Досуг
            'sports': []        # Спорт
        }
        
        for element in elements:
            if element.get('type') != 'node':
                continue
                
            poi_lat = element.get('lat')
            poi_lng = element.get('lon')
            tags = element.get('tags', {})
            
            if not poi_lat or not poi_lng:
                continue
            
            # Рассчитываем расстояние до центра Краснодара
            distance_to_center = haversine_distance(
                poi_lat, poi_lng, 
                KRASNODAR_CENTER[0], KRASNODAR_CENTER[1]
            )
            
            # Рассчитываем расстояние до исходной точки
            distance_to_point = haversine_distance(poi_lat, poi_lng, lat, lng)
            
            # Создаем красивое название для маркера
            name = tags.get('name', '')
            if not name:
                # Формируем название на основе типа объекта
                amenity = tags.get('amenity', '')
                shop = tags.get('shop', '')
                leisure = tags.get('leisure', '')
                highway = tags.get('highway', '')
                
                if amenity == 'hospital':
                    name = 'Больница'
                elif amenity == 'clinic':
                    name = 'Поликлиника'
                elif amenity == 'pharmacy':
                    name = 'Аптека'
                elif amenity == 'school':
                    name = 'Школа'
                elif amenity == 'kindergarten':
                    name = 'Детский сад'
                elif amenity == 'university':
                    name = 'Университет'
                elif amenity == 'bank':
                    name = 'Банк'
                elif amenity == 'atm':
                    name = 'Банкомат'
                elif amenity == 'restaurant':
                    name = 'Ресторан'
                elif amenity == 'cafe':
                    name = 'Кафе'
                elif amenity == 'fuel':
                    name = 'АЗС'
                elif shop == 'supermarket':
                    name = 'Супермаркет'
                elif shop == 'convenience':
                    name = 'Магазин продуктов'
                elif shop == 'bakery':
                    name = 'Пекарня'
                elif shop == 'pharmacy':
                    name = 'Аптека'
                elif shop:
                    name = f'Магазин ({shop})'
                elif leisure == 'park':
                    name = 'Парк'
                elif leisure == 'sports_centre':
                    name = 'Спортивный центр'
                elif highway == 'bus_stop':
                    name = 'Остановка'
                else:
                    name = 'Объект инфраструктуры'
            
            poi_data = {
                'id': element.get('id'),
                'lat': poi_lat,
                'lng': poi_lng,
                'name': name,
                'amenity': tags.get('amenity'),
                'shop': tags.get('shop'),
                'leisure': tags.get('leisure'),
                'highway': tags.get('highway'),
                'railway': tags.get('railway'),
                'distance_to_center': round(distance_to_center, 2),
                'distance_to_point': round(distance_to_point, 2),
                'tags': tags
            }
            
            # Категорируем POI
            amenity = tags.get('amenity', '')
            shop = tags.get('shop', '')
            leisure = tags.get('leisure', '')
            highway = tags.get('highway', '')
            railway = tags.get('railway', '')
            
            if amenity in ['hospital', 'clinic', 'pharmacy', 'doctors']:
                categorized_poi['medical'].append(poi_data)
            elif amenity in ['school', 'kindergarten', 'university', 'college']:
                categorized_poi['education'].append(poi_data)
            elif shop or amenity == 'marketplace':
                categorized_poi['shopping'].append(poi_data)
            elif highway == 'bus_stop' or railway == 'station' or amenity == 'fuel':
                categorized_poi['transport'].append(poi_data)
            elif amenity in ['bank', 'atm']:
                categorized_poi['finance'].append(poi_data)
            elif amenity in ['restaurant', 'cafe', 'cinema'] or leisure == 'park':
                categorized_poi['leisure'].append(poi_data)
            elif leisure in ['sports_centre', 'fitness_centre', 'swimming_pool']:
                categorized_poi['sports'].append(poi_data)
        
        # Сортируем по расстоянию до точки
        for category in categorized_poi:
            categorized_poi[category].sort(key=lambda x: x['distance_to_point'])
            # Ограничиваем количество для производительности
            categorized_poi[category] = categorized_poi[category][:10]
        
        return categorized_poi
        
    except Exception as e:
        print(f"Ошибка получения POI: {e}")
        return {}

def get_infrastructure_summary(lat: float, lng: float) -> Dict:
    """
    Получает краткую сводку инфраструктуры для района/улицы
    """
    poi_data = get_poi_around_coordinates(lat, lng)
    
    summary = {
        'distance_to_center': round(haversine_distance(lat, lng, KRASNODAR_CENTER[0], KRASNODAR_CENTER[1]), 1),
        'medical_count': len(poi_data.get('medical', [])),
        'education_count': len(poi_data.get('education', [])),
        'shopping_count': len(poi_data.get('shopping', [])),
        'transport_count': len(poi_data.get('transport', [])),
        'finance_count': len(poi_data.get('finance', [])),
        'leisure_count': len(poi_data.get('leisure', [])),
        'sports_count': len(poi_data.get('sports', [])),
        'nearest_hospital': None,
        'nearest_school': None,
        'nearest_shop': None
    }
    
    # Находим ближайшие важные объекты
    if poi_data.get('medical'):
        summary['nearest_hospital'] = poi_data['medical'][0]
    
    if poi_data.get('education'):
        summary['nearest_school'] = poi_data['education'][0]
        
    if poi_data.get('shopping'):
        summary['nearest_shop'] = poi_data['shopping'][0]
    
    return summary

if __name__ == "__main__":
    # Тест для центра Краснодара
    test_lat, test_lng = 45.0355, 38.9753
    print("Тестирование системы получения инфраструктуры...")
    
    poi = get_poi_around_coordinates(test_lat, test_lng, 1000)
    summary = get_infrastructure_summary(test_lat, test_lng)
    
    print(f"\\nНайдено POI:")
    for category, items in poi.items():
        print(f"  {category}: {len(items)} объектов")
    
    print(f"\\nКраткая сводка:")
    print(f"  Расстояние до центра: {summary['distance_to_center']} км")
    print(f"  Медицина: {summary['medical_count']}")
    print(f"  Образование: {summary['education_count']}")
    print(f"  Торговля: {summary['shopping_count']}")