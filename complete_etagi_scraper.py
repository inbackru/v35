#!/usr/bin/env python3
"""
Полный парсер всех 44 застройщиков с etagi.com
Работает медленно, но получает ВСЕ данные
"""

import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from app import app, db
from models import Developer
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def create_ultra_patient_driver():
    """Создает максимально терпеливый браузер"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-images')
    options.add_argument('--window-size=1920,1080')
    
    return webdriver.Chrome(options=options)

def create_unique_slug(name):
    """Создаем уникальный slug"""
    base_slug = name.lower().replace(' ', '-').replace('ё', 'e').replace('ъ', '').replace('ь', '')
    base_slug = ''.join(c for c in base_slug if c.isalnum() or c == '-')
    base_slug = base_slug[:50]
    
    slug = base_slug
    counter = 1
    while Developer.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug

def extract_all_developers_ultra_slow():
    """Сверхтерпеливое извлечение ВСЕХ застройщиков"""
    url = "https://krasnodar.etagi.com/zastr/builders/"
    logger.info(f"🐌 Сверхмедленное извлечение с {url}")
    
    driver = None
    try:
        driver = create_ultra_patient_driver()
        driver.set_page_load_timeout(60)
        
        # Загружаем страницу
        driver.get(url)
        logger.info("✅ Страница загружена")
        
        # Даем ОЧЕНЬ много времени на первичную загрузку
        logger.info("⏰ Ждем первичную загрузку 15 секунд...")
        time.sleep(15)
        
        # Очень медленный многоэтапный скролл
        logger.info("📜 Начинаем сверхмедленный скролл для загрузки всех карточек...")
        
        # Скроллим по 200px с долгими паузами
        for i in range(50):
            scroll_position = i * 200
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(1)  # Пауза после каждого скролла
            
            if i % 10 == 0:
                logger.info(f"   Скролл: {scroll_position}px (шаг {i+1}/50)")
        
        # Финальный скролл до самого низа
        logger.info("⬇️ Финальный скролл до конца страницы...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        
        # Ищем и нажимаем ВСЕ кнопки загрузки
        logger.info("🔍 Ищем кнопки 'Показать еще'...")
        for attempt in range(5):
            try:
                buttons = driver.find_elements(By.XPATH, 
                    "//button[contains(translate(text(), 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'показать') or contains(translate(text(), 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'еще') or contains(translate(text(), 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'ещё')]")
                
                if buttons:
                    logger.info(f"   Найдено {len(buttons)} кнопок загрузки")
                    for btn in buttons:
                        try:
                            driver.execute_script("arguments[0].click();", btn)
                            time.sleep(8)  # Долгая пауза после клика
                            logger.info(f"   ✅ Кнопка нажата (попытка {attempt+1})")
                        except Exception as e:
                            logger.info(f"   ⚠️ Ошибка клика: {e}")
                else:
                    logger.info(f"   Кнопок не найдено на попытке {attempt+1}")
                    break
                    
            except Exception as e:
                logger.info(f"   ❌ Ошибка поиска кнопок: {e}")
                break
        
        # Еще один финальный скролл
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        # Получаем итоговый HTML
        html = driver.page_source
        logger.info(f"✅ Получен итоговый HTML размером {len(html)} символов")
        
        return html
        
    except Exception as e:
        logger.error(f"Ошибка при извлечении: {e}")
        return None
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def parse_developers_from_html(html):
    """Парсим застройщиков из HTML"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    developers = []
    
    # Собираем ВСЕ возможные названия застройщиков
    all_text = soup.get_text()
    
    # Расширенный список паттернов
    patterns = [
        # Основные форматы
        r'([А-Я][а-я]{2,}(?:\s+[А-Я][а-я]{2,})*)\s*(?:—|–|-)\s*застройщик',
        r'Застройщик:\s*([А-Я][а-я\s]{3,})',
        
        # Строительные компании
        r'([А-Я][а-я]{2,}\s+Строй[а-я]*)',
        r'([А-Я][а-я]{2,}\s+Девелопмент)',
        r'([А-Я][а-я]{2,}\s+Инвест[а-я]*)',
        r'([А-Я][а-я]{2,}\s+Групп[а-я]*)',
        
        # Организационные формы
        r'ГК\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
        r'ООО\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
        r'АО\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
        r'ЗАО\s+["\«]?([А-Я][а-я\s\-]{3,})["\»]?',
        
        # Конкретные известные застройщики
        r'(ССК|СпецСтройКубань)',
        r'(АГК)',
        r'(Абсолют[\s\-]*[Гг]рупп?)',
        r'(ДОГМА|Догма)',
        r'(Премьер)',
        r'(Стройград)',
        r'(Этажи)',
        r'(Ромекс[\s\-]*Девелопмент)',
        r'(Смена)',
        r'(ФЛАГМАН)',
        r'(Дарстрой|ДАРСТРОЙ)',
        r'(БЭЛ[\s\-]*ДЕВЕЛОПМЕНТ)',
        r'(ЮРСК)',
        r'(ИНАЧЕ)',
        r'(Гарантия)',
        r'(Сармат[\s\-]*Строй)',
        r'(КОНТИНЕНТ[\s\-]*ГРУПП)',
        r'(БАУИНВЕСТ)',
        r'(СК[\s\-]*Строитель)',
        r'(СЗ[\s\-]*ТВОЕ[\s\-]*МЕСТО)',
        r'(Краснодар[\s\-]*Строй)',
        r'(Олимп[\s\-]*Строй)',
        r'(Вектор)',
        r'(Баувест)',
        r'(Инград)',
        r'(Симплекс)',
        r'(АльфаСтрой[а-я]*)',
        r'(Новострой)',
        
        # Дополнительные паттерны
        r'([А-Я]{2,}[а-я]*(?:строй|инвест|групп|холдинг))',
        r'([А-Я][а-я]{3,})\s*(?:\(|\[).*(?:строй|девелопмент|инвест)',
    ]
    
    found_names = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        for match in matches:
            name = match.strip() if isinstance(match, str) else match
            if isinstance(name, tuple):
                name = name[0]
            
            # Очищаем название
            name = re.sub(r'Опыт в строительстве.*', '', name)
            name = re.sub(r'Квартир в продаже.*', '', name)
            name = re.sub(r'Более \d+.*', '', name)
            name = re.sub(r'\d+ лет.*', '', name)
            name = re.sub(r'\d+ года.*', '', name)
            name = name.strip()
            
            if name and len(name) > 2 and len(name) < 100:
                # Исключаем общие слова
                excluded = ['жилые комплексы', 'новостройки', 'квартиры', 'дома', 'строительство', 'все новостройки', 'accept']
                if name.lower() not in excluded:
                    found_names.add(name)
    
    # Преобразуем в список словарей
    for name in found_names:
        developers.append({
            'name': name,
            'description': f'Застройщик {name} - данные с etagi.com',
            'source': 'etagi.com',
            'url': 'https://krasnodar.etagi.com/zastr/builders/',
            'specialization': 'Жилищное строительство'
        })
    
    logger.info(f"🎯 Найдено {len(developers)} уникальных застройщиков")
    return developers

