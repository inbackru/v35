"""
ИИ-парсер застройщиков с сайта krasnodar.domclick.ru
Использует OpenAI GPT для извлечения структурированных данных
"""

import os
import json
import time
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

from openai import OpenAI

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DeveloperInfo:
    """Структура данных застройщика"""
    name: str
    url: str
    logo_url: str = ""
    phone: str = ""
    email: str = ""
    description: str = ""
    
    # Статистика
    completed_buildings: int = 0
    under_construction: int = 0
    completed_complexes: int = 0
    construction_complexes: int = 0
    on_time_percentage: int = 0
    
    # Дополнительная информация
    founded_year: int = 0
    experience_years: int = 0
    total_area_built: str = ""
    completed_projects: int = 0
    employees_count: int = 0
    market_position: str = ""
    specialization: str = ""
    
    # Сертификации и проверки
    sber_verified: bool = False
    no_bankruptcy: bool = False
    quarterly_checks: bool = False
    actual_documents: bool = False
    
    # Жилые комплексы
    residential_complexes: List[Dict] = None
    
    # Метаданные
    parsed_at: str = ""
    source_url: str = ""
    
    def __post_init__(self):
        if self.residential_complexes is None:
            self.residential_complexes = []
        if not self.parsed_at:
            self.parsed_at = datetime.now().isoformat()

class AIWebScraper:
    """ИИ-парсер для веб-сайтов с использованием OpenAI GPT"""
    
    def __init__(self):
        self.openai_client = None
        self.driver = None
        self.setup_openai()
        
    def setup_openai(self):
        """Настройка OpenAI клиента"""
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
            logger.info("OpenAI клиент инициализирован")
        else:
            logger.warning("OPENAI_API_KEY не найден")
    
    def setup_selenium(self):
        """Настройка Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # Используем undetected-chromedriver для обхода антиботов
            self.driver = uc.Chrome(options=chrome_options)
            logger.info("Selenium WebDriver инициализирован")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка инициализации WebDriver: {e}")
            # Fallback на обычный requests
            return False
    
    def get_page_content(self, url: str, use_selenium: bool = True) -> str:
        """Получение HTML-контента страницы"""
        try:
            if use_selenium and self.driver:
                self.driver.get(url)
                time.sleep(2)  # Ждем загрузки
                return self.driver.page_source
            else:
                # Fallback на requests
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                return response.text
                
        except Exception as e:
            logger.error(f"Ошибка получения страницы {url}: {e}")
            return ""
    
    def extract_with_ai(self, html_content: str, extraction_schema: Dict) -> Dict:
        """Извлечение данных с помощью OpenAI GPT"""
        if not self.openai_client:
            logger.warning("OpenAI клиент недоступен")
            return {}
        
        try:
            # Очищаем HTML от лишнего для экономии токенов
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Удаляем скрипты, стили, комментарии
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            # Оставляем только текстовый контент с основными тегами
            clean_html = soup.get_text(separator=' ', strip=True)
            
            # Ограничиваем размер для экономии токенов (макс 8000 символов)
            if len(clean_html) > 8000:
                clean_html = clean_html[:8000] + "..."
            
            system_prompt = f"""
Ты эксперт по извлечению структурированных данных с веб-страниц.
Извлеки информацию о застройщике согласно следующей схеме:

{json.dumps(extraction_schema, ensure_ascii=False, indent=2)}

Верни ТОЛЬКО валидный JSON без дополнительных пояснений.
Если какое-то поле не найдено, используй пустую строку "" или 0 для чисел.
Для boolean полей используй true/false.
"""

            user_prompt = f"Извлеки данные из следующего HTML-контента:\n\n{clean_html}"
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # Используем новейшую модель GPT-4o
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1  # Низкая температура для стабильности
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Данные успешно извлечены с помощью ИИ")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка ИИ-извлечения: {e}")
            return {}
    
    def fallback_extraction(self, html_content: str) -> Dict:
        """Fallback извлечение данных без ИИ"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        result = {
            "name": "",
            "phone": "",
            "description": "",
            "completed_buildings": 0,
            "under_construction": 0,
            "on_time_percentage": 0
        }
        
        try:
            # Базовое извлечение с помощью селекторов
            title = soup.find('h1')
            if title:
                result["name"] = title.get_text(strip=True)
            
            # Поиск телефона
            phone_patterns = soup.find_all(text=lambda text: text and '+7' in text)
            if phone_patterns:
                result["phone"] = phone_patterns[0].strip()
            
            # Поиск описания
            description = soup.find('div', class_=['description', 'about'])
            if description:
                result["description"] = description.get_text(strip=True)[:500]
                
        except Exception as e:
            logger.error(f"Ошибка fallback извлечения: {e}")
        
        return result
    
    def close(self):
        """Закрытие ресурсов"""
        if self.driver:
            self.driver.quit()

