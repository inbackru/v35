#!/usr/bin/env python3
"""
Многоисточниковый парсер застройщиков с обычным Selenium
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

def create_stealth_driver():
    """Создает скрытый браузер с защитой от детекции"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        logger.error(f"Ошибка создания драйвера: {e}")
        return None

def scrape_multiple_sources() -> Dict:
    """Парсинг застройщиков с нескольких источников"""
    
    sources = [
        'https://krasnodar.etagi.com/zastr/builders/',
        'https://krasnodar.domclick.ru/zastroishchiki',
        'https://krasnodar.cian.ru/developers/',
        'https://novostroyki.su/krasnodar/developers/',
    ]
    
    all_developers = []
    driver = None
    
    try:
        driver = create_stealth_driver()
        if not driver:
            raise Exception("Не удалось создать браузер")
        
        for url in sources:
            try:
                logger.info(f"🌐 Пробуем источник: {url}")
                
                # Переходим на страницу
                driver.get(url)
                
                # Быстрая загрузка - сократили время ожидания
                time.sleep(3)
                
                # Быстрый скролл для etagi.com
                if 'etagi.com' in url:
                    logger.info("Быстрая обработка etagi.com")
                    
                    # Простой скролл до конца страницы
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    
                    # Попробуем кликнуть кнопку "Показать еще" один раз
                    try:
                        show_more_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Показать') or contains(text(), 'Еще')]")
                        driver.execute_script("arguments[0].click();", show_more_btn)
                        time.sleep(2)
                        logger.info("Нажата кнопка 'Показать еще'")
                    except:
                        pass
                    
                else:
                    # Для других сайтов простой скролл
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                
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
        
    except Exception as e:
        logger.error(f"Общая ошибка парсинга: {e}")
        return {
            'success': False,
            'error': str(e),
            'developers': []
        }
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("🔻 Браузер закрыт")
            except:
                pass