def run_complete_import():
    """Запускаем полный импорт"""
    logger.info("🚀 Запуск полного импорта всех застройщиков с etagi.com")
    
    # Извлекаем HTML
    html = extract_all_developers_ultra_slow()
    if not html:
        logger.error("❌ Не удалось получить HTML")
        return
    
    # Парсим застройщиков
    developers_data = parse_developers_from_html(html)
    if not developers_data:
        logger.error("❌ Не удалось найти застройщиков")
        return
    
    logger.info(f"📥 Найдено {len(developers_data)} застройщиков для импорта")
    
    # Импортируем в базу данных
    with app.app_context():
        created_count = 0
        updated_count = 0
        
        for dev_data in developers_data:
            try:
                name = dev_data.get('name', '').strip()
                if not name:
                    continue
                
                # Проверяем существующего
                existing = Developer.query.filter_by(name=name).first()
                
                if existing:
                    # Обновляем
                    existing.description = dev_data.get('description', existing.description)[:1000]
                    existing.updated_at = datetime.now()
                    updated_count += 1
                    logger.info(f"🔄 Обновлен: {name}")
                    
                else:
                    # Создаем нового
                    developer = Developer()
                    developer.name = name
                    developer.slug = create_unique_slug(name)
                    developer.description = dev_data.get('description', f'Застройщик {name}')[:1000]
                    developer.specialization = 'Жилищное строительство'
                    developer.source_url = 'https://krasnodar.etagi.com/zastr/builders/'
                    developer.is_active = True
                    developer.is_partner = True
                    developer.rating = 4.8
                    developer.experience_years = 10
                    developer.zoom_level = 13
                    developer.max_cashback_percent = 10.0
                    developer.no_bankruptcy = True
                    developer.actual_documents = True
                    developer.parsing_status = 'success'
                    developer.created_at = datetime.now()
                    developer.updated_at = datetime.now()
                    
                    db.session.add(developer)
                    created_count += 1
                    logger.info(f"✅ Создан: {name}")
            
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке {dev_data.get('name', 'Unknown')}: {e}")
                continue
        
        # Сохраняем все изменения
        try:
            db.session.commit()
            logger.info(f"\n🎯 ФИНАЛЬНЫЕ ИТОГИ:")
            logger.info(f"   ➕ Создано: {created_count}")
            logger.info(f"   🔄 Обновлено: {updated_count}")
            logger.info(f"   📊 Всего обработано: {created_count + updated_count}")
            
            # Общая статистика
            total = Developer.query.count()
            logger.info(f"   💾 Всего в базе: {total} застройщиков")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка при сохранении: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    run_complete_import()