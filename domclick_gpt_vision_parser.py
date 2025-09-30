#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-4 Vision парсер для реальных данных Domclick
Использует искусственный интеллект для обхода защиты и извлечения данных
"""

import os
import json
import base64
import time
import random
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests
from typing import Dict, List, Optional

# Проверяем наличие OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI не установлен. Установите: pip install openai")

class DomclickGPTVisionParser:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key and OPENAI_AVAILABLE:
            self.client = openai.OpenAI(api_key=self.openai_api_key)
            print("✅ OpenAI API подключен")
        else:
            self.client = None
            print("⚠️ OpenAI API ключ не найден")
        
        self.scraped_data = []
        self.base_urls = [
            "https://domclick.ru/krasnodar/search/living/newbuilding",
            "https://domclick.ru/search?type=living&deal_type=sell&object_type%5B%5D=newbuilding&city_id=4897"
        ]
        
        print("🤖 GPT-4 Vision парсер Domclick инициализирован")

    def setup_stealth_browser(self):
        """Настройка браузера с максимальной скрытностью"""
        try:
            with sync_playwright() as p:
                # Случайные параметры браузера
                width = random.randint(1200, 1920)
                height = random.randint(800, 1080)
                
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--disable-blink-features=AutomationControlled',
                        f'--window-size={width},{height}',
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]
                )
                
                context = browser.new_context(
                    viewport={'width': width, 'height': height},
                    locale='ru-RU',
                    timezone_id='Europe/Moscow'
                )
                
                page = context.new_page()
                
                # Удаляем признаки автоматизации
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['ru-RU', 'ru', 'en-US', 'en'],
                    });
                """)
                
                return browser, context, page
                
        except Exception as e:
            print(f"❌ Ошибка запуска браузера: {e}")
            return None, None, None

    def human_like_navigation(self, page, url: str) -> bool:
        """Человекоподобная навигация по сайту"""
        try:
            print(f"🔍 Переход на: {url}")
            
            # Переходим на страницу
            response = page.goto(url, wait_until='networkidle', timeout=30000)
            
            if not response or response.status >= 400:
                print(f"❌ Ошибка загрузки: статус {response.status if response else 'timeout'}")
                return False
            
            # Случайная задержка
            time.sleep(random.uniform(2, 5))
            
            # Проверяем наличие защиты
            page_content = page.content()
            if any(block in page_content.lower() for block in ['access denied', 'blocked', 'captcha', 'challenge']):
                print("⚠️ Обнаружена защита от ботов")
                
                # Пробуем обойти
                page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                time.sleep(random.uniform(1, 3))
                page.mouse.click(random.randint(100, 500), random.randint(100, 500))
                time.sleep(random.uniform(3, 7))
                
                # Проверяем еще раз
                page_content = page.content()
                if any(block in page_content.lower() for block in ['access denied', 'blocked']):
                    print("❌ Не удалось обойти защиту")
                    return False
            
            # Имитация человеческого поведения
            self.simulate_human_behavior(page)
            
            print("✅ Страница успешно загружена")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка навигации: {e}")
            return False

    def simulate_human_behavior(self, page):
        """Имитация поведения человека на странице"""
        try:
            # Скролл страницы
            for _ in range(random.randint(2, 5)):
                scroll_y = random.randint(300, 800)
                page.evaluate(f"window.scrollBy(0, {scroll_y})")
                time.sleep(random.uniform(0.5, 2))
            
            # Случайные движения мыши
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.move(x, y)
                time.sleep(random.uniform(0.2, 1))
                
        except Exception as e:
            print(f"⚠️ Ошибка имитации поведения: {e}")

    def take_smart_screenshot(self, page, selector: str = None) -> Optional[str]:
        """Умный скриншот с фокусом на нужные элементы"""
        try:
            if selector:
                # Скриншот конкретного элемента
                element = page.locator(selector).first
                if element.count() > 0:
                    screenshot_bytes = element.screenshot()
                else:
                    print(f"⚠️ Элемент {selector} не найден, делаем скриншот всей страницы")
                    screenshot_bytes = page.screenshot(full_page=True)
            else:
                # Скриншот всей страницы
                screenshot_bytes = page.screenshot(full_page=True)
            
            # Конвертируем в base64
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            print(f"📸 Скриншот сделан: {len(screenshot_base64)} символов")
            return screenshot_base64
            
        except Exception as e:
            print(f"❌ Ошибка создания скриншота: {e}")
            return None

    def extract_property_data_with_gpt(self, screenshot_base64: str) -> List[Dict]:
        """Извлечение данных недвижимости с помощью GPT-4 Vision"""
        if not self.client:
            print("❌ OpenAI API недоступен")
            return []
        
        try:
            prompt = """
Проанализируй скриншот сайта Domclick с объявлениями о недвижимости в Краснодаре.

Извлеки ВСЕ видимые объекты недвижимости в формате JSON массива:

[
    {
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
        "status": "новостройка/вторичка",
        "year": "год постройки",
        "description": "краткое описание объекта"
    }
]

ВАЖНО:
- Извлекай ТОЛЬКО реальные данные с изображения
- Если данные неясны, пиши null
- Числовые поля должны содержать только цифры
- Ищи карточки объектов, списки, таблицы недвижимости
- Фокусируйся на новостройках для Краснодара
"""

            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4 Vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            print(f"🤖 GPT ответ получен: {len(content)} символов")
            
            # Парсим JSON из ответа
            try:
                # Ищем JSON блок в ответе
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
            print(f"❌ Ошибка GPT Vision: {e}")
            return []

    def process_extracted_data(self, properties: List[Dict]) -> List[Dict]:
        """Обработка и нормализация извлеченных данных"""
        processed = []
        
        for prop in properties:
            try:
                # Очистка и валидация данных
                processed_prop = {
                    'inner_id': f"gpt_vision_{int(time.time())}_{len(processed)}",
                    'complex_name': self.clean_text(prop.get('name', '')),
                    'developer_name': self.clean_text(prop.get('developer', 'Уточняется')),
                    'city': 'Краснодар',
                    'object_rooms': self.safe_int(prop.get('rooms')),
                    'object_area': self.safe_float(prop.get('area')),
                    'price': self.safe_int(prop.get('price')),
                    'object_min_floor': self.safe_int(prop.get('floor')),
                    'object_max_floor': self.safe_int(prop.get('floors_total')),
                    'address_display_name': self.clean_text(prop.get('address', '')),
                    'property_type': prop.get('property_type', 'квартира'),
                    'status': prop.get('status', 'новостройка'),
                    'year_built': self.safe_int(prop.get('year')),
                    'description': self.clean_text(prop.get('description', '')),
                    'source': 'domclick_gpt_vision',
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
            # Удаляем пробелы и нечисловые символы
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

    def run_full_parsing(self) -> Dict:
        """Основной метод парсинга"""
        print("🚀 Запуск полного GPT-4 Vision парсинга...")
        
        all_properties = []
        
        browser, context, page = self.setup_stealth_browser()
        if not browser:
            return {'success': False, 'error': 'Не удалось запустить браузер'}
        
        try:
            for url in self.base_urls:
                print(f"\n🔍 Парсинг: {url}")
                
                if not self.human_like_navigation(page, url):
                    continue
                
                # Ждем загрузки контента
                time.sleep(random.uniform(3, 7))
                
                # Делаем скриншот
                screenshot = self.take_smart_screenshot(page)
                if not screenshot:
                    continue
                
                # Извлекаем данные с помощью GPT-4 Vision
                if self.client:
                    properties = self.extract_property_data_with_gpt(screenshot)
                    if properties:
                        processed = self.process_extracted_data(properties)
                        all_properties.extend(processed)
                        print(f"✅ Добавлено объектов: {len(processed)}")
                else:
                    print("⚠️ OpenAI API недоступен - скриншот сохранен для будущего анализа")
                
                # Пауза между URL
                time.sleep(random.uniform(5, 10))
            
            self.scraped_data = all_properties
            
            return {
                'success': True,
                'properties_count': len(all_properties),
                'properties': all_properties
            }
            
        except Exception as e:
            print(f"❌ Критическая ошибка парсинга: {e}")
            return {'success': False, 'error': str(e)}
            
        finally:
            browser.close()
            print("🔒 Браузер закрыт")

    def save_to_excel(self, filename: str = None) -> str:
        """Сохранение данных в Excel"""
        if not self.scraped_data:
            print("❌ Нет данных для сохранения")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attached_assets/domclick_gpt_vision_{timestamp}.xlsx"
        
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
    """Запуск GPT-4 Vision парсера"""
    parser = DomclickGPTVisionParser()
    
    if not parser.client:
        print("\n⚠️ ВНИМАНИЕ: OpenAI API ключ не настроен")
        print("Парсер может делать скриншоты, но не анализировать их")
        print("Добавьте OPENAI_API_KEY в переменные среды для полной функциональности")
    
    try:
        result = parser.run_full_parsing()
        
        if result['success']:
            print(f"\n🎉 ПАРСИНГ ЗАВЕРШЕН УСПЕШНО!")
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
            print(f"❌ Ошибка парсинга: {result['error']}")
            return None
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    main()