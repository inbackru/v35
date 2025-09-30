import trafilatura
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List, Optional, Tuple

class KrasnodarDeveloperScraper:
    """
    Парсер застройщиков Краснодара для получения актуальных данных о ЖК и квартирах
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Основные застройщики Краснодара
        self.developers = {
            'ssk': {
                'name': 'ССК (СпецСтройКубань)',
                'website': 'https://sskuban.ru',
                'parser': self.parse_ssk
            },
            'neometria': {
                'name': 'Неометрия',
                'website': 'https://neometria.ru',
                'parser': self.parse_neometria
            },
            'yugstroyinvest': {
                'name': 'ЮгСтройИнвест',
                'website': 'https://yugi.ru',
                'parser': self.parse_yugstroyinvest
            }
        }
    
    def get_website_text_content(self, url: str) -> str:
        """
        Получение текстового содержимого сайта с помощью trafilatura
        """
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                return text or ""
            return ""
        except Exception as e:
            print(f"Ошибка при получении контента с {url}: {e}")
            return ""
    
    def parse_ssk(self) -> List[Dict]:
        """
        Парсинг сайта ССК - sskuban.ru
        """
        print("Парсинг ССК...")
        developer_data = []
        
        try:
            # Главная страница ССК
            main_url = "https://sskuban.ru"
            response = self.session.get(main_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Поиск ЖК на сайте ССК
                projects_links = soup.find_all('a', href=re.compile(r'/projects/|/zhk/|/complex/'))
                
                for link in projects_links[:5]:  # Ограничиваем первыми 5 для теста
                    project_url = urljoin(main_url, link.get('href'))
                    project_name = link.get_text(strip=True)
                    
                    if project_name and len(project_name) > 3:
                        project_data = self.parse_project_details(project_url, project_name, 'ССК')
                        if project_data:
                            developer_data.append(project_data)
                            
        except Exception as e:
            print(f"Ошибка при парсинге ССК: {e}")
        
        return developer_data
    
    def parse_neometria(self) -> List[Dict]:
        """
        Парсинг сайта Неометрия - neometria.ru
        """
        print("Парсинг Неометрия...")
        developer_data = []
        
        try:
            # Страница проектов Неометрии
            projects_url = "https://neometria.ru/projects/"
            response = self.session.get(projects_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Поиск ЖК
                project_cards = soup.find_all(['div', 'section'], class_=re.compile(r'project|complex|card'))
                
                for card in project_cards[:5]:  # Ограничиваем для теста
                    link = card.find('a')
                    if link:
                        project_url = urljoin(projects_url, link.get('href'))
                        project_name = card.get_text(strip=True)[:100]  # Ограничиваем длину
                        
                        if project_name and 'ЖК' in project_name or 'жк' in project_name.lower():
                            project_data = self.parse_project_details(project_url, project_name, 'Неометрия')
                            if project_data:
                                developer_data.append(project_data)
                                
        except Exception as e:
            print(f"Ошибка при парсинге Неометрия: {e}")
        
        return developer_data
    
    def parse_yugstroyinvest(self) -> List[Dict]:
        """
        Парсинг сайта ЮгСтройИнвест - может не быть актуального сайта
        """
        print("Парсинг ЮгСтройИнвест...")
        # Заглушка - может потребоваться найти актуальный сайт
        return []
    
    def parse_project_details(self, url: str, name: str, developer: str) -> Optional[Dict]:
        """
        Детальный парсинг страницы проекта для получения информации о квартирах
        """
        try:
            time.sleep(1)  # Избегаем блокировки
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Извлекаем основную информацию
            project_info = {
                'name': name,
                'developer': developer,
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'apartments': []
            }
            
            # Поиск информации о квартирах
            # Ищем цены
            price_elements = soup.find_all(text=re.compile(r'\d+\s*(?:млн|тыс|руб|\₽)'))
            prices = []
            for price_text in price_elements[:10]:  # Ограничиваем количество
                price_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:млн|тыс)', str(price_text))
                if price_match:
                    price_val = float(price_match.group(1))
                    if 'млн' in str(price_text):
                        price_val *= 1000000
                    elif 'тыс' in str(price_text):
                        price_val *= 1000
                    if 1000000 <= price_val <= 50000000:  # Разумные пределы для Краснодара
                        prices.append(int(price_val))
            
            # Поиск количества комнат
            room_elements = soup.find_all(text=re.compile(r'\d+\s*(?:-к|комн|к\.|room)'))
            rooms = []
            for room_text in room_elements[:10]:
                room_match = re.search(r'(\d+)\s*(?:-к|комн|к\.)', str(room_text))
                if room_match:
                    room_count = int(room_match.group(1))
                    if 0 <= room_count <= 5:  # Разумные пределы
                        rooms.append(room_count)
            
            # Поиск площадей
            area_elements = soup.find_all(text=re.compile(r'\d+(?:\.\d+)?\s*м²'))
            areas = []
            for area_text in area_elements[:10]:
                area_match = re.search(r'(\d+(?:\.\d+)?)\s*м²', str(area_text))
                if area_match:
                    area_val = float(area_match.group(1))
                    if 15 <= area_val <= 300:  # Разумные пределы для квартир
                        areas.append(area_val)
            
            # Создаем записи о квартирах на основе найденных данных
            max_items = max(len(prices), len(rooms), len(areas), 1)
            
            for i in range(min(max_items, 10)):  # Максимум 10 квартир с одной страницы
                apartment = {
                    'complex_name': name,
                    'developer': developer,
                    'price': prices[i] if i < len(prices) else None,
                    'rooms': rooms[i] if i < len(rooms) else None,
                    'area': areas[i] if i < len(areas) else None,
                    'source_url': url,
                    'found_at': datetime.now().isoformat()
                }
                
                # Добавляем только если есть хотя бы какая-то информация
                if apartment['price'] or apartment['rooms'] or apartment['area']:
                    project_info['apartments'].append(apartment)
            
            return project_info if project_info['apartments'] else None
            
        except Exception as e:
            print(f"Ошибка при парсинге проекта {url}: {e}")
            return None
    
    def scrape_all_developers(self) -> Dict[str, List[Dict]]:
        """
        Парсинг всех застройщиков
        """
        all_data = {}
        
        for dev_code, dev_info in self.developers.items():
            print(f"\n{'='*50}")
            print(f"Парсинг застройщика: {dev_info['name']}")
            print(f"{'='*50}")
            
            try:
                data = dev_info['parser']()
                all_data[dev_code] = data
                print(f"Получено {len(data)} проектов от {dev_info['name']}")
                
            except Exception as e:
                print(f"Ошибка при парсинге {dev_info['name']}: {e}")
                all_data[dev_code] = []
            
            time.sleep(2)  # Пауза между застройщиками
        
        return all_data
    
    def save_to_json(self, data: Dict, filename: str = None):
        """
        Сохранение данных в JSON файл
        """
        if filename is None:
            filename = f"scraped_developers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в {filename}")
            return filename
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            return None

def main():
    """
    Основная функция для тестирования парсера
    """
    print("🏗️  Запуск парсера застройщиков Краснодара")
    print("=" * 60)
    
    scraper = KrasnodarDeveloperScraper()
    
    # Парсим всех застройщиков
    all_data = scraper.scrape_all_developers()
    
    # Выводим статистику
    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА ПАРСИНГА")
    print("=" * 60)
    
    total_projects = 0
    total_apartments = 0
    
    for dev_code, projects in all_data.items():
        dev_name = scraper.developers[dev_code]['name']
        project_count = len(projects)
        apartment_count = sum(len(project.get('apartments', [])) for project in projects)
        
        print(f"{dev_name}:")
        print(f"  - Проектов: {project_count}")
        print(f"  - Квартир: {apartment_count}")
        print()
        
        total_projects += project_count
        total_apartments += apartment_count
    
    print(f"ИТОГО:")
    print(f"  - Всего проектов: {total_projects}")
    print(f"  - Всего квартир: {total_apartments}")
    
    # Сохраняем данные
    filename = scraper.save_to_json(all_data)
    
    if filename:
        print(f"✅ Данные успешно собраны и сохранены в {filename}")
    else:
        print("❌ Ошибка при сохранении данных")
    
    return all_data

if __name__ == "__main__":
    main()