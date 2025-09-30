#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РЕАЛЬНЫЙ парсер данных Domclick через inpars.ru API
Получает настоящие данные новостроек Краснодара
"""

import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional

class DomclickRealAPIParser:
    def __init__(self):
        # Используем тестовый токен для демонстрации
        self.api_token = "aEcS9UfAagInparSiv23aoa_vPzxqWvm"
        self.base_url = "https://inpars.ru/api/v2/estate"
        
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'InBack Real Estate Parser 1.0'
        })
        
        self.scraped_data = []
        print("🌐 РЕАЛЬНЫЙ API парсер Domclick инициализирован")
        print(f"📡 Источник: inpars.ru API")
        print(f"🔑 Тестовый режим активен")

    def get_krasnodar_city_id(self) -> Optional[int]:
        """Получение ID города Краснодар"""
        try:
            # Поиск по справочникам не требует оплаты
            cities_url = "https://inpars.ru/api/v2/region"
            response = self.session.get(cities_url, params={'access-token': self.api_token})
            
            if response.status_code == 200:
                data = response.json()
                # Поиск Краснодара в списке городов
                for region in data.get('data', []):
                    if 'krasnodar' in region.get('name', '').lower():
                        print(f"✅ Найден Краснодар: ID {region.get('id')}")
                        return region.get('id')
                        
                # Для демонстрации используем стандартный ID Краснодара
                print("⚠️ Используется стандартный ID Краснодара: 23")
                return 23
            else:
                print(f"❌ Ошибка получения списка городов: {response.status_code}")
                return 23
                
        except Exception as e:
            print(f"❌ Ошибка API городов: {e}")
            return 23

    def fetch_domclick_properties(self, limit: int = 100) -> List[Dict]:
        """Получение реальных данных Domclick через API"""
        try:
            print(f"🔍 Запрос данных Domclick из Краснодара...")
            
            # Параметры для получения новостроек Domclick в Краснодаре
            params = {
                'access-token': self.api_token,
                'sourceId': 22,  # Domclick.ru
                'isNew': 1,      # Только новостройки
                'typeAd': 2,     # Продам
                'limit': limit,
                'sortBy': 'updated_desc'
            }
            
            # Добавляем город если удалось определить
            city_id = self.get_krasnodar_city_id()
            if city_id:
                params['cityId'] = city_id
            
            response = self.session.get(self.base_url, params=params, timeout=30)
            
            print(f"📊 API ответ: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                properties = data.get('data', [])
                meta = data.get('meta', {})
                
                print(f"✅ Получено объектов: {len(properties)}")
                print(f"📈 Общее количество: {meta.get('totalCount', 'неизвестно')}")
                print(f"🚦 Лимит запросов: {meta.get('rateRemaining', 'неизвестно')}/{meta.get('rateLimit', 'неизвестно')}")
                
                return properties
                
            elif response.status_code == 429:
                print("⚠️ Превышен лимит запросов, ожидание...")
                time.sleep(60)
                return []
                
            else:
                print(f"❌ Ошибка API: {response.status_code}")
                print(f"Ответ: {response.text[:500]}")
                return []
                
        except Exception as e:
            print(f"❌ Ошибка получения данных: {e}")
            return []

    def process_property_data(self, properties: List[Dict]) -> List[Dict]:
        """Обработка полученных данных недвижимости"""
        processed = []
        
        print(f"🔄 Обработка {len(properties)} объектов...")
        
        for i, prop in enumerate(properties):
            try:
                # Базовая информация
                property_data = {
                    'inner_id': f"domclick_api_{prop.get('id', int(time.time()))}_{i}",
                    'external_id': str(prop.get('id', '')),
                    'source_url': prop.get('url', ''),
                    'source': 'domclick_api',
                    'scraped_at': datetime.now().isoformat()
                }
                
                # Основные данные
                property_data.update({
                    'price': self.safe_int(prop.get('cost')),
                    'object_area': self.safe_float(prop.get('sq')),
                    'object_rooms': self.safe_int(prop.get('rooms')),
                    'object_min_floor': self.safe_int(prop.get('floor')),
                    'object_max_floor': self.safe_int(prop.get('floors')),
                    'city': 'Краснодар'
                })
                
                # Адрес и местоположение
                address_parts = []
                if prop.get('region'):
                    address_parts.append(prop['region'])
                if prop.get('city'):
                    address_parts.append(prop['city'])
                if prop.get('street'):
                    address_parts.append(prop['street'])
                    
                property_data['address_display_name'] = ', '.join(address_parts) or 'г. Краснодар'
                
                # Координаты
                if prop.get('lat') and prop.get('lng'):
                    property_data['address_position_lat'] = self.safe_float(prop['lat'])
                    property_data['address_position_lon'] = self.safe_float(prop['lng'])
                
                # Дополнительные параметры из params2
                params2 = prop.get('params2', {})
                
                # Информация о доме
                house_info = params2.get('О доме', {})
                property_data.update({
                    'complex_name': house_info.get('Названи новостройки', '').replace('ЖК «', '').replace('»', '') or 'Не указан',
                    'completion_date': house_info.get('Срок сдачи', ''),
                    'building_type': house_info.get('Тип дома', 'Монолит')
                })
                
                # Информация о застройщике
                developer_info = params2.get('О застройщике', {})
                property_data['developer_name'] = (
                    developer_info.get('Группа компаний', '') or
                    developer_info.get('Застройщик', '') or
                    'Уточняется'
                )
                
                # Информация о квартире
                apartment_info = params2.get('О квартире', {})
                if apartment_info.get('Этаж'):
                    floor_info = apartment_info['Этаж']
                    if 'из' in floor_info:
                        parts = floor_info.split('из')
                        if len(parts) == 2:
                            property_data['object_min_floor'] = self.safe_int(parts[0].strip())
                            property_data['object_max_floor'] = self.safe_int(parts[1].strip())
                
                # Статус и тип
                property_data.update({
                    'status': 'В продаже',
                    'property_type': 'квартира',
                    'deal_type': 'Продажа',
                    'region': 'Краснодарский край',
                    'country': 'Россия'
                })
                
                # Расчет цены за м²
                if property_data['price'] and property_data['object_area']:
                    property_data['price_per_sqm'] = int(property_data['price'] / property_data['object_area'])
                
                # Фильтрация валидных объектов
                if (property_data['price'] and property_data['price'] > 500000 and
                    property_data['object_area'] and property_data['object_area'] > 10):
                    processed.append(property_data)
                    
                    if len(processed) <= 3:  # Показываем первые 3 для демонстрации
                        print(f"  {len(processed)}. {property_data['complex_name']} - {property_data['object_rooms']}к, {property_data['object_area']}м², {property_data['price']:,}₽")
                        
            except Exception as e:
                print(f"⚠️ Ошибка обработки объекта {i}: {e}")
                continue
        
        print(f"✅ Обработано валидных объектов: {len(processed)}")
        return processed

    def safe_int(self, value) -> Optional[int]:
        """Безопасное преобразование в int"""
        if not value:
            return None
        try:
            if isinstance(value, str):
                clean_value = ''.join(filter(str.isdigit, value))
                return int(clean_value) if clean_value else None
            return int(value)
        except:
            return None

    def safe_float(self, value) -> Optional[float]:
        """Безопасное преобразование в float"""
        if not value:
            return None
        try:
            if isinstance(value, str):
                clean_value = value.replace(',', '.').replace(' ', '')
                return float(''.join(c for c in clean_value if c.isdigit() or c == '.'))
            return float(value)
        except:
            return None

    def run_parsing(self, max_properties: int = 50) -> Dict:
        """Основной метод парсинга"""
        print("🚀 ЗАПУСК РЕАЛЬНОГО ПАРСИНГА DOMCLICK...")
        print(f"🎯 Цель: получить {max_properties} объектов новостроек")
        print()
        
        try:
            # Получаем данные через API
            properties = self.fetch_domclick_properties(limit=max_properties)
            
            if not properties:
                return {
                    'success': False,
                    'error': 'Не удалось получить данные через API',
                    'properties_count': 0,
                    'properties': []
                }
            
            # Обрабатываем полученные данные
            processed = self.process_property_data(properties)
            
            self.scraped_data = processed
            
            return {
                'success': True,
                'properties_count': len(processed),
                'properties': processed,
                'source': 'domclick_api_inpars'
            }
            
        except Exception as e:
            print(f"❌ Критическая ошибка парсинга: {e}")
            return {
                'success': False,
                'error': str(e),
                'properties_count': 0,
                'properties': []
            }

    def save_to_excel(self, filename: str = None) -> str:
        """Сохранение данных в Excel"""
        if not self.scraped_data:
            print("❌ Нет данных для сохранения")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attached_assets/domclick_real_api_{timestamp}.xlsx"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            df = pd.DataFrame(self.scraped_data)
            df.to_excel(filename, index=False)
            
            print(f"✅ Данные сохранены: {filename}")
            print(f"📊 Объектов в файле: {len(self.scraped_data)}")
            
            # Статистика по данным
            if len(self.scraped_data) > 0:
                df_stats = pd.DataFrame(self.scraped_data)
                print(f"\n📈 СТАТИСТИКА:")
                print(f"   💰 Средняя цена: {df_stats['price'].mean():,.0f} ₽")
                print(f"   📐 Средняя площадь: {df_stats['object_area'].mean():.1f} м²")
                print(f"   🏢 Уникальных ЖК: {df_stats['complex_name'].nunique()}")
                print(f"   🏗️ Уникальных застройщиков: {df_stats['developer_name'].nunique()}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return None

def main():
    """Запуск реального парсера"""
    parser = DomclickRealAPIParser()
    
    try:
        # Запускаем парсинг
        result = parser.run_parsing(max_properties=30)
        
        if result['success']:
            print(f"\n🎉 ПАРСИНГ ЗАВЕРШЕН УСПЕШНО!")
            print(f"📊 Найдено объектов: {result['properties_count']}")
            
            if result['properties_count'] > 0:
                # Сохраняем в Excel
                filename = parser.save_to_excel()
                
                print(f"\n🏘️ ПРИМЕРЫ НАЙДЕННЫХ ЖК:")
                complexes = {}
                for prop in result['properties'][:10]:
                    complex_name = prop.get('complex_name', 'Без названия')
                    if complex_name not in complexes:
                        complexes[complex_name] = []
                    complexes[complex_name].append(prop)
                
                for complex_name, props in list(complexes.items())[:5]:
                    print(f"   🏢 {complex_name}: {len(props)} квартир")
                    dev = props[0].get('developer_name', 'Неизвестно')
                    print(f"      └── Застройщик: {dev}")
                
                return filename
        else:
            print(f"❌ Ошибка парсинга: {result['error']}")
            return None
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    main()