def parse_etagi_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с etagi.com"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Специальная обработка для etagi.com - ищем карточки застройщиков
        
        # Сначала ищем карточки застройщиков по специфичным селекторам
        developer_cards = soup.find_all(['div', 'article', 'section'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['card', 'item', 'developer', 'builder', 'company']
        ))
        
        # Также ищем ссылки на страницы застройщиков
        developer_links = soup.find_all('a', href=re.compile(r'/zastr/|/developer|/builder'))
        
        logger.info(f"Найдено {len(developer_cards)} карточек и {len(developer_links)} ссылок на etagi.com")
        
        # Обрабатываем карточки
        for card in developer_cards:
            try:
                # Ищем название в разных элементах
                name_elem = card.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'], string=re.compile(r'[А-Я][а-я]{2,}'))
                
                if not name_elem:
                    # Ищем по классам
                    name_elem = card.find(['div', 'span'], class_=lambda x: x and any(
                        keyword in str(x).lower() for keyword in ['title', 'name', 'company']
                    ))
                
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    # Тщательно очищаем название от лишнего текста
                    name = re.sub(r'Опыт в строительстве.*', '', name)  # Убираем "Опыт в строительстве..."
                    name = re.sub(r'Квартир в продаже.*', '', name)  # Убираем "Квартир в продаже..."
                    name = re.sub(r'Более \d+.*', '', name)  # Убираем "Более 123..."
                    name = re.sub(r'\d+ лет.*', '', name)  # Убираем "16 лет..."
                    name = re.sub(r'\d+ года.*', '', name)  # Убираем "23 года..."
                    name = re.sub(r'\s*\(.*?\)\s*', '', name)  # Убираем скобки
                    name = re.sub(r'\s*—.*', '', name)  # Убираем после тире
                    name = re.sub(r'\s*-.*', '', name)  # Убираем после дефиса
                    name = name.strip()
                    
                    if len(name) > 2 and len(name) < 100 and not any(d['name'] == name for d in developers):
                        developers.append({
                            'name': name,
                            'description': f'Застройщик {name} - информация с etagi.com',
                            'source': 'etagi.com',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        })
                        logger.info(f"  ✅ {name}")
                        
            except Exception as e:
                continue
        
        # Обрабатываем ссылки
        for link in developer_links:
            try:
                name = link.get_text(strip=True)
                if name and len(name) > 2 and len(name) < 100 and not any(d['name'] == name for d in developers):
                    # Очищаем название
                    name = re.sub(r'Опыт в строительстве.*', '', name)
                    name = re.sub(r'Квартир в продаже.*', '', name)
                    name = re.sub(r'Более \d+.*', '', name)
                    name = re.sub(r'\d+ лет.*', '', name)
                    name = re.sub(r'\d+ года.*', '', name)
                    name = re.sub(r'\s*\(.*?\)\s*', '', name)
                    name = re.sub(r'\s*—.*', '', name)
                    name = re.sub(r'\s*-.*', '', name)
                    name = name.strip()
                    if name:
                        developers.append({
                            'name': name,
                            'description': f'Застройщик {name} - информация с etagi.com',
                            'source': 'etagi.com',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        })
                        logger.info(f"  ✅ {name}")
            except:
                continue
        
        # Дополнительно ищем в тексте
        all_text = soup.get_text()
        
        # Расширенные паттерны для поиска всех застройщиков
        patterns = [
            # Основные паттерны
            r'([А-Я][а-я]+(?:\s+[А-Я][а-я]+)*)\s*[-–—]\s*застройщик',
            r'Застройщик:\s*([А-Я][а-я\s]+)',
            r'([А-Я][а-я]{2,}\s+Строй[а-я]*)',
            r'([А-Я][а-я]{2,}\s+Девелопмент)',
            r'([А-Я][а-я]{2,}\s+Инвест[а-я]*)',
            r'([А-Я][а-я]{2,}\s+Групп[а-я]*)',
            r'ГК\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
            r'ООО\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
            r'([А-Я]{2,}[а-я]*)\s*(?:—|–|-)\s*(?:строительная компания|застройщик)',
            r'Компания\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
            r'([А-Я][а-я]{3,})\s+(?:Холдинг|Траст|Корпорация)',
            # Известные застройщики Краснодара (более точные паттерны)
            r'(ССК)',
            r'(СпецСтройКубань)',
            r'(АГК)',
            r'(Абсолют[\s\-]*[Гг]рупп?)',
            r'(ДОГМА)',
            r'(Догма)',
            r'(Премьер)',
            r'(Стройград)',
            r'(Новая[\s\-]*Сочи)',
            r'(Южный[\s\-]*Дом)',
            r'(Краснодар[\s\-]*Строй)',
            r'(Олимп[\s\-]*Строй)',
            r'(МЖК)',
            r'(Молодежный[\s\-]*жилищный[\s\-]*комплекс)',
            r'(Этажи)',
            r'(Ромекс[\s\-]*Девелопмент)',
            r'(Смена)',
            r'(Альфа[\s\-]*Строй)',
            r'(Вектор)',
            r'(ГИК[\s\-]*ГК)',
            r'(АСК)',
            r'(Баувест)',
            r'(Инград)',
            r'(Симплекс)',
            r'(АльфаСтройИнвест)',
            r'(АРТ[\s\-]*ГРУПП)',
            r'(Альпика[\s\-]*Групп)',
            # Дополнительные общие паттерны
            r'([А-Я][а-я]{2,}(?:строй|инвест|групп|холдинг))',
            r'([А-Я]{2,}[а-я]*)\s*(?:\(|\[).*(?:строй|девелопмент|инвест)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                name = match.strip()
                # Дополнительная очистка для паттернов
                name = re.sub(r'Опыт в строительстве.*', '', name)
                name = re.sub(r'Квартир в продаже.*', '', name)
                name = re.sub(r'Более \d+.*', '', name)
                name = re.sub(r'\d+ лет.*', '', name)
                name = re.sub(r'\d+ года.*', '', name)
                name = name.strip()
                
                if len(name) > 2 and len(name) < 80 and not any(d['name'] == name for d in developers):
                    # Исключаем общие слова
                    excluded_words = ['жилые комплексы', 'новостройки', 'все новостройки', 'квартиры', 'дома']
                    if name.lower() not in excluded_words:
                        developers.append({
                            'name': name,
                            'description': f'Застройщик {name} - информация с etagi.com',
                            'source': 'etagi.com',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        })
                        logger.info(f"  ✅ {name}")
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга etagi.com: {e}")
        return []

def parse_domclick_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с domclick.ru"""
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
        
        # Если таблица не найдена, ищем по тексту
        if not developers:
            all_text = soup.get_text()
            patterns = [
                r'([А-Я][а-я]{2,}\s+Строй[а-я]*)',
                r'([А-Я][а-я]{2,}\s+Девелопмент)',
                r'ГК\s+([А-Я][а-я\s]{3,})',
                r'([А-Я][а-я]{2,}\s+Групп[а-я]*)',
                r'(ССК|СпецСтройКубань)',
                r'(АГК|Абсолют)',
                r'(ДОГМА|Догма)',
                r'(Премьер)',
                r'(Стройград)',
                r'(Краснодар\s*Строй)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, all_text)
                for match in matches:
                    name = match.strip()
                    if len(name) > 2 and len(name) < 80 and not any(d['name'] == name for d in developers):
                        developers.append({
                            'name': name,
                            'source': 'domclick.ru',
                            'url': url,
                            'specialization': 'Жилищное строительство',
                            'description': f'Застройщик {name} с domclick.ru'
                        })
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга domclick.ru: {e}")
        return []

def parse_cian_developers(html: str, url: str) -> List[Dict]:
    """Парсинг застройщиков с cian.ru"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        all_text = soup.get_text()
        
        patterns = [
            r'([А-Я][а-я]+\s+Строй[а-я]*)',
            r'([А-Я][а-я]+\s+Девелопмент)',
            r'([А-Я][а-я]+\s+Инвест[а-я]*)',
            r'ГК\s+([А-Я][а-я\s]+)',
            r'([А-Я][а-я]+\s+Групп[а-я]*)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                name = match.strip()
                if len(name) > 3 and len(name) < 80 and not any(d['name'] == name for d in developers):
                    developers.append({
                        'name': name,
                        'description': f'Застройщик {name} с cian.ru',
                        'source': 'cian.ru',
                        'url': url,
                        'specialization': 'Жилищное строительство'
                    })
                    logger.info(f"  ✅ {name}")
        
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка парсинга cian.ru: {e}")
        return []

def parse_generic_developers(html: str, url: str) -> List[Dict]:
    """Универсальный парсинг застройщиков из HTML"""
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
                        'source': f'generic_{url}',
                        'url': url,
                        'specialization': 'Жилищное строительство',
                        'description': f'Застройщик {name} найден на {url}'
                    })
        
        logger.info(f"Найдено {len(developers)} застройщиков через паттерны")
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка универсального парсинга: {e}")
        return []

if __name__ == "__main__":
    # Тест парсера
    print("🧪 Тестирование многоисточникового парсера...")
    
    result = scrape_multiple_sources()
    
    print(f"✅ Результат: success={result['success']}")
    if result['success']:
        print(f"🏢 Найдено уникальных застройщиков: {len(result['developers'])}")
        print(f"📊 Успешных источников: {result.get('successful_sources', 0)}")
        print("\nПервые 15 застройщиков:")
        for i, dev in enumerate(result['developers'][:15], 1):
            print(f"  {i}. {dev['name']} (источник: {dev['source']})")
    else:
        print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")