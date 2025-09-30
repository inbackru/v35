#!/usr/bin/env python3
"""
Продвинутый парсер с Botasaurus для получения реальных данных застройщиков
"""

import logging
import json
import re
import time
from typing import List, Dict
from botasaurus import *

logger = logging.getLogger(__name__)

@browser(
    headless=True,
    block_images=True,
    add_stealth=True,
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    window_size="1920,1080"
)
def scrape_developers_multiple_sources(driver, data):
    """Парсинг застройщиков с нескольких источников"""
    
    sources = [
        'https://krasnodar.etagi.com/zastr/builders/',
        'https://krasnodar.domclick.ru/zastroishchiki',
        'https://krasnodar.cian.ru/developers/',
        'https://novostroyki.su/krasnodar/developers/',
    ]
    
    all_developers = []
    
    for url in sources:
        try:
            logger.info(f"🌐 Пробуем источник: {url}")
            
            # Переходим на страницу
            driver.get(url)
            
            # Ждем загрузки
            driver.wait(5)
            
            # Эмулируем человеческое поведение
            driver.execute_script("window.scrollTo(0, 500);")
            driver.wait(2)
            driver.execute_script("window.scrollTo(0, 1000);")
            driver.wait(2)
            driver.scroll_to_bottom()
            driver.wait(3)
            
            # Кликаем по кнопкам "Показать еще" если есть
            try:
                from selenium.webdriver.common.by import By
                show_more_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Показать') or contains(text(), 'Еще') or contains(text(), 'Загрузить')]")
                for btn in show_more_buttons[:3]:  # Максимум 3 клика
                    try:
                        driver.execute_script("arguments[0].click();", btn)
                        driver.wait(2)
                    except:
                        pass
            except:
                pass
            
            # Получаем HTML
            html = driver.page_source
            logger.info(f"✅ Получен HTML размером {len(html)} символов с {url}")
            
            # Парсим застройщиков
            if 'etagi.com' in url:
                developers = parse_etagi_developers(html, url)
            elif 'domclick.ru' in url:
                developers = parse_domclick_developers(html, url)
            elif 'cian.ru' in url:
                developers = parse_cian_developers(html, url)
            else:
                developers = parse_generic_developers(html, url)
            
            if developers:
                logger.info(f"🏢 Найдено {len(developers)} застройщиков на {url}")
                all_developers.extend(developers)
            else:
                logger.warning(f"❌ Не найдено застройщиков на {url}")
                
        except Exception as e:
            logger.error(f"Ошибка при парсинге {url}: {e}")
            continue
    
    # Убираем дубликаты по названию
    unique_developers = []
    seen_names = set()
    
    for dev in all_developers:
        name_clean = re.sub(r'\s+', ' ', dev['name'].strip().lower())
        if name_clean not in seen_names:
            seen_names.add(name_clean)
            unique_developers.append(dev)
    
    return {
        'success': len(unique_developers) > 0,
        'developers': unique_developers,
        'total_sources': len(sources),
        'successful_sources': len([d for d in all_developers if d]),
        'unique_developers': len(unique_developers)
    }

def parse_etagi_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с etagi.com"""
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем карточки застройщиков на etagi.com
        cards = soup.find_all(['div', 'article'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['developer', 'builder', 'company', 'card', 'item']
        ))
        
        logger.info(f"Найдено {len(cards)} потенциальных карточек на etagi.com")
        
        for card in cards:
            try:
                # Ищем название застройщика
                name_elem = card.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=lambda x: x and any(
                    keyword in str(x).lower() for keyword in ['title', 'name', 'company', 'developer']
                ))
                
                if not name_elem:
                    name_elem = card.find(['h1', 'h2', 'h3', 'h4'])
                
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if name and len(name) > 2 and len(name) < 100:
                        
                        # Ищем дополнительную информацию
                        description = ""
                        stats = card.find(text=re.compile(r'\d+.*(?:проект|дом|квартир)'))
                        if stats:
                            description = stats.strip()
                        
                        # Ищем телефон
                        phone_elem = card.find(text=re.compile(r'\+7\s?\(?\d{3}\)?'))
                        phone = phone_elem.strip() if phone_elem else ''
                        
                        developer_data = {
                            'name': name,
                            'description': description or f'Застройщик {name} - информация с etagi.com',
                            'phone': phone,
                            'source': 'etagi.com',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        }
                        
                        developers.append(developer_data)
                        logger.info(f"  ✅ {name}")
                        
            except Exception as e:
                continue
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга etagi.com: {e}")
        return []

def parse_domclick_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с domclick.ru"""
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем таблицу с застройщиками
        table_rows = soup.find_all('tr')
        
        for row in table_rows:
            try:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:
                    name_text = cells[0].get_text(strip=True)
                    if name_text and len(name_text) > 2 and name_text not in ['Застройщик', 'Название']:
                        
                        completed_text = cells[1].get_text(strip=True) if len(cells) > 1 else '0'
                        under_construction_text = cells[2].get_text(strip=True) if len(cells) > 2 else '0'
                        on_time_text = cells[3].get_text(strip=True) if len(cells) > 3 else '0%'
                        contact_text = cells[4].get_text(strip=True) if len(cells) > 4 else ''
                        
                        # Парсим числа
                        completed_match = re.search(r'(\d+)', completed_text)
                        under_construction_match = re.search(r'(\d+)', under_construction_text)
                        on_time_match = re.search(r'(\d+)', on_time_text)
                        
                        completed_buildings = int(completed_match.group(1)) if completed_match else 0
                        under_construction = int(under_construction_match.group(1)) if under_construction_match else 0
                        on_time_percentage = int(on_time_match.group(1)) if on_time_match else 100
                        
                        phone_match = re.search(r'\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}', contact_text)
                        phone = phone_match.group(0) if phone_match else ''
                        
                        developer_data = {
                            'name': name_text,
                            'completed_buildings': completed_buildings,
                            'under_construction': under_construction,
                            'on_time_percentage': on_time_percentage,
                            'phone': phone,
                            'source': 'domclick.ru',
                            'url': url,
                            'specialization': 'Жилищное строительство',
                            'description': f'Застройщик {name_text} - сдано: {completed_buildings}, строится: {under_construction}, вовремя: {on_time_percentage}%'
                        }
                        
                        developers.append(developer_data)
                        logger.info(f"  ✅ {name_text}")
                        
            except Exception as e:
                continue
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга domclick.ru: {e}")
        return []

