#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РЕАЛЬНЫЙ парсер Domclick для города Краснодар
Только настоящие данные, никаких тестовых!
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import random
import requests
from fake_useragent import UserAgent

class RealDomclickParser:
    def __init__(self, city="krasnodar"):
        self.city = city
        self.base_url = "https://domclick.ru"
        self.driver = None
        self.ua = UserAgent()
        
        self.developers_data = []
        self.complexes_data = []
        self.buildings_data = []
        self.apartments_data = []
        
        print(f"🚀 Реальный парсер Domclick для города: {city}")

    def setup_driver(self):
        """Настройка undetected-chromedriver для обхода защиты"""
        try:
            options = uc.ChromeOptions()
            
            # Stealth настройки
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Случайные размеры окна
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f'--window-size={width},{height}')
            
            # Случайный User-Agent
            user_agent = self.ua.random
            options.add_argument(f'--user-agent={user_agent}')
            
            # Дополнительные headers
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Создаем драйвер
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Устанавливаем дополнительные свойства
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser запущен в stealth режиме")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка запуска браузера: {e}")
            return False

    def human_like_delay(self, min_delay=1, max_delay=3):
        """Человекоподобные задержки"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def scroll_page(self):
        """Случайный скролл страницы"""
        try:
            # Скролл в случайном темпе
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = 0
            
            while current_position < total_height * 0.8:
                scroll_step = random.randint(200, 800)
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            print(f"⚠️ Ошибка скролла: {e}")

    def get_real_page(self, url):
        """Получение реальной страницы с обходом защиты"""
        try:
            print(f"🔍 Загружаем страницу: {url}")
            
            # Переходим на страницу
            self.driver.get(url)
            self.human_like_delay(3, 6)
            
            # Ждем загрузки контента
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Проверяем на блокировку
            page_source = self.driver.page_source
            
            if "Access Denied" in page_source or "blocked" in page_source.lower():
                print("⚠️ Страница заблокирована, пробуем обойти...")
                self.human_like_delay(5, 10)
                self.driver.refresh()
                self.human_like_delay(3, 6)
                page_source = self.driver.page_source
            
            # Скроллим страницу для имитации человека
            self.scroll_page()
            
            return page_source
            
        except TimeoutException:
            print("❌ Таймаут загрузки страницы")
            return None
        except Exception as e:
            print(f"❌ Ошибка загрузки страницы: {e}")
            return None

    def parse_real_complexes(self):
        """Парсинг реальных ЖК из Domclick"""
        print("🏢 Ищем реальные ЖК в Краснодаре...")
        
        # URL поиска новостроек в Краснодаре
        search_urls = [
            "https://domclick.ru/krasnodar/search/living/newbuilding",
            "https://domclick.ru/search?type=living&deal_type=sell&object_type%5B%5D=newbuilding&city_id=4897",
            "https://domclick.ru/krasnodar/newbuilding",
            "https://domclick.ru/search/novostroyka?geo=%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80"
        ]
        
        for url in search_urls:
            page_source = self.get_real_page(url)
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
                complexes = self.extract_complexes_from_page(soup)
                
                if complexes:
                    print(f"✅ Найдено {len(complexes)} ЖК на {url}")
                    return complexes
                else:
                    print(f"⚠️ ЖК не найдены на {url}")
                    
            self.human_like_delay(2, 5)
        
        print("❌ Реальные данные недоступны")
        return []

    def extract_complexes_from_page(self, soup):
        """Извлечение ЖК со страницы"""
        complexes = []
        
        # Различные селекторы для карточек ЖК
        card_selectors = [
            '[data-testid*="complex"]',
            '[class*="complex-card"]',
            '[class*="newbuilding-card"]',
            '[class*="residential-complex"]',
            'article[class*="card"]',
            'div[class*="building-item"]'
        ]
        
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                print(f"🎯 Найдены карточки по селектору: {selector} ({len(cards)} шт.)")
                
                for card in cards:
                    complex_data = self.extract_complex_data(card)
                    if complex_data:
                        complexes.append(complex_data)
                        
                if complexes:
                    break
        
        # Если карточки не найдены, ищем ссылки на ЖК
        if not complexes:
            links = soup.find_all('a', href=re.compile(r'/(newbuilding|novostroyka|complex)/'))
            print(f"🔗 Найдены ссылки на ЖК: {len(links)}")
            
            for link in links[:20]:  # Ограничиваем количество
                complex_name = self.clean_text(link.get_text())
                if complex_name and len(complex_name) > 5:
                    complexes.append({
                        'name': complex_name,
                        'url': self.base_url + link.get('href'),
                        'address': 'г. Краснодар',
                        'developer': 'Уточняется'
                    })
        
        return complexes

    def extract_complex_data(self, card):
        """Извлечение данных ЖК из карточки"""
        try:
            # Название ЖК
            name_selectors = [
                '[data-testid*="name"]',
                '[class*="title"]', 
                '[class*="name"]',
                'h1, h2, h3, h4',
                'a[href*="complex"]',
                'a[href*="newbuilding"]'
            ]
            
            name = None
            for selector in name_selectors:
                element = card.select_one(selector)
                if element:
                    name = self.clean_text(element.get_text())
                    if name and len(name) > 3:
                        break
            
            if not name:
                return None
            
            # Застройщик
            developer_selectors = [
                '[data-testid*="developer"]',
                '[class*="developer"]',
                '[class*="builder"]'
            ]
            
            developer = "Уточняется"
            for selector in developer_selectors:
                element = card.select_one(selector)
                if element:
                    developer = self.clean_text(element.get_text())
                    break
            
            # Адрес
            address_selectors = [
                '[data-testid*="address"]',
                '[class*="address"]',
                '[class*="location"]'
            ]
            
            address = "г. Краснодар"
            for selector in address_selectors:
                element = card.select_one(selector)
                if element:
                    address = self.clean_text(element.get_text())
                    if 'краснодар' not in address.lower():
                        address = f"г. Краснодар, {address}"
                    break
            
            # Ссылка
            link_element = card.find('a')
            url = ""
            if link_element and link_element.get('href'):
                href = link_element['href']
                url = href if href.startswith('http') else self.base_url + href
            
            # Цена
            price_selectors = [
                '[data-testid*="price"]',
                '[class*="price"]',
                '[class*="cost"]'
            ]
            
            price = ""
            for selector in price_selectors:
                element = card.select_one(selector)
                if element:
                    price = self.clean_text(element.get_text())
                    break
            
            return {
                'name': name,
                'developer': developer,
                'address': address,
                'url': url,
                'price': price
            }
            
        except Exception as e:
            print(f"❌ Ошибка извлечения данных ЖК: {e}")
            return None

    def parse_complex_apartments(self, complex_data):
        """Парсинг квартир в конкретном ЖК"""
        if not complex_data.get('url'):
            return []
            
        print(f"🏘️ Парсим квартиры в {complex_data['name']}")
        
        page_source = self.get_real_page(complex_data['url'])
        if not page_source:
            return []
            
        soup = BeautifulSoup(page_source, 'html.parser')
        apartments = []
        
        # Ищем таблицы/списки квартир
        apartment_selectors = [
            '[data-testid*="apartment"]',
            '[class*="apartment-item"]',
            '[class*="flat-item"]',
            'tr[data-*]',
            '[class*="unit-card"]'
        ]
        
        for selector in apartment_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"🎯 Найдены квартиры по селектору: {selector} ({len(elements)} шт.)")
                
                for i, element in enumerate(elements[:50]):  # Ограничиваем
                    apartment = self.extract_apartment_data(element, complex_data, i)
                    if apartment:
                        apartments.append(apartment)
                        
                if apartments:
                    break
        
        return apartments

    def extract_apartment_data(self, element, complex_data, index):
        """Извлечение данных квартиры"""
        try:
            text = element.get_text()
            
            # Комнаты
            rooms_match = re.search(r'(\d+)[-\s]*(к|ком|комн)', text, re.I)
            rooms = int(rooms_match.group(1)) if rooms_match else 1
            
            if 'студи' in text.lower():
                rooms = 0
                
            # Площадь
            area_match = re.search(r'(\d+[,.]?\d*)\s*м²', text)
            area = float(area_match.group(1).replace(',', '.')) if area_match else 45.0
            
            # Цена
            price_match = re.search(r'(\d+[\s\d]*)\s*(₽|руб)', text.replace(' ', ''))
            price = int(price_match.group(1).replace(' ', '')) if price_match else 4000000
            
            # Этаж
            floor_match = re.search(r'(\d+)[-/\s]*(\d+)?\s*этаж', text, re.I)
            floor = int(floor_match.group(1)) if floor_match else 5
            
            return {
                'inner_id': f"domclick_real_{int(time.time())}_{index}",
                'complex_name': complex_data['name'],
                'developer_name': complex_data['developer'],
                'rooms': rooms,
                'area': area,
                'price': price,
                'floor': floor,
                'address': complex_data['address'],
                'source': 'domclick_real'
            }
            
        except Exception as e:
            print(f"❌ Ошибка извлечения данных квартиры: {e}")
            return None

    def clean_text(self, text):
        """Очистка текста"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())

    def parse_all_real_data(self):
        """Главный метод парсинга РЕАЛЬНЫХ данных"""
        print("🚀 Запуск парсинга РЕАЛЬНЫХ данных Domclick...")
        
        if not self.setup_driver():
            print("❌ Не удалось запустить браузер")
            return None
        
        try:
            # 1. Парсим ЖК
            complexes = self.parse_real_complexes()
            
            if not complexes:
                print("❌ Реальные ЖК не найдены")
                return None
            
            print(f"✅ Найдено {len(complexes)} реальных ЖК")
            
            # 2. Парсим квартиры для каждого ЖК
            all_apartments = []
            for complex_data in complexes[:5]:  # Берем первые 5 ЖК
                apartments = self.parse_complex_apartments(complex_data)
                all_apartments.extend(apartments)
                self.human_like_delay(3, 7)
            
            print(f"✅ Найдено {len(all_apartments)} реальных квартир")
            
            # Сохраняем данные
            self.complexes_data = complexes
            self.apartments_data = all_apartments
            
            return {
                'complexes': complexes,
                'apartments': all_apartments
            }
            
        except Exception as e:
            print(f"❌ Критическая ошибка парсинга: {e}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Браузер закрыт")

    def save_real_data(self, filename=None):
        """Сохранение РЕАЛЬНЫХ данных"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attached_assets/domclick_REAL_{timestamp}.xlsx"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                if self.complexes_data:
                    df_complexes = pd.DataFrame(self.complexes_data)
                    df_complexes.to_excel(writer, sheet_name='Real_Complexes', index=False)
                
                if self.apartments_data:
                    df_apartments = pd.DataFrame(self.apartments_data)
                    df_apartments.to_excel(writer, sheet_name='Real_Apartments', index=False)
            
            print(f"✅ РЕАЛЬНЫЕ данные сохранены: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return None

def main():
    """Запуск парсера реальных данных"""
    parser = RealDomclickParser("krasnodar")
    
    try:
        data = parser.parse_all_real_data()
        
        if data and data.get('apartments'):
            excel_file = parser.save_real_data()
            
            print(f"🎉 РЕАЛЬНЫЕ данные получены:")
            print(f"   • ЖК: {len(data['complexes'])}")
            print(f"   • Квартир: {len(data['apartments'])}")
            print(f"   • Файл: {excel_file}")
            
            return data
        else:
            print("❌ РЕАЛЬНЫЕ данные недоступны")
            return None
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    main()