class DeveloperScraper:
    """Специализированный парсер застройщиков с Domclick"""
    
    def __init__(self):
        self.scraper = AIWebScraper()
        self.base_url = "https://krasnodar.domclick.ru"
        self.developers_url = f"{self.base_url}/zastroishchiki"
        
    def get_developers_list(self) -> List[Dict]:
        """Получение списка всех застройщиков с domclick.ru"""
        logger.info("Получение списка застройщиков с domclick.ru...")
        
        url = "https://krasnodar.domclick.ru/zastroishchiki"
        
        # Пробуем разные методы доступа к сайту
        html_content = None
        
        # Метод 1: Trafilatura (обходит многие защиты)
        try:
            import trafilatura
            logger.info("Пробуем trafilatura...")
            downloaded = trafilatura.fetch_url(url)
            if downloaded and len(downloaded) > 10000:  # Минимальный размер страницы
                html_content = downloaded
                logger.info("✅ Получили контент через trafilatura")
        except Exception as e:
            logger.warning(f"Trafilatura не сработал: {e}")
        
        # Метод 2: Обычный requests с продвинутыми заголовками
        if not html_content:
            try:
                logger.info("Пробуем requests с заголовками...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Cache-Control': 'max-age=0'
                }
                
                response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                logger.info(f"Статус ответа: {response.status_code}")
                
                if response.status_code == 200 and len(response.text) > 10000:
                    html_content = response.text
                    logger.info("✅ Получили контент через requests")
                else:
                    logger.warning(f"Плохой ответ: статус {response.status_code}, размер {len(response.text)}")
                    
            except Exception as e:
                logger.warning(f"Requests не сработал: {e}")
        
        # Метод 3: Selenium как последняя попытка
        if not html_content:
            try:
                logger.info("Пробуем Selenium...")
                if self.scraper.setup_selenium():
                    html_content = self.scraper.get_page_content(url, use_selenium=True)
                    if html_content:
                        logger.info("✅ Получили контент через Selenium")
            except Exception as e:
                logger.warning(f"Selenium не сработал: {e}")
        
        if not html_content:
            logger.error("❌ Все методы получения контента не сработали, используем резервный список")
            return self._get_fallback_developers_data()
        
        logger.info(f"Размер полученного контента: {len(html_content)} символов")
        
        # Извлечение списка застройщиков с помощью ИИ
        schema = {
            "developers": [
                {
                    "name": "string",
                    "url": "string", 
                    "logo_url": "string",
                    "phone": "string",
                    "completed_buildings": "number",
                    "under_construction": "number",
                    "completed_complexes": "number",
                    "construction_complexes": "number", 
                    "on_time_percentage": "number",
                    "founded_year": "number"
                }
            ]
        }
        
        result = self.scraper.extract_with_ai(html_content, schema)
        
        if not result or 'developers' not in result:
            # Fallback парсинг
            result = self.fallback_developers_extraction(html_content)
        
        developers = result.get('developers', [])
        
        # Дополняем URL полными ссылками
        for dev in developers:
            if dev.get('url') and not dev['url'].startswith('http'):
                dev['url'] = urljoin(self.base_url, dev['url'])
        
        logger.info(f"Найдено {len(developers)} застройщиков")
        return developers
    
    def fallback_developers_extraction(self, html_content: str) -> Dict:
        """Fallback извлечение списка застройщиков"""
        soup = BeautifulSoup(html_content, 'html.parser')
        developers = []
        
        try:
            # Поиск таблицы или списка застройщиков
            rows = soup.find_all(['tr', 'div'], class_=lambda x: x and 'developer' in x.lower() if x else False)
            
            for row in rows[:20]:  # Ограничиваем для тестирования
                dev = {
                    "name": "",
                    "url": "",
                    "logo_url": "",
                    "phone": "",
                    "completed_buildings": 0,
                    "under_construction": 0,
                    "on_time_percentage": 0
                }
                
                # Извлечение названия и ссылки
                link = row.find('a')
                if link:
                    dev["name"] = link.get_text(strip=True)
                    dev["url"] = link.get('href', '')
                
                # Извлечение логотипа
                img = row.find('img')
                if img:
                    dev["logo_url"] = img.get('src', '')
                
                # Извлечение телефона
                phone_text = row.get_text()
                if '+7' in phone_text:
                    import re
                    phone_match = re.search(r'\+7[\s\(\)\-\d]+', phone_text)
                    if phone_match:
                        dev["phone"] = phone_match.group().strip()
                
                if dev["name"]:
                    developers.append(dev)
                    
        except Exception as e:
            logger.error(f"Ошибка fallback извлечения: {e}")
        
        return {"developers": developers}
    
    def parse_developer_details(self, developer_url: str) -> DeveloperInfo:
        """Парсинг детальной информации о застройщике"""
        logger.info(f"Парсинг застройщика: {developer_url}")
        
        html_content = self.scraper.get_page_content(developer_url, use_selenium=False)
        
        if not html_content:
            logger.warning(f"Не удалось получить контент для {developer_url}")
            return DeveloperInfo(name="", url=developer_url, source_url=developer_url)
        
        # Схема для детального извлечения
        detailed_schema = {
            "name": "string",
            "phone": "string", 
            "email": "string",
            "description": "string",
            "completed_buildings": "number",
            "under_construction": "number",
            "completed_complexes": "number",
            "construction_complexes": "number",
            "on_time_percentage": "number",
            "founded_year": "number",
            "experience_years": "number",
            "total_area_built": "string",
            "completed_projects": "number",
            "employees_count": "number",
            "market_position": "string",
            "specialization": "string",
            "sber_verified": "boolean",
            "no_bankruptcy": "boolean",
            "quarterly_checks": "boolean",
            "actual_documents": "boolean",
            "residential_complexes": [
                {
                    "name": "string",
                    "url": "string",
                    "price_from": "string",
                    "apartments_count": "number",
                    "address": "string",
                    "class": "string",
                    "rooms_available": ["string"]
                }
            ]
        }
        
        extracted_data = self.scraper.extract_with_ai(html_content, detailed_schema)
        
        if not extracted_data:
            # Fallback извлечение
            extracted_data = self.scraper.fallback_extraction(html_content)
        
        # Создаем объект DeveloperInfo
        developer_info = DeveloperInfo(
            name=extracted_data.get("name", ""),
            url=developer_url,
            source_url=developer_url,
            phone=extracted_data.get("phone", ""),
            email=extracted_data.get("email", ""),
            description=extracted_data.get("description", ""),
            completed_buildings=extracted_data.get("completed_buildings", 0),
            under_construction=extracted_data.get("under_construction", 0),
            completed_complexes=extracted_data.get("completed_complexes", 0),
            construction_complexes=extracted_data.get("construction_complexes", 0),
            on_time_percentage=extracted_data.get("on_time_percentage", 0),
            founded_year=extracted_data.get("founded_year", 0),
            experience_years=extracted_data.get("experience_years", 0),
            total_area_built=extracted_data.get("total_area_built", ""),
            completed_projects=extracted_data.get("completed_projects", 0),
            employees_count=extracted_data.get("employees_count", 0),
            market_position=extracted_data.get("market_position", ""),
            specialization=extracted_data.get("specialization", ""),
            sber_verified=extracted_data.get("sber_verified", False),
            no_bankruptcy=extracted_data.get("no_bankruptcy", False),
            quarterly_checks=extracted_data.get("quarterly_checks", False),
            actual_documents=extracted_data.get("actual_documents", False),
            residential_complexes=extracted_data.get("residential_complexes", [])
        )
        
        logger.info(f"Застройщик '{developer_info.name}' успешно спарсен")
        return developer_info
    
    def parse_all_developers(self, limit: int = 10) -> List[DeveloperInfo]:
        """Парсинг всех застройщиков с ограничением"""
        logger.info(f"Начинаем парсинг застройщиков (лимит: {limit})")
        
        developers_list = self.get_developers_list()
        parsed_developers = []
        
        for i, dev_info in enumerate(developers_list[:limit]):
            try:
                logger.info(f"Парсинг {i+1}/{min(limit, len(developers_list))}: {dev_info.get('name', 'Неизвестно')}")
                
                developer_details = self.parse_developer_details(dev_info['url'])
                
                # Дополняем базовыми данными из списка
                if not developer_details.name and dev_info.get('name'):
                    developer_details.name = dev_info['name']
                if not developer_details.phone and dev_info.get('phone'):
                    developer_details.phone = dev_info['phone']
                if not developer_details.logo_url and dev_info.get('logo_url'):
                    developer_details.logo_url = dev_info['logo_url']
                
                parsed_developers.append(developer_details)
                
                # Пауза между запросами
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Ошибка парсинга застройщика {dev_info.get('name', 'Неизвестно')}: {e}")
                continue
        
        logger.info(f"Парсинг завершен. Успешно спарсено: {len(parsed_developers)} застройщиков")
        return parsed_developers
    
    def save_to_json(self, developers: List[DeveloperInfo], filename: str = "developers_data.json"):
        """Сохранение данных в JSON файл"""
        try:
            data = [asdict(dev) for dev in developers]
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Данные сохранены в {filename}")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения в JSON: {e}")
    
    def close(self):
        """Закрытие ресурсов"""
        self.scraper.close()

def main():
    """Основная функция для тестирования парсера"""
    parser = DeveloperScraper()
    
    try:
        # Парсим первых 5 застройщиков для тестирования
        developers = parser.parse_all_developers(limit=5)
        
        # Сохраняем результаты
        parser.save_to_json(developers, "data/developers_parsed.json")
        
        # Выводим краткую статистику
        print(f"\n=== РЕЗУЛЬТАТЫ ПАРСИНГА ===")
        print(f"Всего спарсено: {len(developers)} застройщиков")
        
        for dev in developers:
            print(f"\n{dev.name}")
            print(f"  - Телефон: {dev.phone}")
            print(f"  - Сдано домов: {dev.completed_buildings}")
            print(f"  - Строится: {dev.under_construction}")
            print(f"  - Процент сдачи в срок: {dev.on_time_percentage}%")
            print(f"  - ЖК: {len(dev.residential_complexes)}")
        
    finally:
        parser.close()

if __name__ == "__main__":
    main()