def parse_cian_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с cian.ru"""
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем элементы с застройщиками на cian
        cards = soup.find_all(['div', 'article'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['developer', 'company', 'card', 'item']
        ))
        
        for card in cards:
            try:
                name_elem = card.find(['h1', 'h2', 'h3', 'a'])
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    if name and len(name) > 2 and len(name) < 100:
                        
                        # Ищем описание
                        desc_elem = card.find(['p', 'div'], class_=lambda x: x and 'desc' in str(x).lower())
                        description = desc_elem.get_text(strip=True) if desc_elem else f'Застройщик {name} с cian.ru'
                        
                        developer_data = {
                            'name': name,
                            'description': description,
                            'source': 'cian.ru',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        }
                        
                        developers.append(developer_data)
                        logger.info(f"  ✅ {name}")
                        
            except Exception as e:
                continue
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга cian.ru: {e}")
        return []

def parse_generic_developers(html: str, url: str) -> List[Dict]:
    """Универсальный парсинг застройщиков из HTML"""
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем паттерны текста с названиями компаний
        text_content = soup.get_text()
        
        # Продвинутые паттерны для поиска застройщиков
        company_patterns = [
            r'(?:ООО|ОАО|ЗАО|АО|ПАО)\s+["\«]?([А-Я][а-я\-\s]+)["\»]?',
            r'([А-Я][а-я]+(?:\s+[А-Я][а-я]+)*)\s+(?:Строй|Девелопмент|Инвест|Групп|ГК|Холдинг)',
            r'Группа\s+компаний\s+["\«]?([А-Я][а-я\-\s]+)["\»]?',
            r'ГК\s+["\«]?([А-Я][а-я\-\s]+)["\»]?',
            r'Компания\s+["\«]?([А-Я][а-я\-\s]+)["\»]?'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text_content, re.MULTILINE)
            for match in matches:
                name = match.strip() if isinstance(match, str) else match[0].strip()
                if len(name) > 3 and len(name) < 100 and not any(d['name'] == name for d in developers):
                    developers.append({
                        'name': name,
                        'source': f'generic_pattern_{url}',
                        'url': url,
                        'specialization': 'Жилищное строительство',
                        'description': f'Застройщик {name} найден на {url}'
                    })
        
        logger.info(f"Найдено {len(developers)} застройщиков через паттерны")
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка универсального парсинга: {e}")
        return []

def scrape_developers_stable() -> Dict:
    """Стабильная функция для парсинга застройщиков из нескольких источников"""
    try:
        # Запускаем парсинг через Botasaurus
        results = scrape_developers_multiple_sources([{}])
        
        if results and len(results) > 0:
            return results[0]
        else:
            return {
                'success': False,
                'error': 'Нет результатов от парсера',
                'developers': []
            }
            
    except Exception as e:
        logger.error(f"Ошибка стабильного парсинга: {e}")
        return {
            'success': False,
            'error': str(e),
            'developers': []
        }

if __name__ == "__main__":
    # Тест парсера
    print("🧪 Тестирование многоисточникового парсера...")
    
    result = scrape_developers_stable()
    
    print(f"✅ Результат: success={result['success']}")
    if result['success']:
        print(f"🏢 Найдено уникальных застройщиков: {len(result['developers'])}")
        print(f"📊 Успешных источников: {result.get('successful_sources', 0)}")
        print("\nПервые 10 застройщиков:")
        for i, dev in enumerate(result['developers'][:10], 1):
            print(f"  {i}. {dev['name']} (источник: {dev['source']})")
    else:
        print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")