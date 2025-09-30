#!/usr/bin/env python3
"""
Импорт данных из парсера с созданием иерархической структуры:
Застройщик → ЖК → Литер/Корпус → Квартиры
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from app import app, db
from models import Developer, ResidentialComplex, Building, Property, District

def generate_slug(name):
    """Генерация slug из названия"""
    if not name or pd.isna(name):
        return 'unnamed'
    slug = re.sub(r'[^\w\s-]', '', str(name).lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def safe_get(row, field, default=None):
    """Безопасно получить значение поля"""
    try:
        value = row.get(field, default)
        if pd.isna(value) or value is None or value == '':
            return default
        return value
    except:
        return default

def safe_str(value, default=''):
    """Безопасно преобразовать в строку"""
    if pd.isna(value) or value is None:
        return default
    return str(value).strip()

def safe_int(value, default=0):
    """Безопасно преобразовать в int"""
    if pd.isna(value) or value is None:
        return default
    try:
        return int(float(value))
    except:
        return default

def safe_float(value, default=0.0):
    """Безопасно преобразовать в float"""
    if pd.isna(value) or value is None:
        return default
    try:
        return float(value)
    except:
        return default

def import_hierarchy_from_parser(excel_file):
    """Импорт данных с созданием полной иерархии"""
    
    print("🚀 ИМПОРТ ИЕРАРХИЧЕСКОЙ СТРУКТУРЫ ИЗ ПАРСЕРА")
    print("=" * 60)
    
    # Читаем данные
    df = pd.read_excel(excel_file)
    print(f"📊 Загружено {len(df)} записей квартир")
    
    stats = {
        'developers': 0,
        'complexes': 0, 
        'buildings': 0,
        'properties': 0
    }
    
    # Группируем данные по застройщикам
    developer_groups = df.groupby('developer_name')
    
    for dev_name, dev_data in developer_groups:
        print(f"\n🏗️ Обработка застройщика: {dev_name}")
        
        # 1. Создаем или находим застройщика
        developer = Developer.query.filter_by(name=dev_name).first()
        if not developer:
            developer = Developer(
                name=dev_name,
                slug=generate_slug(dev_name),
                website=safe_str(dev_data.iloc[0]['developer_site']),
                created_at=datetime.utcnow()
            )
            db.session.add(developer)
            db.session.flush()  # Получаем ID
            stats['developers'] += 1
            print(f"  ✅ Создан застройщик: {dev_name}")
        
        # Группируем по ЖК
        complex_groups = dev_data.groupby('complex_name')
        
        for complex_name, complex_data in complex_groups:
            print(f"    🏘️ Обработка ЖК: {complex_name}")
            
            # 2. Создаем или находим ЖК
            complex_obj = ResidentialComplex.query.filter_by(
                name=complex_name, 
                developer_id=developer.id
            ).first()
            
            if not complex_obj:
                first_row = complex_data.iloc[0]
                
                complex_obj = ResidentialComplex(
                    name=complex_name,
                    slug=generate_slug(complex_name),
                    developer_id=developer.id,
                    
                    # Данные из парсера
                    complex_id=safe_str(first_row['complex_id']),
                    complex_phone=safe_str(first_row['complex_phone']),
                    sales_phone=safe_str(first_row['complex_sales_phone']),
                    sales_address=safe_str(first_row['complex_sales_address']),
                    object_class_display_name=safe_str(first_row['complex_object_class_display_name']),
                    
                    # Даты строительства
                    start_build_year=safe_int(first_row['complex_start_build_year']),
                    start_build_quarter=safe_int(first_row['complex_start_build_quarter']),
                    first_build_year=safe_int(first_row['complex_first_build_year']),
                    first_build_quarter=safe_int(first_row['complex_first_build_quarter']),
                    end_build_year=safe_int(first_row['complex_end_build_year']),
                    end_build_quarter=safe_int(first_row['complex_end_build_quarter']),
                    
                    # Особенности
                    has_accreditation=bool(safe_get(first_row, 'complex_has_accreditation', False)),
                    has_green_mortgage=bool(safe_get(first_row, 'complex_has_green_mortgage', False)),
                    has_big_check=bool(safe_get(first_row, 'complex_has_big_check', False)),
                    with_renovation=bool(safe_get(first_row, 'complex_with_renovation', False)),
                    financing_sber=bool(safe_get(first_row, 'complex_financing_sber', False)),
                    
                    created_at=datetime.utcnow()
                )
                db.session.add(complex_obj)
                db.session.flush()
                stats['complexes'] += 1
                print(f"      ✅ Создан ЖК: {complex_name}")
            
            # Группируем по корпусам/литерам
            building_groups = complex_data.groupby('complex_building_name')
            
            for building_name, building_data in building_groups:
                if pd.isna(building_name) or str(building_name).strip() == '':
                    building_name = 'Основной корпус'
                    
                print(f"        🏢 Обработка корпуса: {building_name}")
                
                # 3. Создаем или находим корпус/литер
                building = Building.query.filter_by(
                    name=building_name,
                    complex_id=complex_obj.id
                ).first()
                
                if not building:
                    first_building_row = building_data.iloc[0]
                    
                    building = Building(
                        name=building_name,
                        slug=generate_slug(building_name),
                        complex_id=complex_obj.id,
                        
                        # Данные из парсера
                        building_id=safe_str(first_building_row['complex_building_id']),
                        building_name=safe_str(first_building_row['complex_building_name']),
                        released=bool(safe_get(first_building_row, 'complex_building_released', False)),
                        is_unsafe=bool(safe_get(first_building_row, 'complex_building_is_unsafe', False)),
                        has_accreditation=bool(safe_get(first_building_row, 'complex_building_accreditation', False)),
                        has_green_mortgage=bool(safe_get(first_building_row, 'complex_building_has_green_mortgage', False)),
                        
                        end_build_year=safe_int(first_building_row['complex_building_end_build_year']),
                        end_build_quarter=safe_int(first_building_row['complex_building_end_build_quarter']),
                        complex_product=safe_str(first_building_row['complex_building_complex_product']),
                        
                        total_apartments=len(building_data),
                        created_at=datetime.utcnow()
                    )
                    db.session.add(building)
                    db.session.flush()
                    stats['buildings'] += 1
                    print(f"          ✅ Создан корпус: {building_name}")
                
                # 4. Создаем квартиры
                for _, apartment_row in building_data.iterrows():
                    # Проверяем, не существует ли уже такая квартира
                    existing_property = Property.query.filter_by(
                        building_id=building.id,
                        rooms=safe_int(apartment_row['object_rooms']),
                        area=safe_float(apartment_row['object_area']),
                        price=safe_float(apartment_row['price'])
                    ).first()
                    
                    if not existing_property:
                        # Создаем уникальный slug для квартиры
                        property_title = f"{safe_int(apartment_row['object_rooms'])}-комнатная квартира в {building_name}"
                        property_slug = f"{generate_slug(property_title)}-{apartment_row['inner_id']}"
                        
                        property_obj = Property(
                            # Связи
                            building_id=building.id,
                            residential_complex_id=complex_obj.id,
                            developer_id=developer.id,
                            
                            # Основные характеристики
                            title=property_title,
                            slug=property_slug,
                            rooms=safe_int(apartment_row['object_rooms']),
                            area=safe_float(apartment_row['object_area']),
                            price=safe_float(apartment_row['price']),
                            price_per_sqm=safe_float(apartment_row['square_price']),
                            
                            # Этажность
                            floor=safe_int(apartment_row['object_min_floor']),
                            total_floors=safe_int(apartment_row['object_max_floor']),
                            
                            # Адрес
                            address=safe_str(apartment_row['address_display_name']),
                            latitude=safe_float(apartment_row['address_position_lat']),
                            longitude=safe_float(apartment_row['address_position_lon']),
                            
                            # Ремонт
                            renovation_type=safe_str(apartment_row['renovation_type']),
                            
                            # Дополнительные данные из парсера
                            inner_id=safe_str(apartment_row['inner_id']),
                            url=safe_str(apartment_row['url']),
                            is_apartment=bool(safe_get(apartment_row, 'object_is_apartment', True)),
                            
                            # Ипотека и сделки
                            mortgage_price=safe_float(apartment_row['mortgage_price']),
                            min_rate=safe_float(apartment_row['min_rate']),
                            deal_type=safe_str(apartment_row['deal_type']),
                            
                            created_at=datetime.utcnow()
                        )
                        db.session.add(property_obj)
                        stats['properties'] += 1
                
                print(f"          📊 Добавлено квартир: {len(building_data)}")
    
    # Сохраняем все изменения
    db.session.commit()
    
    print(f"\n🎉 ИМПОРТ ЗАВЕРШЕН!")
    print(f"📈 СТАТИСТИКА:")
    print(f"  • Застройщики: {stats['developers']}")
    print(f"  • Жилые комплексы: {stats['complexes']}")
    print(f"  • Корпуса/литеры: {stats['buildings']}")
    print(f"  • Квартиры: {stats['properties']}")
    
    return stats

def main():
    """Основная функция"""
    with app.app_context():
        excel_file = 'attached_assets/Сочи_1756306374885.xlsx'
        
        if not os.path.exists(excel_file):
            print(f"❌ Файл {excel_file} не найден!")
            return
        
        try:
            stats = import_hierarchy_from_parser(excel_file)
            
            print(f"\n✅ Импорт завершен успешно!")
            print(f"Всего обработано: {sum(stats.values())} объектов")
            
        except Exception as e:
            print(f"❌ Ошибка импорта: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == "__main__":
    main()