#!/usr/bin/env python3
"""
Интеграция парсера застройщиков с системой InBack
Обновляет базу данных актуальными данными о ЖК и квартирах
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from web_scraper import KrasnodarDeveloperScraper

# Database integration
try:
    from app import app, db
    from models import Developer, ResidentialComplex, District
except ImportError as e:
    print(f"⚠️  Ошибка импорта моделей: {e}")
    app, db = None, None

class PropertyScraperIntegration:
    """
    Класс для интеграции данных парсера с базой данных InBack
    """
    
    def __init__(self):
        self.scraper = KrasnodarDeveloperScraper()
        
        # Маппинг районов Краснодара (можно расширить)
        self.district_mapping = {
            'центральный': 'Центральный район',
            'западный': 'Западный район', 
            'карасунский': 'Карасунский округ',
            'прикубанский': 'Прикубанский округ',
            'первомайский': 'Первомайский округ',
            'комсомольский': 'Октябрьский округ',
        }
    
    def create_property_model_if_missing(self):
        """
        Создает модель Property если её нет
        """
        if not db:
            print("❌ База данных недоступна")
            return False
            
        try:
            with app.app_context():
                # Проверяем, есть ли таблица properties
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                
                if 'properties' not in inspector.get_table_names():
                    print("🏗️  Создание модели Property...")
                    
                    # Добавляем модель Property в models.py
                    property_model_code = '''

class Property(db.Model):
    """Property/Apartment model for real estate listings"""
    __tablename__ = 'properties'
    __table_args__ = {"extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic property information
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    # Property details
    rooms = db.Column(db.Integer, nullable=True)  # Количество комнат (0 для студии)
    area = db.Column(db.Float, nullable=True)  # Площадь в м²
    floor = db.Column(db.Integer, nullable=True)  # Этаж
    total_floors = db.Column(db.Integer, nullable=True)  # Всего этажей в доме
    
    # Pricing
    price = db.Column(db.Integer, nullable=True)  # Цена в рублях
    price_per_sqm = db.Column(db.Integer, nullable=True)  # Цена за м²
    
    # Location and relations
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'), nullable=True)
    complex_id = db.Column(db.Integer, db.ForeignKey('residential_complexes.id'), nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=True)
    
    # Status and availability
    status = db.Column(db.String(50), default='available')  # available, sold, reserved
    is_active = db.Column(db.Boolean, default=True)
    
    # Images and media
    main_image = db.Column(db.String(300), nullable=True)
    gallery_images = db.Column(db.Text, nullable=True)  # JSON array of image URLs
    
    # Technical details
    building_type = db.Column(db.String(100), nullable=True)  # монолит, кирпич, панель
    ceiling_height = db.Column(db.Float, nullable=True)  # Высота потолков
    
    # Coordinates for maps
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Metadata
    source_url = db.Column(db.String(300), nullable=True)  # URL источника данных
    scraped_at = db.Column(db.DateTime, nullable=True)  # Дата парсинга
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    developer = db.relationship('Developer', backref='properties')
    complex = db.relationship('ResidentialComplex', backref='properties')
    district = db.relationship('District', backref='properties')
    
    def __repr__(self):
        return f'<Property {self.title}>'
    
    @property
    def formatted_price(self):
        if self.price:
            if self.price >= 1000000:
                return f"{self.price / 1000000:.1f} млн ₽"
            elif self.price >= 1000:
                return f"{self.price / 1000:.0f} тыс ₽"
            return f"{self.price} ₽"
        return "Цена не указана"
    
    @property
    def room_description(self):
        if self.rooms == 0:
            return "Студия"
        elif self.rooms == 1:
            return "1-комнатная"
        elif self.rooms in [2, 3, 4]:
            return f"{self.rooms}-комнатная"
        elif self.rooms:
            return f"{self.rooms}-комн."
        return "Тип не указан"
'''
                    
                    # Добавляем модель в models.py
                    with open('models.py', 'a', encoding='utf-8') as f:
                        f.write(property_model_code)
                    
                    # Создаем таблицы
                    db.create_all()
                    print("✅ Модель Property создана")
                    return True
                else:
                    print("✅ Модель Property уже существует")
                    return True
                    
        except Exception as e:
            print(f"❌ Ошибка при создании модели Property: {e}")
            return False
    
    def ensure_developer_exists(self, name: str, website: str = None) -> Optional[int]:
        """
        Убедиться, что застройщик существует в базе данных
        """
        if not db:
            return None
            
        try:
            with app.app_context():
                developer = Developer.query.filter_by(name=name).first()
                
                if not developer:
                    slug = name.lower().replace(' ', '-').replace('(', '').replace(')', '')
                    
                    developer = Developer(
                        name=name,
                        slug=slug,
                        website=website or '',
                        description=f'Автоматически создан парсером {datetime.now().strftime("%d.%m.%Y")}',
                        created_at=datetime.utcnow()
                    )
                    
                    db.session.add(developer)
                    db.session.commit()
                    print(f"✅ Создан застройщик: {name}")
                
                return developer.id
                
        except Exception as e:
            print(f"❌ Ошибка при создании застройщика {name}: {e}")
            return None
    
    def ensure_complex_exists(self, name: str, developer_id: int, district_id: int = None) -> Optional[int]:
        """
        Убедиться, что ЖК существует в базе данных
        """
        if not db:
            return None
            
        try:
            with app.app_context():
                complex_obj = ResidentialComplex.query.filter_by(
                    name=name, 
                    developer_id=developer_id
                ).first()
                
                if not complex_obj:
                    slug = name.lower().replace(' ', '-').replace('«', '').replace('»', '').replace('"', '')
                    
                    complex_obj = ResidentialComplex(
                        name=name,
                        slug=slug,
                        developer_id=developer_id,
                        district_id=district_id,
                        cashback_rate=5.0  # Значение по умолчанию
                    )
                    
                    db.session.add(complex_obj)
                    db.session.commit()
                    print(f"✅ Создан ЖК: {name}")
                
                return complex_obj.id
                
        except Exception as e:
            print(f"❌ Ошибка при создании ЖК {name}: {e}")
            return None
    
    def determine_district_id(self, text: str) -> Optional[int]:
        """
        Определить район по тексту (примитивное решение)
        """
        if not db:
            return None
            
        text_lower = text.lower()
        
        for keyword, district_name in self.district_mapping.items():
            if keyword in text_lower:
                try:
                    with app.app_context():
                        from models import District
                        district = District.query.filter_by(name=district_name).first()
                        if district:
                            return district.id
                except Exception as e:
                    print(f"Ошибка при поиске района: {e}")
        
        return None
    
    def integrate_scraped_data(self, scraped_data: Dict) -> Dict[str, int]:
        """
        Интеграция спарсенных данных с базой данных
        """
        stats = {
            'developers_created': 0,
            'complexes_created': 0, 
            'apartments_created': 0,
            'errors': 0
        }
        
        if not db:
            print("❌ База данных недоступна")
            return stats
        
        # Создаем модель Property если нужно
        self.create_property_model_if_missing()
        
        try:
            with app.app_context():
                # Импортируем Property после создания
                from models import Property
                
                for dev_code, projects in scraped_data.items():
                    dev_info = self.scraper.developers.get(dev_code, {})
                    dev_name = dev_info.get('name', dev_code)
                    dev_website = dev_info.get('website', '')
                    
                    # Создаем/получаем застройщика
                    developer_id = self.ensure_developer_exists(dev_name, dev_website)
                    if developer_id:
                        stats['developers_created'] += 1
                    
                    for project in projects:
                        try:
                            complex_name = project.get('name', 'Без названия')
                            
                            # Определяем район (примитивно)
                            district_id = self.determine_district_id(complex_name)
                            
                            # Создаем/получаем ЖК
                            complex_id = self.ensure_complex_exists(
                                complex_name, 
                                developer_id, 
                                district_id
                            )
                            
                            if complex_id:
                                stats['complexes_created'] += 1
                            
                            # Добавляем квартиры
                            for i, apartment in enumerate(project.get('apartments', [])):
                                try:
                                    # Создаем уникальный slug
                                    title = f"{complex_name} - {apartment.get('rooms', 0)} комн."
                                    if apartment.get('area'):
                                        title += f", {apartment['area']} м²"
                                    
                                    slug = f"{dev_code}-{complex_id}-{i}-{int(datetime.now().timestamp())}"
                                    
                                    # Проверяем, не существует ли уже такая квартира
                                    existing = Property.query.filter_by(
                                        complex_id=complex_id,
                                        rooms=apartment.get('rooms'),
                                        area=apartment.get('area'),
                                        price=apartment.get('price')
                                    ).first()
                                    
                                    if not existing:
                                        property_obj = Property(
                                            title=title,
                                            slug=slug,
                                            rooms=apartment.get('rooms'),
                                            area=apartment.get('area'),
                                            price=apartment.get('price'),
                                            price_per_sqm=int(apartment['price'] / apartment['area']) if apartment.get('price') and apartment.get('area') else None,
                                            developer_id=developer_id,
                                            complex_id=complex_id,
                                            district_id=district_id,
                                            source_url=apartment.get('source_url'),
                                            scraped_at=datetime.utcnow(),
                                            status='available',
                                            is_active=True
                                        )
                                        
                                        db.session.add(property_obj)
                                        stats['apartments_created'] += 1
                                
                                except Exception as e:
                                    print(f"❌ Ошибка при создании квартиры: {e}")
                                    stats['errors'] += 1
                                    
                        except Exception as e:
                            print(f"❌ Ошибка при обработке проекта {project.get('name')}: {e}")
                            stats['errors'] += 1
                
                # Сохраняем все изменения
                db.session.commit()
                print("✅ Все изменения сохранены в базу данных")
                
        except Exception as e:
            print(f"❌ Критическая ошибка при интеграции данных: {e}")
            try:
                if db and db.session:
                    db.session.rollback()
            except:
                pass  # Ignore rollback errors
            stats['errors'] += 1
        
        return stats
    
    def run_full_scraping_and_integration(self) -> Dict:
        """
        Полный цикл: парсинг + интеграция с базой данных
        """
        print("🚀 Запуск полного цикла парсинга и интеграции")
        print("="*60)
        
        # Этап 1: Парсинг
        print("📡 Этап 1: Парсинг сайтов застройщиков...")
        scraped_data = self.scraper.scrape_all_developers()
        
        # Этап 2: Сохранение в JSON (резервная копия)
        print("\n💾 Этап 2: Сохранение резервной копии...")
        json_file = self.scraper.save_to_json(scraped_data)
        
        # Этап 3: Интеграция с базой данных
        print("\n🔗 Этап 3: Интеграция с базой данных...")
        integration_stats = self.integrate_scraped_data(scraped_data)
        
        # Итоговая статистика
        print("\n" + "="*60)
        print("📊 ИТОГОВАЯ СТАТИСТИКА")
        print("="*60)
        print(f"✅ Застройщиков создано/обновлено: {integration_stats['developers_created']}")
        print(f"✅ ЖК создано/обновлено: {integration_stats['complexes_created']}")  
        print(f"✅ Квартир добавлено: {integration_stats['apartments_created']}")
        print(f"❌ Ошибок: {integration_stats['errors']}")
        
        if json_file:
            print(f"💾 Резервная копия: {json_file}")
        
        result = {
            'scraped_data': scraped_data,
            'integration_stats': integration_stats,
            'json_backup': json_file,
            'timestamp': datetime.now().isoformat()
        }
        
        return result

def main():
    """
    Главная функция для запуска интеграции
    """
    integration = PropertyScraperIntegration()
    result = integration.run_full_scraping_and_integration()
    
    return result

if __name__ == "__main__":
    main()