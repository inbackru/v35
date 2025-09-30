#!/usr/bin/env python3
"""
Простой парсер с использованием Selenium вместо Botasaurus
"""

import logging
import time
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def create_stable_driver():
    """Создает стабильный Selenium драйвер"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)
        return driver
    except Exception as e:
        logger.error(f"Ошибка создания драйвера: {e}")
        return None

def scrape_developers_simple(url: str = None) -> Dict:
    """Простой парсинг застройщиков с domclick.ru"""
    if not url:
        url = 'https://krasnodar.domclick.ru/zastroishchiki'
    
    driver = None
    try:
        logger.info(f"🌐 Открываем {url}")
        
        driver = create_stable_driver()
        if not driver:
            raise Exception("Не удалось создать браузер")
        
        # Переходим на страницу
        driver.get(url)
        
        # Ждем загрузки
        time.sleep(5)
        
        # Простой скролл
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Получаем HTML
        html = driver.page_source
        logger.info(f"✅ Получен HTML размером {len(html)} символов")
        
        # Парсим застройщиков
        developers = parse_developers_from_html_simple(html)
        
        return {
            'success': True,
            'developers': developers,
            'html_size': len(html),
            'url': url
        }
        
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        return {
            'success': False,
            'error': str(e),
            'developers': [],
            'url': url
        }
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("🔻 Браузер закрыт")
            except:
                pass

def parse_developers_from_html_simple(html: str) -> List[Dict]:
    """Простой парсинг застройщиков из HTML"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем таблицу с застройщиками
        table_rows = soup.find_all('tr')
        
        logger.info(f"Найдено {len(table_rows)} строк в HTML")
        
        for row in table_rows:
            try:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:  # Минимум 4 колонки
                    
                    # Извлекаем текст из ячеек
                    name_text = cells[0].get_text(strip=True)
                    completed_text = cells[1].get_text(strip=True) if len(cells) > 1 else '0'
                    under_construction_text = cells[2].get_text(strip=True) if len(cells) > 2 else '0'
                    on_time_text = cells[3].get_text(strip=True) if len(cells) > 3 else '0%'
                    contact_text = cells[4].get_text(strip=True) if len(cells) > 4 else ''
                    
                    # Фильтруем заголовки
                    if name_text and len(name_text) > 2 and name_text not in ['Застройщик', 'Название', 'Компания']:
                        
                        # Парсим числовые данные
                        completed_match = re.search(r'(\d+)', completed_text)
                        under_construction_match = re.search(r'(\d+)', under_construction_text)
                        on_time_match = re.search(r'(\d+)', on_time_text)
                        
                        completed_buildings = int(completed_match.group(1)) if completed_match else 0
                        under_construction = int(under_construction_match.group(1)) if under_construction_match else 0
                        on_time_percentage = int(on_time_match.group(1)) if on_time_match else 100
                        
                        # Извлекаем телефон
                        phone_match = re.search(r'\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}', contact_text)
                        phone = phone_match.group(0) if phone_match else ''
                        
                        developer_data = {
                            'name': name_text,
                            'completed_buildings': completed_buildings,
                            'under_construction': under_construction,
                            'on_time_percentage': on_time_percentage,
                            'phone': phone,
                            'source': 'domclick_simple',
                            'specialization': 'Жилищное строительство',
                            'description': f'Застройщик {name_text} - сдано домов: {completed_buildings}, строится: {under_construction}, вовремя: {on_time_percentage}%'
                        }
                        
                        developers.append(developer_data)
                        logger.info(f"  ✅ {name_text} - сдано: {completed_buildings}, строится: {under_construction}")
                        
            except Exception as e:
                logger.warning(f"Ошибка обработки строки: {e}")
                continue
        
        # Если в таблице ничего не нашли, ищем по тексту
        if not developers:
            logger.info("Поиск по тексту страницы...")
            text_content = soup.get_text()
            
            # Паттерны для поиска названий компаний
            company_patterns = [
                r'[А-Я]{2,}[а-я]*\s*(?:Строй|Девелопмент|Инвест|Групп|ГК)',
                r'ООО\s+["\«]?[А-Я][а-я\s]+["\»]?',
                r'[А-Я][а-я]+\s+[А-Я][а-я]+(?:\s+[А-Я][а-я]+)?'
            ]
            
            for pattern in company_patterns:
                matches = re.findall(pattern, text_content)
                for match in matches:
                    if len(match) > 3 and not any(d['name'] == match.strip() for d in developers):
                        developers.append({
                            'name': match.strip(),
                            'source': 'text_extraction',
                            'specialization': 'Жилищное строительство',
                            'description': f'Застройщик {match} найден в тексте страницы'
                        })
        
        logger.info(f"Итого найдено застройщиков: {len(developers)}")
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга HTML: {e}")
        return []

if __name__ == "__main__":
    # Тест парсера
    print("🧪 Тестирование простого парсера...")
    
    result = scrape_developers_simple()
    
    print(f"✅ Результат: success={result['success']}")
    if result['success']:
        print(f"🏢 Найдено застройщиков: {len(result['developers'])}")
        for dev in result['developers'][:5]:
            print(f"  - {dev['name']}")
    else:
        print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")