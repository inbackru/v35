"""
Создание полной иерархии Застройщик → ЖК → Корпус → Квартиры из Excel данных
Автоматическое создание связанных записей в таблицах developers, residential_complexes, buildings, properties
"""
import sys
import os
from datetime import datetime
import re

# Добавим путь к нашему приложению
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import ExcelProperty, Developer, ResidentialComplex, Building, Property

def slugify(text):
    """Создание slug из текста"""
    if not text:
        return ""
    # Конвертируем в нижний регистр и заменяем пробелы на дефисы
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def create_developers_from_excel():
    """Создание застройщиков из Excel данных"""
    print("=== СОЗДАНИЕ ЗАСТРОЙЩИКОВ ===")
    
    with app.app_context():
        # Получаем уникальных застройщиков из Excel данных
        excel_data = db.session.query(ExcelProperty).all()
        
        unique_developers = {}
        for record in excel_data:
            if record.developer_name and record.developer_name not in unique_developers:
                unique_developers[record.developer_name] = {
                    'name': record.developer_name,
                    'excel_id': record.developer_id_excel,
                    'site': record.developer_site
                }
        
        print(f"Найдено {len(unique_developers)} уникальных застройщиков")
        
        created_count = 0
        for dev_name, dev_data in unique_developers.items():
            # Проверяем, существует ли уже такой застройщик
            existing = db.session.query(Developer).filter_by(name=dev_name).first()
            
            if not existing:
                developer = Developer(
                    name=dev_name,
                    slug=slugify(dev_name),
                    website=dev_data['site'],
                    description=f"Застройщик {dev_name}",
                    created_at=datetime.utcnow()
                )
                
                db.session.add(developer)
                created_count += 1
                print(f"Создан застройщик: {dev_name}")
        
        db.session.commit()
        print(f"Создано {created_count} новых застройщиков")
        
        return db.session.query(Developer).count()

def create_residential_complexes_from_excel():
    """Создание ЖК из Excel данных"""
    print("\n=== СОЗДАНИЕ ЖИЛЫХ КОМПЛЕКСОВ ===")
    
    with app.app_context():
        # Получаем уникальные ЖК из Excel данных
        excel_data = db.session.query(ExcelProperty).all()
        
        unique_complexes = {}
        for record in excel_data:
            if record.complex_name and record.complex_name not in unique_complexes:
                unique_complexes[record.complex_name] = {
                    'name': record.complex_name,
                    'excel_id': record.complex_id_excel,
                    'developer_name': record.developer_name,
                    'phone': record.complex_phone,
                    'address': record.complex_sales_address,
                    'class_name': record.complex_object_class_display_name,
                    'lat': record.address_position_lat,
                    'lon': record.address_position_lon
                }
        
        print(f"Найдено {len(unique_complexes)} уникальных ЖК")
        
        created_count = 0
        for complex_name, complex_data in unique_complexes.items():
            # Проверяем, существует ли уже такой ЖК
            existing = db.session.query(ResidentialComplex).filter_by(name=complex_name).first()
            
            if not existing:
                # Найдем застройщика по имени
                developer = None
                if complex_data['developer_name']:
                    developer = db.session.query(Developer).filter_by(name=complex_data['developer_name']).first()
                
                residential_complex = ResidentialComplex(
                    name=complex_name,
                    slug=slugify(complex_name),
                    developer_id=developer.id if developer else None,
                    phone=complex_data['phone'],
                    address=complex_data['address'],
                    description=f"Жилой комплекс {complex_name}",
                    latitude=float(complex_data['lat']) if complex_data['lat'] else None,
                    longitude=float(complex_data['lon']) if complex_data['lon'] else None,
                    class_name=complex_data['class_name'],
                    created_at=datetime.utcnow(),
                    is_active=True
                )
                
                db.session.add(residential_complex)
                created_count += 1
                print(f"Создан ЖК: {complex_name} (застройщик: {complex_data['developer_name']})")
        
        db.session.commit()
        print(f"Создано {created_count} новых ЖК")
        
        return db.session.query(ResidentialComplex).count()

