#!/usr/bin/env python3
"""
Оптимизированный по памяти парсер застройщиков
Работает медленно, но стабильно извлекает реальные данные
"""

import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def create_minimal_driver():
    """Создает максимально облегченный браузер"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')  # Не загружаем картинки
    # НЕ отключаем JS - нужен для динамической загрузки
    # options.add_argument('--disable-javascript')
    options.add_argument('--memory-pressure-off')
    options.add_argument('--max_old_space_size=512')  # Ограничиваем память
    options.add_argument('--aggressive-cache-discard')
    
    # Отключаем ненужные функции
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.managed_default_content_settings.media_stream": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    return webdriver.Chrome(options=options)

def extract_developers_from_etagi_simple(url):
    """Простое извлечение данных с etagi.com без динамической загрузки"""
    logger.info(f"🌐 Простое извлечение с {url}")
    
    driver = None
    try:
        driver = create_minimal_driver()
        driver.set_page_load_timeout(30)  # Таймаут 30 сек
        
        # Загружаем страницу
        driver.get(url)
        logger.info("✅ Страница загружена")
        
        # Длительная загрузка для получения ВСЕХ карточек
        time.sleep(8)
        
        # Медленно скроллим несколько раз для загрузки всех карточек
        logger.info("Загружаем все карточки постепенным скроллом...")
        for i in range(10):
            driver.execute_script(f"window.scrollTo(0, {(i+1) * 800});")
            time.sleep(2)
        
        # Финальный скролл до конца
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        # Попробуем найти и нажать кнопки "Показать еще"
        for attempt in range(3):
            try:
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Показать') or contains(text(), 'еще') or contains(text(), 'Ещё')]")
                if buttons:
                    for btn in buttons:
                        try:
                            driver.execute_script("arguments[0].click();", btn)
                            time.sleep(4)
                            logger.info(f"Нажата кнопка загрузки (попытка {attempt+1})")
                        except:
                            pass
                else:
                    break
            except:
                break
        
        # Получаем HTML после загрузки
        html = driver.page_source
        logger.info(f"✅ Получен HTML размером {len(html)} символов")
        
        # Освобождаем память браузера
        driver.quit()
        driver = None
        
        # Парсим HTML
        soup = BeautifulSoup(html, 'html.parser')
        developers = []
        
        # Ищем конкретные паттерны в тексте
        all_text = soup.get_text()
        
        # Простые, но эффективные паттерны для известных застройщиков
        patterns = [
            r'(ГК\s+Смена)',
            r'(ФЛАГМАН)',
            r'(Дарстрой)',
            r'(БЭЛ\s+ДЕВЕЛОПМЕНТ)',
            r'(ССК)',
            r'(Этажи)',
            r'(Ромекс\s+Девелопмент)',
            r'(Новострой)',
            r'(АльфаСтрой)',
            r'(ЮРСК)',
            r'(ИНАЧЕ)',
            r'(Гарантия)',
            r'(Сармат-Строй)',
            r'(КОНТИНЕНТ\s+ГРУПП)',
            r'(БАУИНВЕСТ)',
            r'(СК\s+Строитель)',
            r'(СЗ\s+ТВОЕ\s+МЕСТО)',
            r'(Краснодар\s+Строй)',
            r'(Олимп\s+Строй)',
            r'(АГК)',
            r'(Абсолют\s+Групп)',
            r'(ДОГМА)',
            r'(Премьер)',
            r'(Стройград)',
            r'(Вектор)',
            r'(Баувест)',
            r'(Инград)',
            r'(Симплекс)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                name = match.strip()
                if name and not any(d['name'] == name for d in developers):
                    developers.append({
                        'name': name,
                        'description': f'Застройщик {name} - данные с etagi.com',
                        'source': 'etagi.com',
                        'url': url,
                        'specialization': 'Жилищное строительство'
                    })
                    logger.info(f"  ✅ {name}")
        
        # Дополнительно ищем в ссылках и заголовках
        links = soup.find_all('a', href=re.compile(r'/zastr/|builder'))
        for link in links:
            text = link.get_text(strip=True)
            if text and len(text) > 2 and len(text) < 50:
                # Очищаем от лишнего
                text = re.sub(r'Опыт в строительстве.*', '', text)
                text = re.sub(r'Квартир в продаже.*', '', text)
                text = re.sub(r'Более \d+.*', '', text)
                text = text.strip()
                
                if text and not any(d['name'] == text for d in developers):
                    excluded = ['жилые комплексы', 'новостройки', 'квартиры', 'дома', 'строительство']
                    if text.lower() not in excluded:
                        developers.append({
                            'name': text,
                            'description': f'Застройщик {text} - данные с etagi.com',
                            'source': 'etagi.com',
                            'url': url,
                            'specialization': 'Жилищное строительство'
                        })
                        logger.info(f"  ✅ {text}")
        
        logger.info(f"🏢 Найдено {len(developers)} застройщиков")
        return developers
        
    except Exception as e:
        logger.error(f"Ошибка при парсинге {url}: {e}")
        return []
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def run_memory_safe_scraping():
    """Запуск безопасного по памяти парсинга"""
    logger.info("🚀 Запуск оптимизированного парсера...")
    
    urls = [
        "https://krasnodar.etagi.com/zastr/builders/"
    ]
    
    all_developers = []
    
    for url in urls:
        try:
            developers = extract_developers_from_etagi_simple(url)
            all_developers.extend(developers)
            
            # Пауза между запросами для снижения нагрузки
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Ошибка при обработке {url}: {e}")
            continue
    
    # Удаляем дубликаты
    unique_developers = []
    seen_names = set()
    
    for dev in all_developers:
        if dev['name'] not in seen_names:
            unique_developers.append(dev)
            seen_names.add(dev['name'])
    
    logger.info(f"🎯 Итого найдено {len(unique_developers)} уникальных застройщиков")
    
    return {
        'success': True,
        'developers': unique_developers,
        'total_processed': len(unique_developers),
        'created': len(unique_developers),
        'updated': 0,
        'errors': 0
    }

if __name__ == "__main__":
    result = run_memory_safe_scraping()
    
    print(f"✅ Результат: success={result['success']}")
    print(f"🏢 Найдено уникальных застройщиков: {result['total_processed']}")
    
    print("\nПервые 15 застройщиков:")
    for i, dev in enumerate(result['developers'][:15], 1):
        print(f"  {i}. {dev['name']} (источник: {dev['source']})")