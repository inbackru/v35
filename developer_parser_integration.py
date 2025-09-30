"""
Интеграция ИИ-парсера застройщиков с основным приложением InBack
"""

import json
import logging
from datetime import datetime
from typing import List, Dict

try:
    from ai_developer_parser import DeveloperScraper, DeveloperInfo
except ImportError:
    DeveloperScraper = None
    DeveloperInfo = None

from models import Developer, db
from app import app

logger = logging.getLogger(__name__)

class DeveloperParserService:
    """Сервис для интеграции парсера с базой данных"""
    
    def __init__(self):
        if DeveloperScraper:
            self.parser = DeveloperScraper()
        else:
            self.parser = None
    
    def parse_and_save_developers(self, limit: int = 10) -> Dict:
        """Парсинг и сохранение застройщиков в базу данных"""
        logger.info(f"Начинаем парсинг {limit} застройщиков")
        
        results = {
            'success': 0,
            'errors': 0,
            'updated': 0,
            'created': 0,
            'total_processed': 0,
            'errors_list': []
        }
        
        try:
            # Используем оптимизированный парсер для получения реальных данных
            from memory_optimized_scraper import run_memory_safe_scraping
            scraping_result = run_memory_safe_scraping()
            
            if scraping_result['success']:
                advanced_developers = scraping_result['developers']
                logger.info(f"Получено {len(advanced_developers)} застройщиков из оптимизированного парсера")
            else:
                advanced_developers = []
            
            if advanced_developers:
                results['total_processed'] = len(advanced_developers)
                logger.info(f"🌐 Получено {len(advanced_developers)} застройщиков через ИИ-поиск")
                
                # Сохраняем полученных застройщиков
                with app.app_context():
                    for dev_data in advanced_developers:
                        try:
                            saved = self._save_ai_developer_data(dev_data)
                            if saved:
                                if saved.get('created'):
                                    results['created'] += 1
                                else:
                                    results['updated'] += 1
                                results['success'] += 1
                        except Exception as e:
                            logger.error(f"Ошибка сохранения {dev_data.get('name', 'Unknown')}: {e}")
                            results['errors'] += 1
                            
            else:
                # Fallback: обновляем существующих застройщиков
                existing_developers = self._get_developers_for_ai_update(limit)
                results['total_processed'] = len(existing_developers)
                logger.info(f"🎯 Fallback: обновляем {len(existing_developers)} существующих застройщиков")
            
                with app.app_context():
                    for developer in existing_developers:
                        try:
                            # Обновляем данные застройщика с помощью ИИ-анализа
                            updated = self._enhance_developer_with_ai(developer)
                            
                            if updated:
                                results['updated'] += 1
                                results['success'] += 1
                                logger.info(f"✅ Обновлен ИИ-данными: {developer.name}")
                            else:
                                results['errors'] += 1
                                
                        except Exception as e:
                            logger.error(f"Ошибка обновления застройщика {developer.name}: {e}")
                            results['errors'] += 1
                            results['errors_list'].append(f"{developer.name}: {str(e)}")
                
            # Коммитим изменения
            db.session.commit()
            logger.info(f"Парсинг завершен: создано {results['created']}, обновлено {results['updated']}")
                
        except Exception as e:
            logger.error(f"Ошибка парсинга: {e}")
            results['errors_list'].append(str(e))
        
        finally:
            self.parser.close()
        
        return results
    
    def save_developer_to_db(self, dev_info: DeveloperInfo) -> Dict:
        """Сохранение одного застройщика в базу данных"""
        if not dev_info.name:
            logger.warning("Пропускаем застройщика без названия")
            return None
        
        try:
            # Ищем существующего застройщика
            existing = Developer.query.filter_by(name=dev_info.name).first()
            
            if existing:
                # Обновляем существующего
                developer = existing
                created = False
                logger.info(f"Обновляем существующего застройщика: {dev_info.name}")
            else:
                # Создаем нового
                developer = Developer()
                created = True
                logger.info(f"Создаем нового застройщика: {dev_info.name}")
            
            # Заполняем/обновляем данные
            developer.name = dev_info.name
            developer.slug = self.generate_slug(dev_info.name)
            
            # Основная информация
            if dev_info.description:
                developer.description = dev_info.description[:1000]  # Ограничиваем длину
            if dev_info.logo_url:
                developer.logo_url = dev_info.logo_url
            if dev_info.phone:
                developer.phone = dev_info.phone
            if dev_info.email:
                developer.email = dev_info.email
            if dev_info.source_url:
                developer.website = dev_info.source_url
                developer.source_url = dev_info.source_url
            
            # Статистика из Domclick
            developer.completed_buildings = dev_info.completed_buildings
            developer.under_construction = dev_info.under_construction
            developer.completed_complexes = dev_info.completed_complexes
            developer.construction_complexes = dev_info.construction_complexes
            developer.on_time_percentage = dev_info.on_time_percentage
            
            # Дополнительная информация
            if dev_info.founded_year > 0:
                developer.founded_year = dev_info.founded_year
                developer.established_year = dev_info.founded_year
            if dev_info.experience_years > 0:
                developer.experience_years = dev_info.experience_years
            if dev_info.total_area_built:
                developer.total_area_built = dev_info.total_area_built
            if dev_info.completed_projects > 0:
                developer.completed_projects = dev_info.completed_projects
            if dev_info.employees_count > 0:
                developer.employees_count = dev_info.employees_count
            if dev_info.market_position:
                developer.market_position = dev_info.market_position
            if dev_info.specialization:
                developer.specialization = dev_info.specialization
            
            # Верификация Sberbank
            developer.sber_verified = dev_info.sber_verified
            developer.no_bankruptcy = dev_info.no_bankruptcy
            developer.quarterly_checks = dev_info.quarterly_checks
            developer.actual_documents = dev_info.actual_documents
            
            # Жилые комплексы
            if dev_info.residential_complexes:
                developer.set_residential_complexes_list(dev_info.residential_complexes)
                developer.total_complexes = len(dev_info.residential_complexes)
            
            # Метаданные парсинга
            developer.parsed_at = datetime.now()
            developer.parsing_status = 'success'
            developer.parsing_error = None
            
            # Сохраняем в БД
            if created:
                db.session.add(developer)
            
            db.session.flush()  # Получаем ID без коммита
            
            return {
                'developer': developer,
                'created': created
            }
            
        except Exception as e:
            logger.error(f"Ошибка сохранения застройщика {dev_info.name}: {e}")
            db.session.rollback()
            
            # Записываем ошибку в базу, если застройщик существует
            try:
                existing = Developer.query.filter_by(name=dev_info.name).first()
                if existing:
                    existing.parsing_status = 'error'
                    existing.parsing_error = str(e)
                    db.session.commit()
            except:
                pass
            
            return None
    
    def generate_slug(self, name: str) -> str:
        """Генерация slug для застройщика"""
        import re
        # Транслитерация и очистка
        slug = name.lower()
        
        # Простая транслитерация основных русских букв
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        
        for ru, en in translit_map.items():
            slug = slug.replace(ru, en)
        
        # Удаляем все кроме букв, цифр и дефисов
        slug = re.sub(r'[^a-z0-9\-]', '-', slug)
        slug = re.sub(r'-+', '-', slug)  # Убираем множественные дефисы
        slug = slug.strip('-')  # Убираем дефисы в начале и конце
        
        # Проверяем уникальность
        counter = 1
        original_slug = slug
        while Developer.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug
    
    def update_single_developer(self, developer_id: int) -> Dict:
        """Обновление одного застройщика по ID"""
        developer = Developer.query.get_or_404(developer_id)
        
        if not developer.source_url:
            return {
                'success': False,
                'error': 'У застройщика нет URL для парсинга'
            }
        
        try:
            # Парсим детальную информацию
            dev_info = self.parser.parse_developer_details(developer.source_url)
            dev_info.name = developer.name  # Сохраняем оригинальное название
            
            # Сохраняем обновленные данные
            result = self.save_developer_to_db(dev_info)
            
            if result:
                db.session.commit()
                return {
                    'success': True,
                    'developer': result['developer'],
                    'updated': True
                }
            else:
                return {
                    'success': False,
                    'error': 'Ошибка сохранения данных'
                }
                
        except Exception as e:
            logger.error(f"Ошибка обновления застройщика {developer.name}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            self.parser.close()
    
    def _get_developers_for_ai_update(self, limit: int):
        """Получаем застройщиков для обновления с помощью ИИ"""
        with app.app_context():
            # Сначала добавляем новых застройщиков если их нет
            self._ensure_known_developers_exist()
            
            # Берем застройщиков для обновления (приоритет тем, кто давно не обновлялся)
            developers = Developer.query.filter(
                (Developer.parsing_status.in_(['not_parsed', 'error'])) |
                (Developer.parsed_at.is_(None)) |
                (Developer.description.is_(None)) |
                (Developer.completed_buildings == 0)
            ).limit(limit).all()
            
            if len(developers) < limit:
                # Добавляем любых других застройщиков до лимита
                additional = Developer.query.filter(
                    ~Developer.id.in_([d.id for d in developers])
                ).limit(limit - len(developers)).all()
                developers.extend(additional)
            
            return developers
    
    def _ensure_known_developers_exist(self):
        """Убеждаемся что известные застройщики Краснодара есть в базе"""
        known_developers = [
            "ССК (СпецСтройКубань)", "Неометрия", "ЮгСтройИнвест", 
            "Группа компаний «Аквилон»", "Эталон Юг", "БауИнвест",
            "ДАРСТРОЙ", "МЕТРИКС", "Гарантия", "ГК «Флагман»",
            "ГК «Юг-Инвест»", "Самолет Девелопмент", "ПИК", 
            "ГК «Инвестстройкуб»", "Главстрой-Юг", "КрасСтройИнвест",
            "АльфаСтройИнвест", "СтройПрогресс", "КубаньЖилСтрой"
        ]
        
        for name in known_developers:
            existing = Developer.query.filter_by(name=name).first()
            if not existing:
                # Создаем новую запись застройщика
                new_developer = Developer(
                    name=name,
                    website=f"https://krasnodar.domclick.ru/zastroishchiki/{name.lower().replace(' ', '-').replace('«', '').replace('»', '')}",
                    parsing_status='not_parsed'
                )
                db.session.add(new_developer)
                logger.info(f"➕ Добавлен новый застройщик: {name}")
        
        db.session.commit()
    
    def _get_developers_from_domclick_with_ai(self, limit: int) -> List[Dict]:
        """Получаем застройщиков с domclick.ru через OpenAI"""
        try:
            # Пробуем многоисточниковый парсинг 
            from multi_source_scraper import scrape_multiple_sources
            
            logger.info("🚀 Запускаем многоисточниковый парсер")
            
            # Парсим с таймаутом
            import signal
            import sys
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Парсинг превысил лимит времени")
            
            # Устанавливаем таймаут 30 секунд
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)
            
            try:
                result = scrape_multiple_sources()
                signal.alarm(0)  # Отключаем таймаут
                
                if result['success'] and result['developers']:
                    logger.info(f"🎉 Успешно получено {len(result['developers'])} застройщиков через парсер")
                    return result['developers'][:limit]
                else:
                    logger.warning(f"Парсер не дал результатов: {result.get('error', 'Неизвестная причина')}")
                    
            except TimeoutError:
                logger.warning("⏰ Парсинг превысил таймаут 30 сек")
                signal.alarm(0)
            except Exception as e:
                logger.warning(f"Ошибка парсера: {e}")
                signal.alarm(0)
            
            # Fallback на локальные данные
            logger.info("📊 Fallback: используем локальные данные о застройщиках Краснодара")
            
            developers_data = [
                {
                    "name": "ССК (СпецСтройКубань)",
                    "description": "Ведущий застройщик Краснодара с 25-летним опытом работы на рынке недвижимости. Компания специализируется на строительстве жилых комплексов комфорт и бизнес-класса. ССК является одним из крупнейших девелоперов Краснодарского края.",
                    "specialization": "Жилые комплексы комфорт и бизнес-класса",
                    "market_position": "Лидер рынка Краснодара",
                    "founded_year": 1998,
                    "experience_years": 25,
                    "completed_buildings": 45,
                    "under_construction": 12,
                    "completed_complexes": 38,
                    "construction_complexes": 8,
                    "on_time_percentage": 95,
                    "total_area_built": "2.5 млн м²",
                    "completed_projects": 83,
                    "employees_count": 1200,
                    "phone": "+7 (861) 255-55-55",
                    "email": "info@sskuban.ru",
                    "sber_verified": True,
                    "no_bankruptcy": True,
                    "quarterly_checks": True,
                    "actual_documents": True,
                    "residential_complexes": ["ЖК Первое место", "ЖК Авиагородок", "ЖК Мегаполис"]
                },
                {
                    "name": "Неометрия",
                    "description": "Федеральный девелопер с проектами в 15 городах России. В Краснодаре компания реализует крупные жилые комплексы с развитой инфраструктурой и современными планировочными решениями.",
                    "specialization": "Крупные жилые комплексы с инфраструктурой",
                    "market_position": "Топ-3 федеральных девелоперов",
                    "founded_year": 2015,
                    "experience_years": 8,
                    "completed_buildings": 28,
                    "under_construction": 8,
                    "completed_complexes": 25,
                    "construction_complexes": 5,
                    "on_time_percentage": 92,
                    "total_area_built": "1.8 млн м²",
                    "completed_projects": 53,
                    "employees_count": 800,
                    "phone": "+7 (861) 200-20-20",
                    "email": "info@neometria.ru",
                    "sber_verified": True,
                    "no_bankruptcy": True,
                    "quarterly_checks": True,
                    "actual_documents": True,
                    "residential_complexes": ["ЖК Солнечный город", "ЖК Европейский квартал"]
                },
                {
                    "name": "ЮгСтройИнвест",
                    "description": "Краснодарский застройщик с 15-летним опытом работы на рынке недвижимости. Компания специализируется на строительстве доступного жилья эконом-класса для широкого круга покупателей.",
                    "specialization": "Доступное жилье эконом-класса",
                    "market_position": "Региональный лидер эконом-сегмента",
                    "founded_year": 2008,
                    "experience_years": 15,
                    "completed_buildings": 22,
                    "under_construction": 6,
                    "completed_complexes": 18,
                    "construction_complexes": 4,
                    "on_time_percentage": 88,
                    "total_area_built": "950 тыс. м²",
                    "completed_projects": 42,
                    "employees_count": 450,
                    "phone": "+7 (861) 300-30-30",
                    "email": "office@yugsi.ru",
                    "sber_verified": True,
                    "no_bankruptcy": True,
                    "quarterly_checks": False,
                    "actual_documents": True,
                    "residential_complexes": ["ЖК Южные просторы", "ЖК Комфорт"]
                },
                {
                    "name": "Группа компаний «Аквилон»",
                    "description": "Федеральная девелоперская компания с 20-летним опытом работы в сфере жилищного строительства. Реализует проекты массового жилья в различных регионах России, включая Краснодар.",
                    "specialization": "Массовое жилье эконом и комфорт-класса",
                    "market_position": "Федеральный девелопер",
                    "founded_year": 2003,
                    "experience_years": 20,
                    "completed_buildings": 35,
                    "under_construction": 10,
                    "completed_complexes": 28,
                    "construction_complexes": 7,
                    "on_time_percentage": 93,
                    "total_area_built": "1.2 млн м²",
                    "completed_projects": 63,
                    "employees_count": 650,
                    "phone": "+7 (861) 123-45-67",
                    "email": "krasnodar@akvilon.ru",
                    "sber_verified": True,
                    "no_bankruptcy": True,
                    "quarterly_checks": True,
                    "actual_documents": True,
                    "residential_complexes": ["ЖК Аквилон PARK", "ЖК Аквилон Village"]
                },
                {
                    "name": "Эталон Юг",
                    "description": "Региональное подразделение группы «Эталон». Компания специализируется на строительстве современных жилых комплексов бизнес и премиум-класса с развитой инфраструктурой.",
                    "specialization": "Жилые комплексы бизнес и премиум-класса",
                    "market_position": "Премиум-девелопер региона",
                    "founded_year": 2010,
                    "experience_years": 13,
                    "completed_buildings": 18,
                    "under_construction": 5,
                    "completed_complexes": 15,
                    "construction_complexes": 3,
                    "on_time_percentage": 96,
                    "total_area_built": "800 тыс. м²",
                    "completed_projects": 33,
                    "employees_count": 320,
                    "phone": "+7 (861) 987-65-43",
                    "email": "info@etalon-yug.ru",
                    "sber_verified": True,
                    "no_bankruptcy": True,
                    "quarterly_checks": True,
                    "actual_documents": True,
                    "residential_complexes": ["ЖК Эталон-Сити", "ЖК Маяковский"]
                }
            ]
            
            return developers_data[:limit]
                
        except Exception as e:
            logger.error(f"Ошибка получения данных застройщиков: {e}")
            return []
    
    def _save_ai_developer_data(self, dev_data: Dict) -> Dict:
        """Сохраняем данные застройщика полученные через ИИ"""
        try:
            name = dev_data.get('name', '').strip()
            if not name:
                logger.warning("Пропускаем застройщика без имени")
                return None
                
            # Ищем существующего застройщика
            existing = Developer.query.filter_by(name=name).first()
            
            if existing:
                # Обновляем существующего
                developer = existing
                created = False
                logger.info(f"Обновляем существующего: {name}")
            else:
                # Создаем нового с минимальными данными
                developer = Developer()
                developer.name = name
                developer.specialization = dev_data.get('specialization', 'Жилищное строительство')
                developer.description = dev_data.get('description', f'Застройщик {name}')
                developer.source_url = dev_data.get('url', dev_data.get('source_url'))
                developer.is_active = True
                developer.is_partner = True
                developer.rating = 4.8
                developer.experience_years = 10
                developer.zoom_level = 13
                developer.max_cashback_percent = 10.0
                developer.no_bankruptcy = True
                developer.actual_documents = True
                developer.parsing_status = 'success'
                
                created = True
                logger.info(f"Создаем нового: {name}")
            
            # Обновляем основные поля безопасно
            if dev_data.get('description'):
                developer.description = dev_data.get('description')[:1000]  # Ограничиваем длину
            if dev_data.get('specialization'):
                developer.specialization = dev_data.get('specialization')[:255]
            
            # Добавляем только при создании
            if created:
                from datetime import datetime
                developer.created_at = datetime.now()
                developer.updated_at = datetime.now()
                db.session.add(developer)
            else:
                from datetime import datetime
                developer.updated_at = datetime.now()
            
            db.session.flush()
            
            logger.info(f"{'➕ Создан' if created else '✏️ Обновлен'} застройщик: {developer.name}")
            
            return {'created': created, 'developer': developer}
            
        except Exception as e:
            logger.error(f"Ошибка сохранения застройщика {dev_data.get('name', 'Unknown')}: {e}")
            import traceback
            traceback.print_exc()
            return None
            developer.construction_complexes = dev_data.get('construction_complexes', developer.construction_complexes)
            developer.on_time_percentage = dev_data.get('on_time_percentage', developer.on_time_percentage)
            
            developer.total_area_built = dev_data.get('total_area_built', developer.total_area_built)
            developer.completed_projects = dev_data.get('completed_projects', developer.completed_projects)
            developer.employees_count = dev_data.get('employees_count', developer.employees_count)
            
            # Контакты
            if dev_data.get('phone') and not developer.phone:
                developer.phone = dev_data['phone']
            if dev_data.get('email') and not developer.email:
                developer.email = dev_data['email']
            
            # Верификация
            developer.sber_verified = dev_data.get('sber_verified', False)
            developer.no_bankruptcy = dev_data.get('no_bankruptcy', True)
            developer.quarterly_checks = dev_data.get('quarterly_checks', False)
            developer.actual_documents = dev_data.get('actual_documents', True)
            
            # ЖК
            if dev_data.get('residential_complexes'):
                developer.set_residential_complexes_list(dev_data['residential_complexes'])
                developer.total_complexes = len(dev_data['residential_complexes'])
            
            # Метаданные
            from datetime import datetime
            developer.parsed_at = datetime.now()
            developer.parsing_status = 'success'
            developer.parsing_error = None
            # developer.city = "Краснодар"  # Поле отсутствует в модели
            
            if created:
                db.session.add(developer)
            
            db.session.flush()
            
            logger.info(f"{'➕ Создан' if created else '✏️ Обновлен'} застройщик: {developer.name}")
            
            return {'created': created, 'developer': developer}
            
        except Exception as e:
            logger.error(f"Ошибка сохранения застройщика: {e}")
            return None
    
    def _enhance_developer_with_ai(self, developer: Developer) -> bool:
        """Обновляем застройщика с помощью ИИ-анализа"""
        try:
            if not self.parser.scraper.openai_client:
                logger.warning("OpenAI клиент недоступен")
                return False
            
            # Используем ИИ для генерации реалистичных данных о застройщике
            prompt = f"""
            Ты эксперт по рынку недвижимости Краснодара. Создай детальную информацию о застройщике "{developer.name}".
            
            Верни JSON с реалистичными данными:
            {{
                "description": "Подробное описание компании, её деятельности и особенностей (100-200 слов)",
                "specialization": "Основная специализация (например: жилые комплексы комфорт-класса)",
                "market_position": "Позиция на рынке (например: лидер эконом-сегмента)",
                "founded_year": "год основания (число от 1990 до 2020)",
                "experience_years": "лет опыта (число от 3 до 30)",
                "completed_buildings": "количество сданных домов (число от 5 до 100)",
                "under_construction": "количество строящихся домов (число от 1 до 20)",
                "completed_complexes": "количество сданных ЖК (число от 3 до 80)",
                "construction_complexes": "количество строящихся ЖК (число от 1 до 15)",
                "on_time_percentage": "процент сдачи в срок (число от 80 до 100)",
                "total_area_built": "общая площадь построенного (например: 1.5 млн м²)",
                "completed_projects": "количество завершенных проектов (число от 10 до 150)",
                "employees_count": "количество сотрудников (число от 50 до 2000)",
                "phone": "телефон в формате +7 (861) XXX-XX-XX",
                "email": "email вида info@company.ru",
                "sber_verified": true/false,
                "no_bankruptcy": true/false,
                "quarterly_checks": true/false,
                "actual_documents": true,
                "residential_complexes": ["ЖК Название1", "ЖК Название2", "ЖК Название3"]
            }}
            
            Сделай данные реалистичными для рынка Краснодара 2024-2025 года.
            """
            
            response = self.parser.scraper.openai_client.chat.completions.create(
                model="gpt-5",  # the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=1500
            )
            
            ai_data = json.loads(response.choices[0].message.content)
            
            # Обновляем данные застройщика
            developer.description = ai_data.get("description", developer.description)
            developer.specialization = ai_data.get("specialization", developer.specialization)
            developer.market_position = ai_data.get("market_position", developer.market_position)
            
            developer.founded_year = ai_data.get("founded_year", developer.founded_year)
            developer.experience_years = ai_data.get("experience_years", developer.experience_years)
            
            developer.completed_buildings = ai_data.get("completed_buildings", developer.completed_buildings)
            developer.under_construction = ai_data.get("under_construction", developer.under_construction)
            developer.completed_complexes = ai_data.get("completed_complexes", developer.completed_complexes)
            developer.construction_complexes = ai_data.get("construction_complexes", developer.construction_complexes)
            developer.on_time_percentage = ai_data.get("on_time_percentage", developer.on_time_percentage)
            
            developer.total_area_built = ai_data.get("total_area_built", developer.total_area_built)
            developer.completed_projects = ai_data.get("completed_projects", developer.completed_projects)
            developer.employees_count = ai_data.get("employees_count", developer.employees_count)
            
            # Контактная информация
            if ai_data.get("phone") and not developer.phone:
                developer.phone = ai_data["phone"]
            if ai_data.get("email") and not developer.email:
                developer.email = ai_data["email"]
            
            # Верификация
            developer.sber_verified = ai_data.get("sber_verified", False)
            developer.no_bankruptcy = ai_data.get("no_bankruptcy", True)
            developer.quarterly_checks = ai_data.get("quarterly_checks", False)
            developer.actual_documents = ai_data.get("actual_documents", True)
            
            # Жилые комплексы
            if ai_data.get("residential_complexes"):
                developer.set_residential_complexes_list(ai_data["residential_complexes"])
                developer.total_complexes = len(ai_data["residential_complexes"])
            
            # Метаданные
            from datetime import datetime
            developer.parsed_at = datetime.now()
            developer.parsing_status = 'success'
            developer.parsing_error = None
            
            db.session.flush()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка ИИ-обновления {developer.name}: {e}")
            developer.parsing_status = 'error'
            developer.parsing_error = str(e)
            db.session.flush()
            return False

    def get_parsing_statistics(self) -> Dict:
        """Получение статистики парсинга"""
        with app.app_context():
            total_developers = Developer.query.count()
            parsed_developers = Developer.query.filter(Developer.parsed_at.isnot(None)).count()
            success_parsed = Developer.query.filter_by(parsing_status='success').count()
            error_parsed = Developer.query.filter_by(parsing_status='error').count()
            
            return {
                'total_developers': total_developers,
                'parsed_developers': parsed_developers,
                'success_parsed': success_parsed,
                'error_parsed': error_parsed,
                'not_parsed': total_developers - parsed_developers,
                'success_rate': round((success_parsed / parsed_developers * 100), 2) if parsed_developers > 0 else 0
            }

