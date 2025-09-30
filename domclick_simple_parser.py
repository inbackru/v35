#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенный парсер Domclick без браузера
Использует HTTP запросы + GPT-4 для анализа HTML
"""

import os
import json
import time
import random
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class DomclickSimpleParser:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key and OPENAI_AVAILABLE:
            self.client = openai.OpenAI(api_key=self.openai_api_key)
            print("✅ OpenAI API подключен")
        else:
            self.client = None
            print("⚠️ OpenAI API ключ не найден")
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.scraped_data = []
        print("🌐 Простой HTTP парсер Domclick инициализирован")

    def get_search_page(self, url: str) -> Optional[str]:
        """Получение HTML страницы поиска"""
        try:
            print(f"🔍 Загрузка: {url}")
            
            # Случайная задержка
            time.sleep(random.uniform(2, 5))
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ Страница загружена: {len(response.text)} символов")
                return response.text
            else:
                print(f"❌ Ошибка HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return None

    def extract_properties_with_gpt(self, html_content: str) -> List[Dict]:
        """Извлечение данных недвижимости с помощью GPT-4"""
        if not self.client:
            print("❌ OpenAI API недоступен")
            return []
        
        try:
            # Обрезаем HTML до разумного размера
            html_snippet = html_content[:15000] if len(html_content) > 15000 else html_content
            
            prompt = f"""
Проанализируй HTML код страницы Domclick с объявлениями о недвижимости в Краснодаре.

Найди ВСЕ объекты недвижимости и извлеки данные в формате JSON массива:

[
    {{
        "name": "название ЖК или адрес объекта",
        "price": "цена в рублях (только число)",
        "rooms": "количество комнат (0 для студии)",
        "area": "площадь в м² (только число)",
        "floor": "этаж",
        "floors_total": "всего этажей в доме",
        "developer": "застройщик или агентство",
        "district": "район Краснодара",
        "address": "полный адрес",
        "property_type": "квартира/дом/коммерческая",
        "status": "новостройка/вторичка"
    }}
]

HTML код:
{html_snippet}