def create_buildings_from_excel():
    """Создание корпусов/литеров из Excel данных"""
    print("\n=== СОЗДАНИЕ КОРПУСОВ ===")
    
    with app.app_context():
        # Получаем уникальные корпуса из Excel данных
        excel_data = db.session.query(ExcelProperty).all()
        
        unique_buildings = {}
        for record in excel_data:
            if record.complex_building_name and record.complex_name:
                building_key = f"{record.complex_name}_{record.complex_building_name}"
                
                if building_key not in unique_buildings:
                    unique_buildings[building_key] = {
                        'name': record.complex_building_name,
                        'complex_name': record.complex_name,
                        'excel_building_id': record.complex_building_id,
                        'released': record.complex_building_released,
                        'is_unsafe': record.complex_building_is_unsafe,
                        'has_accreditation': record.complex_building_accreditation,
                        'end_build_year': record.complex_building_end_build_year,
                        'end_build_quarter': record.complex_building_end_build_quarter,
                        'total_floors': record.object_max_floor
                    }
        
        print(f"Найдено {len(unique_buildings)} уникальных корпусов")
        
        created_count = 0
        for building_key, building_data in unique_buildings.items():
            # Найдем ЖК по имени
            complex_obj = db.session.query(ResidentialComplex).filter_by(name=building_data['complex_name']).first()
            
            if complex_obj:
                # Проверяем, существует ли уже такой корпус
                existing = db.session.query(Building).filter_by(
                    name=building_data['name'],
                    complex_id=complex_obj.id
                ).first()
                
                if not existing:
                    building = Building(
                        name=building_data['name'],
                        slug=slugify(f"{building_data['complex_name']}-{building_data['name']}"),
                        complex_id=complex_obj.id,
                        building_id=str(building_data['excel_building_id']) if building_data['excel_building_id'] else None,
                        building_name=building_data['name'],
                        released=building_data['released'] or False,
                        is_unsafe=building_data['is_unsafe'] or False,
                        has_accreditation=building_data['has_accreditation'] or False,
                        end_build_year=building_data['end_build_year'],
                        end_build_quarter=building_data['end_build_quarter'],
                        total_floors=building_data['total_floors'] or 1,
                        created_at=datetime.utcnow()
                    )
                    
                    db.session.add(building)
                    created_count += 1
                    print(f"Создан корпус: {building_data['name']} в ЖК {building_data['complex_name']}")
        
        db.session.commit()
        print(f"Создано {created_count} новых корпусов")
        
        return db.session.query(Building).count()

def create_properties_from_excel():
    """Создание квартир из Excel данных"""
    print("\n=== СОЗДАНИЕ КВАРТИР ===")
    
    with app.app_context():
        excel_data = db.session.query(ExcelProperty).all()
        
        created_count = 0
        for record in excel_data:
            # Найдем связанные объекты
            developer = None
            if record.developer_name:
                developer = db.session.query(Developer).filter_by(name=record.developer_name).first()
            
            complex_obj = None
            if record.complex_name:
                complex_obj = db.session.query(ResidentialComplex).filter_by(name=record.complex_name).first()
            
            building = None
            if record.complex_building_name and complex_obj:
                building = db.session.query(Building).filter_by(
                    name=record.complex_building_name,
                    complex_id=complex_obj.id
                ).first()
            
            # Создаем slug и title для квартиры
            title = f"{record.object_rooms}-комн" if record.object_rooms and record.object_rooms > 0 else "Студия"
            slug = slugify(f"{title}-{record.inner_id}")
            
            # Создаем квартиру
            property_obj = Property(
                title=title,
                slug=slug,
                rooms=record.object_rooms or 0,
                area=float(record.object_area) if record.object_area else None,
                floor=record.object_min_floor,
                total_floors=record.object_max_floor or (building.total_floors if building else 1),
                price=record.price,
                price_per_sqm=record.square_price,
                developer_id=developer.id if developer else None,
                complex_id=complex_obj.id if complex_obj else None,
                building_id=building.id if building else None,
                status='available',
                is_active=True,
                main_image=None,  # Добавим фото позже
                latitude=float(record.address_position_lat) if record.address_position_lat else None,
                longitude=float(record.address_position_lon) if record.address_position_lon else None,
                source_url=record.url,
                inner_id=str(record.inner_id),
                renovation_type=record.renovation_display_name,
                mortgage_price=float(record.mortgage_price) if record.mortgage_price else None,
                address=record.address_name,
                created_at=datetime.utcnow()
            )
            
            db.session.add(property_obj)
            created_count += 1
            
            if created_count % 20 == 0:
                db.session.commit()
                print(f"Создано {created_count} квартир...")
        
        db.session.commit()
        print(f"Создано {created_count} новых квартир")
        
        return db.session.query(Property).count()

def main():
    """Основная функция создания иерархии"""
    print("=== СОЗДАНИЕ ПОЛНОЙ ИЕРАРХИИ ИЗ EXCEL ДАННЫХ ===")
    
    with app.app_context():
        # Проверим, есть ли данные Excel
        excel_count = db.session.query(ExcelProperty).count()
        print(f"Данных Excel в БД: {excel_count}")
        
        if excel_count == 0:
            print("Нет данных Excel для обработки!")
            return
    
    # 1. Создаем застройщиков
    developers_count = create_developers_from_excel()
    
    # 2. Создаем ЖК
    complexes_count = create_residential_complexes_from_excel()
    
    # 3. Создаем корпуса
    buildings_count = create_buildings_from_excel()
    
    # 4. Создаем квартиры
    properties_count = create_properties_from_excel()
    
    print("\n=== ИТОГО СОЗДАНО ===")
    print(f"Застройщиков: {developers_count}")
    print(f"Жилых комплексов: {complexes_count}")
    print(f"Корпусов: {buildings_count}")
    print(f"Квартир: {properties_count}")
    
    print("\n=== ИЕРАРХИЯ ГОТОВА! ===")
    print("Теперь на сайте будут отображаться:")
    print("- /developers - страница застройщиков")
    print("- /residential-complexes - страница ЖК")
    print("- /properties - страница квартир с полными данными")

if __name__ == "__main__":
    main()