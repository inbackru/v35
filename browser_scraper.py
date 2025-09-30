#!/usr/bin/env python3
"""
Парсер с эмуляцией браузера для обхода защит Qrator
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import random
import logging
import undetected_chromedriver as uc

logger = logging.getLogger(__name__)

class BrowserScraper:
    """Парсер с эмуляцией настоящего браузера"""
    
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self._setup_browser()
    
    def _setup_browser(self):
        """Настройка браузера с максимальной эмуляцией человека"""
        try:
            # Сначала пробуем обычный Selenium с Chromium
            options = Options()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            # Настройки для работы в контейнере
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--remote-debugging-port=9222')
            
            # Эмуляция обычного браузера
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User-Agent как у настоящего браузера
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Русская локаль
            options.add_argument('--lang=ru-RU')
            options.add_argument('--accept-lang=ru-RU,ru;q=0.9,en;q=0.8')
            
            # Размер окна
            options.add_argument('--window-size=1920,1080')
            
            # Отключаем уведомления
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                }
            }
            options.add_experimental_option("prefs", prefs)
            
            # Пробуем найти chromedriver в системе
            import shutil
            chromedriver_path = shutil.which('chromedriver')
            
            if chromedriver_path:
                from selenium.webdriver.chrome.service import Service
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                # Fallback к обычному Chrome
                self.driver = webdriver.Chrome(options=options)
            
            # Убираем признаки автоматизации
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ Браузер инициализирован успешно")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации браузера: {e}")
            # Пробуем альтернативный способ с undetected-chromedriver
            try:
                logger.info("Пробуем undetected-chromedriver...")
                options = uc.ChromeOptions()
                if self.headless:
                    options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                self.driver = uc.Chrome(options=options, driver_executable_path='/nix/store/*/bin/chromedriver')
                logger.info("✅ Undetected Chrome инициализирован")
            except Exception as e2:
                logger.error(f"Ошибка undetected-chromedriver: {e2}")
                self.driver = None
    
    def get_page_with_browser(self, url: str, wait_time: int = 10) -> str:
        """Получаем страницу через эмулятор браузера"""
        if not self.driver:
            logger.error("Браузер не инициализирован")
            return ""
        
        try:
            logger.info(f"🌐 Открываем {url}")
            
            # Переходим на страницу
            self.driver.get(url)
            
            # Случайная пауза как у человека
            time.sleep(random.uniform(2, 4))
            
            # Ждем загрузки контента
            try:
                # Ждем загрузки основной страницы
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Ждем загрузки динамического контента
                time.sleep(5)  # Даем время на загрузку JS
                
                # Пробуем найти контент связанный с застройщиками
                potential_selectors = [
                    "[data-testid*='developer']",
                    "[class*='developer']", 
                    "[class*='company']",
                    ".card",
                    ".item",
                    "[data-testid*='company']"
                ]
                
                for selector in potential_selectors:
                    try:
                        elements = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                        )
                        if elements:
                            logger.info(f"Найдены элементы по селектору {selector}: {len(elements)}")
                            break
                    except TimeoutException:
                        continue
                        
            except TimeoutException:
                logger.warning("Timeout ожидания загрузки страницы")
            
            # Простой скролл вниз и вверх для загрузки контента
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Ошибка скроллинга: {e}")
            
            # Получаем HTML
            html = self.driver.page_source
            
            logger.info(f"✅ Получено {len(html)} символов HTML")
            return html
            
        except Exception as e:
            logger.error(f"Ошибка получения страницы: {e}")
            return ""
    
    def _human_scroll(self):
        """Эмулируем человеческий скроллинг"""
        try:
            # Получаем высоту страницы
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Скроллим как человек - не сразу вниз, а постепенно
            current_position = 0
            scroll_step = random.randint(300, 600)
            
            while current_position < total_height:
                # Скроллим на случайное расстояние
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                
                # Случайная пауза между скроллами
                time.sleep(random.uniform(0.5, 1.5))
                
                # Иногда скроллим назад, как делают люди
                if random.random() < 0.2:
                    back_scroll = random.randint(50, 200)
                    self.driver.execute_script(f"window.scrollTo(0, {current_position - back_scroll});")
                    time.sleep(random.uniform(0.3, 0.8))
                
                # Новая высота могла измениться (динамическая загрузка)
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                scroll_step = random.randint(300, 600)
            
            # Возвращаемся в начало
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
        except Exception as e:
            logger.warning(f"Ошибка скроллинга: {e}")
    
    def parse_developers_from_html(self, html: str, base_url: str) -> list:
        """Парсим застройщиков из HTML таблицы domclick.ru"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            developers = []
            
            # Ищем таблицу застройщиков на странице domclick.ru
            # Ищем строки таблицы с данными застройщиков
            table_rows = soup.find_all('tr')  # Строки таблицы
            
            # Также пробуем найти div-элементы с информацией о застройщиках
            developer_blocks = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                keyword in str(x).lower() for keyword in ['developer', 'company', 'застройщик', 'item', 'row']
            ))
            
            logger.info(f"Найдено строк таблицы: {len(table_rows)}, блоков застройщиков: {len(developer_blocks)}")
            
            # Парсим строки таблицы
            for row in table_rows:
                try:
                    # Ищем ячейки в строке
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:  # Минимум 4 колонки: название, сданные, строящиеся, %
                        name_cell = cells[0]
                        completed_cell = cells[1] if len(cells) > 1 else None
                        under_construction_cell = cells[2] if len(cells) > 2 else None
                        on_time_cell = cells[3] if len(cells) > 3 else None
                        contact_cell = cells[4] if len(cells) > 4 else None
                        
                        # Извлекаем название
                        name = name_cell.get_text(strip=True)
                        if name and len(name) > 2 and name != 'Застройщик':
                            
                            # Извлекаем данные
                            completed_text = completed_cell.get_text(strip=True) if completed_cell else '0'
                            under_construction_text = under_construction_cell.get_text(strip=True) if under_construction_cell else '0'
                            on_time_text = on_time_cell.get_text(strip=True) if on_time_cell else '0%'
                            contact_text = contact_cell.get_text(strip=True) if contact_cell else ''
                            
                            # Парсим числа
                            import re
                            completed_match = re.search(r'(\d+)', completed_text)
                            under_construction_match = re.search(r'(\d+)', under_construction_text)
                            on_time_match = re.search(r'(\d+)', on_time_text)
                            
                            completed_buildings = int(completed_match.group(1)) if completed_match else 0
                            under_construction = int(under_construction_match.group(1)) if under_construction_match else 0
                            on_time_percentage = int(on_time_match.group(1)) if on_time_match else 0
                            
                            # Извлекаем телефон
                            phone_match = re.search(r'\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}', contact_text)
                            phone = phone_match.group(0) if phone_match else ''
                            
                            developer_data = {
                                'name': name,
                                'completed_buildings': completed_buildings,
                                'under_construction': under_construction,
                                'on_time_percentage': on_time_percentage,
                                'phone': phone,
                                'source': 'domclick_table',
                                'specialization': 'Жилищное строительство',
                                'description': f'Застройщик {name} - сдано домов: {completed_buildings}, строится: {under_construction}, вовремя: {on_time_percentage}%'
                            }
                            
                            developers.append(developer_data)
                            logger.info(f"  ✅ {name} - сдано: {completed_buildings}, строится: {under_construction}")
                
                except Exception as e:
                    logger.warning(f"Ошибка обработки строки таблицы: {e}")
                    continue
            
            # Если не нашли в таблице, пробуем альтернативные методы
            if not developers:
                logger.info("Пробуем альтернативные селекторы...")
                
                # Ищем все элементы с текстом содержащим названия компаний
                import re
                company_patterns = [
                    r'[А-Я]{2,}[а-я]*\s*(?:Строй|Девелопмент|Инвест|Групп|ГК)',
                    r'[А-Я][а-я]+\s+[А-Я][а-я]+',
                    r'ООО\s+["\«]?[А-Я][а-я\s]+["\»]?'
                ]
                
                text_content = soup.get_text()
                for pattern in company_patterns:
                    matches = re.findall(pattern, text_content)
                    for match in matches:
                        if len(match) > 3 and match not in [d['name'] for d in developers]:
                            developers.append({
                                'name': match.strip(),
                                'source': 'text_pattern',
                                'specialization': 'Жилищное строительство',
                                'description': f'Застройщик {match} найден в тексте страницы'
                            })
            
            logger.info(f"Итого найдено застройщиков: {len(developers)}")
            return developers
            
        except Exception as e:
            logger.error(f"Ошибка парсинга HTML: {e}")
            return []
    
    def _extract_developer_name(self, link_element) -> str:
        """Извлекаем название застройщика из элемента ссылки"""
        # Пробуем разные способы получить название
        
        # 1. Текст самой ссылки
        name = link_element.get_text(strip=True)
        if name and len(name) > 2:
            return name
        
        # 2. Атрибут title
        title = link_element.get('title', '').strip()
        if title and len(title) > 2:
            return title
        
        # 3. Атрибут alt у изображения внутри
        img = link_element.find('img')
        if img:
            alt = img.get('alt', '').strip()
            if alt and len(alt) > 2:
                return alt
        
        # 4. Текст в родительском элементе
        parent = link_element.parent
        if parent:
            parent_text = parent.get_text(strip=True)
            if parent_text and len(parent_text) > 2 and len(parent_text) < 100:
                return parent_text
        
        # 5. Из URL
        href = link_element.get('href', '')
        if href:
            parts = href.split('/')
            for part in reversed(parts):
                if part and part != 'zastroishchiki' and len(part) > 2:
                    # Декодируем URL и очищаем
                    import urllib.parse
                    decoded = urllib.parse.unquote(part)
                    cleaned = decoded.replace('-', ' ').replace('_', ' ').title()
                    if len(cleaned) > 2:
                        return cleaned
        
        return ""
    
    def close(self):
        """Закрываем браузер"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🔻 Браузер закрыт")
            except Exception as e:
                logger.warning(f"Ошибка закрытия браузера: {e}")
    
    def __del__(self):
        """Деструктор - закрываем браузер"""
        self.close()

def test_browser_scraper():
    """Тест браузерного парсера"""
    scraper = BrowserScraper(headless=True)
    
    try:
        url = "https://krasnodar.domclick.ru/zastroishchiki"
        html = scraper.get_page_with_browser(url)
        
        if html and len(html) > 1000:
            print(f"✅ Получен HTML размером {len(html)} символов")
            
            # Проверяем наличие признаков блокировки
            if "qrator" in html.lower() or "защита" in html.lower() or "blocked" in html.lower():
                print("❌ Обнаружена блокировка Qrator")
            else:
                print("✅ Блокировка не обнаружена!")
                
                # Парсим застройщиков
                developers = scraper.parse_developers_from_html(html, url)
                print(f"🏢 Найдено застройщиков: {len(developers)}")
                
                for i, dev in enumerate(developers[:5], 1):
                    print(f"  {i}. {dev['name']}")
        else:
            print("❌ Не удалось получить HTML")
            
    finally:
        scraper.close()

if __name__ == "__main__":
    test_browser_scraper()