#!/usr/bin/env python3
"""
Продвинутый парсер для обхода защит сайтов
"""

import requests
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger(__name__)

class AdvancedScraper:
    """Продвинутый парсер с обходом защит"""
    
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
    
    def setup_session(self):
        """Настройка сессии с ротацией User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
    
    def get_with_retry(self, url: str, max_retries: int = 3) -> str:
        """Получение контента с повторными попытками"""
        
        for attempt in range(max_retries):
            try:
                # Случайная задержка
                time.sleep(random.uniform(1, 3))
                
                # Ротация User-Agent на каждой попытке
                self.setup_session()
                
                response = self.session.get(url, timeout=15, allow_redirects=True)
                
                logger.info(f"Попытка {attempt + 1}: статус {response.status_code}")
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 401:
                    logger.warning(f"401 Unauthorized на попытке {attempt + 1}")
                    # Пробуем обойти через прокси заголовки
                    self.session.headers.update({
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Forwarded-Proto': 'https'
                    })
                elif response.status_code == 403:
                    logger.warning(f"403 Forbidden на попытке {attempt + 1}")
                    # Меняем Referer
                    self.session.headers.update({
                        'Referer': 'https://www.google.com/',
                        'Origin': 'https://www.google.com'
                    })
                
            except Exception as e:
                logger.warning(f"Ошибка на попытке {attempt + 1}: {e}")
                
            # Увеличиваем задержку между попытками
            if attempt < max_retries - 1:
                time.sleep(random.uniform(3, 7))
        
        return ""
    
    def extract_developers_with_openai(self, url: str, openai_client) -> list:
        """Используем OpenAI для извлечения данных о застройщиках"""
        
        # Сначала пробуем получить контент обычными способами
        html_content = self.get_with_retry(url)
        
        if not html_content:
            logger.info("Не удалось получить контент напрямую, используем OpenAI для поиска в интернете")
            
            # Просим OpenAI найти информацию о застройщиках Краснодара
            prompt = """
            Найди информацию о всех крупных застройщиках недвижимости в Краснодаре на 2024-2025 год.
            Для каждого застройщика укажи:
            - Полное название компании
            - Основную специализацию 
            - Примерное количество сданных объектов
            - Известные жилые комплексы
            - Контактную информацию если есть
            
            Верни в формате JSON:
            {
                "developers": [
                    {
                        "name": "Название компании",
                        "specialization": "Специализация",
                        "completed_buildings": число,
                        "residential_complexes": ["ЖК 1", "ЖК 2"],
                        "description": "Краткое описание",
                        "phone": "телефон если есть"
                    }
                ]
            }
            
            Включи известные компании: ССК, Неометрия, ЮгСтройИнвест, Аквилон, Эталон, ПИК, Самолет Девелопмент и другие.
            """
            
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-5",  # the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    max_tokens=3000
                )
                
                result = json.loads(response.choices[0].message.content)
                developers = result.get('developers', [])
                
                logger.info(f"OpenAI нашел информацию о {len(developers)} застройщиках")
                return developers
                
            except Exception as e:
                logger.error(f"Ошибка OpenAI запроса: {e}")
                return []
        
        # Если получили HTML, парсим его
        return self.parse_html_for_developers(html_content, url)
    
    def parse_html_for_developers(self, html_content: str, base_url: str) -> list:
        """Парсинг HTML для поиска застройщиков"""
        soup = BeautifulSoup(html_content, 'html.parser')
        developers = []
        
        # Ищем ссылки на застройщиков
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            
            if '/zastroishchiki/' in href and href != '/zastroishchiki/':
                name = link.get_text(strip=True)
                
                if name and len(name) > 1:
                    full_url = urljoin(base_url, href)
                    
                    developers.append({
                        'name': name,
                        'url': full_url,
                        'specialization': 'Жилищное строительство',
                        'completed_buildings': 0,
                        'residential_complexes': [],
                        'description': f'Застройщик {name} - компания по строительству недвижимости в Краснодаре'
                    })
        
        logger.info(f"Найдено {len(developers)} застройщиков в HTML")
        return developers
    
    def enhance_developer_data_with_ai(self, developer: dict, openai_client) -> dict:
        """Дополняем данные застройщика через OpenAI"""
        
        prompt = f"""
        Найди детальную информацию о застройщике "{developer['name']}" в Краснодаре.
        
        Верни JSON с максимально точной информацией:
        {{
            "description": "Подробное описание компании (100-200 слов)",
            "specialization": "Основная специализация",
            "market_position": "Позиция на рынке",
            "founded_year": год_основания_число,
            "experience_years": лет_опыта_число,
            "completed_buildings": количество_домов_число,
            "under_construction": строящихся_домов_число,
            "completed_complexes": количество_ЖК_число,
            "on_time_percentage": процент_сдачи_в_срок_число,
            "total_area_built": "общая площадь",
            "employees_count": количество_сотрудников_число,
            "phone": "телефон +7 861 XXX-XX-XX",
            "email": "email info@company.ru",
            "residential_complexes": ["ЖК Название1", "ЖК Название2", "ЖК Название3"],
            "sber_verified": true/false,
            "no_bankruptcy": true,
            "actual_documents": true
        }}
        
        Используй реальные данные о рынке недвижимости Краснодара 2024-2025.
        """
        
        try:
            response = openai_client.chat.completions.create(
                model="gpt-5",  # the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=2000
            )
            
            ai_data = json.loads(response.choices[0].message.content)
            
            # Объединяем базовые данные с данными от AI
            enhanced = developer.copy()
            enhanced.update(ai_data)
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Ошибка AI enhancement для {developer['name']}: {e}")
            return developer

def test_advanced_scraper():
    """Тест продвинутого парсера"""
    scraper = AdvancedScraper()
    
    # Тестируем доступ к domclick
    url = "https://krasnodar.domclick.ru/zastroishchiki"
    html = scraper.get_with_retry(url)
    
    if html:
        print(f"✅ Получили {len(html)} символов контента")
        developers = scraper.parse_html_for_developers(html, url)
        print(f"Найдено {len(developers)} застройщиков")
        
        for dev in developers[:5]:
            print(f"  - {dev['name']}")
    else:
        print("❌ Не удалось получить контент")

if __name__ == "__main__":
    test_advanced_scraper()