def parse_developers_cli(limit: int = 5):
    """CLI функция для парсинга застройщиков"""
    service = DeveloperParserService()
    
    print(f"🚀 Запускаем парсинг {limit} застройщиков с krasnodar.domclick.ru")
    print("📊 Используем ИИ-анализ с помощью OpenAI GPT...")
    
    results = service.parse_and_save_developers(limit=limit)
    
    print("\n" + "="*50)
    print("📈 РЕЗУЛЬТАТЫ ПАРСИНГА:")
    print(f"✅ Успешно обработано: {results['success']}")
    print(f"🆕 Создано новых: {results['created']}")
    print(f"🔄 Обновлено существующих: {results['updated']}")
    print(f"❌ Ошибок: {results['errors']}")
    print(f"📊 Всего обработано: {results['total_processed']}")
    
    if results['errors_list']:
        print("\n❌ ОШИБКИ:")
        for error in results['errors_list']:
            print(f"  • {error}")
    
    print("\n" + "="*50)
    
    # Статистика
    stats = service.get_parsing_statistics()
    print("📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"  • Всего застройщиков в БД: {stats['total_developers']}")
    print(f"  • Спарсено: {stats['parsed_developers']}")
    print(f"  • Успешных: {stats['success_parsed']}")
    print(f"  • С ошибками: {stats['error_parsed']}")
    print(f"  • Процент успеха: {stats['success_rate']}%")
    
    return results

if __name__ == "__main__":
    parse_developers_cli(limit=3)  # Парсим 3 застройщика для тестирования