ВАЖНО:
- Извлекай ТОЛЬКО реальные данные из HTML
- Если данные неясны, пиши null
- Числовые поля должны содержать только цифры
- Ищи div с классами card, item, property, apartment, listing
- Фокусируйся на новостройках для Краснодара
"""

            response = self.client.chat.completions.create(
                model="gpt-4",  # Используем GPT-4 вместо Vision
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            print(f"🤖 GPT ответ получен: {len(content)} символов")
            
            # Парсим JSON из ответа
            try:
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    properties = json.loads(json_str)
                    
                    print(f"✅ Извлечено объектов: {len(properties)}")
                    return properties
                else:
                    print("⚠️ JSON не найден в ответе GPT")
                    return []
                    
            except json.JSONDecodeError as e:
                print(f"❌ Ошибка парсинга JSON: {e}")
                print(f"Ответ GPT: {content[:500]}...")
                return []
                
        except Exception as e:
            print(f"❌ Ошибка GPT: {e}")
            return []

    def process_extracted_data(self, properties: List[Dict]) -> List[Dict]:
        """Обработка и нормализация извлеченных данных"""
        processed = []
        
        for prop in properties:
            try:
                processed_prop = {
                    'inner_id': f"simple_parser_{int(time.time())}_{len(processed)}",
                    'complex_name': self.clean_text(prop.get('name', '')),
                    'developer_name': self.clean_text(prop.get('developer', 'Уточняется')),
                    'city': 'Краснодар',
                    'object_rooms': self.safe_int(prop.get('rooms')),
                    'object_area': self.safe_float(prop.get('area')),
                    'price': self.safe_int(prop.get('price')),
                    'object_min_floor': self.safe_int(prop.get('floor')),
                    'object_max_floor': self.safe_int(prop.get('floors_total')),
                    'address_display_name': self.clean_text(prop.get('address', 'г. Краснодар')),
                    'property_type': prop.get('property_type', 'квартира'),
                    'status': prop.get('status', 'новостройка'),
                    'source': 'domclick_simple_parser',
                    'scraped_at': datetime.now().isoformat()
                }
                
                # Базовая валидация
                if processed_prop['price'] and processed_prop['price'] > 100000:
                    processed.append(processed_prop)
                    
            except Exception as e:
                print(f"⚠️ Ошибка обработки объекта: {e}")
                continue
        
        return processed

    def clean_text(self, text) -> str:
        """Очистка текста"""
        if not text or text == 'null':
            return ''
        return str(text).strip()

    def safe_int(self, value) -> Optional[int]:
        """Безопасное преобразование в int"""
        if not value or value == 'null':
            return None
        try:
            clean_value = ''.join(filter(str.isdigit, str(value)))
            return int(clean_value) if clean_value else None
        except:
            return None

    def safe_float(self, value) -> Optional[float]:
        """Безопасное преобразование в float"""
        if not value or value == 'null':
            return None
        try:
            clean_value = str(value).replace(',', '.').replace(' ', '')
            return float(''.join(c for c in clean_value if c.isdigit() or c == '.'))
        except:
            return None

    def run_parsing(self) -> Dict:
        """Основной метод парсинга"""
        print("🚀 Запуск простого парсинга Domclick...")
        
        # URL для парсинга
        search_urls = [
            "https://domclick.ru/krasnodar/search/living/newbuilding",
            "https://domclick.ru/search?type=living&deal_type=sell&object_type%5B%5D=newbuilding&city_id=4897"
        ]
        
        all_properties = []
        
        for url in search_urls:
            try:
                html_content = self.get_search_page(url)
                if not html_content:
                    continue
                
                if self.client:
                    properties = self.extract_properties_with_gpt(html_content)
                    if properties:
                        processed = self.process_extracted_data(properties)
                        all_properties.extend(processed)
                        print(f"✅ Добавлено объектов: {len(processed)}")
                else:
                    print("⚠️ OpenAI API недоступен - HTML получен, но не проанализирован")
                
                # Пауза между запросами
                time.sleep(random.uniform(3, 8))
                
            except Exception as e:
                print(f"❌ Ошибка обработки {url}: {e}")
                continue
        
        self.scraped_data = all_properties
        
        return {
            'success': True if all_properties else False,
            'properties_count': len(all_properties),
            'properties': all_properties
        }

    def save_to_excel(self, filename: str = None) -> str:
        """Сохранение данных в Excel"""
        if not self.scraped_data:
            print("❌ Нет данных для сохранения")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attached_assets/domclick_simple_{timestamp}.xlsx"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            df = pd.DataFrame(self.scraped_data)
            df.to_excel(filename, index=False)
            
            print(f"✅ Данные сохранены: {filename}")
            print(f"📊 Объектов в файле: {len(self.scraped_data)}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return None

def main():
    """Запуск простого парсера"""
    parser = DomclickSimpleParser()
    
    if not parser.client:
        print("\n⚠️ ВНИМАНИЕ: OpenAI API ключ не настроен")
        print("Парсер может получать HTML, но не анализировать его")
        return None
    
    try:
        result = parser.run_parsing()
        
        if result['success']:
            print(f"\n🎉 ПАРСИНГ ЗАВЕРШЕН!")
            print(f"📊 Найдено объектов: {result['properties_count']}")
            
            if result['properties_count'] > 0:
                filename = parser.save_to_excel()
                
                # Показываем примеры данных
                print(f"\n📋 Примеры найденных объектов:")
                for i, prop in enumerate(result['properties'][:3]):
                    print(f"{i+1}. {prop.get('complex_name', 'Без названия')}")
                    print(f"   Цена: {prop.get('price', 'не указана')} ₽")
                    print(f"   Площадь: {prop.get('object_area', 'не указана')} м²")
                    print(f"   Комнат: {prop.get('object_rooms', 'не указано')}")
                
                return filename
        else:
            print("❌ Парсинг не дал результатов")
            return None
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    main()