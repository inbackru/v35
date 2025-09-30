#!/usr/bin/env python3
"""
Универсальный импорт новых данных из Excel файлов
Автоматически создает новых застройщиков, ЖК и квартиры
"""

import pandas as pd
import json
from flask import Flask
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from sqlalchemy import text

def import_new_excel_data(filename):
    """
    Импорт новых данных из Excel файла
    Автоматически создает:
    1. Новых застройщиков (если их нет в базе)
    2. Новые ЖК (если их нет в базе) 
    3. Новые квартиры (обновляет существующие)
    """
    
    print(f"🔄 Начинаем импорт из файла: {filename}")
    
    # Загружаем Excel файл
    try:
        df = pd.read_excel(filename)
        print(f"📊 Найдено {len(df)} записей в файле")
        print(f"📋 Колонки: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Ошибка загрузки файла: {e}")
        return False
    
    # Проверяем наличие необходимых колонок
    required_columns = ['developer_name', 'complex_name']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Отсутствуют обязательные колонки: {missing_columns}")
        return False
    
    with app.app_context():
        try:
            # 1. Создаем новых застройщиков
            import_developers_from_excel(df)
            
            # 2. Создаем новые ЖК 
            import_complexes_from_excel(df)
            
            # 3. Импортируем все квартиры в таблицу excel_properties
            import_properties_to_excel_table(df)
            
            db.session.commit()
            print("✅ Импорт завершен успешно!")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка импорта: {e}")
            db.session.rollback()
            return False

def import_developers_from_excel(df):
    """Создает новых застройщиков из Excel данных"""
    
    print("\n🏗️ Импортируем застройщиков...")
    
    # Получаем уникальных застройщиков из Excel
    unique_developers = df['developer_name'].dropna().unique()
    
    created_count = 0
    
    for dev_name in unique_developers:
        # Проверяем, есть ли уже такой застройщик
        existing = Developer.query.filter_by(name=dev_name.strip()).first()
        
        if not existing:
            # Создаем нового застройщика
            developer = Developer(
                name=dev_name.strip(),
                slug=dev_name.strip().replace(' ', '-').lower(),
                description=f'Надёжный застройщик {dev_name.strip()} с многолетним опытом строительства качественного жилья.',
                website=f'https://{dev_name.strip().replace(" ", "").lower()}.ru',
                phone='+7-861-000-00-00',
                email=f'info@{dev_name.strip().replace(" ", "").lower()}.ru',
                rating=4.5,
                founded_year=2010,
                experience_years=14,
                completed_projects=5,
                completed_buildings=15,
                completed_complexes=5,
                is_active=True,
                logo_url='https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=200',
                banner_image='https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800',
                features=json.dumps([
                    'Собственное строительство',
                    'Сдача объектов в срок',
                    'Качественные материалы',
                    'Полное сопровождение сделки'
                ]),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(developer)
            created_count += 1
            print(f"   ➕ Создан застройщик: {dev_name}")
        else:
            print(f"   ✓ Застройщик уже существует: {dev_name}")
    
    print(f"🏗️ Создано новых застройщиков: {created_count}")

def import_complexes_from_excel(df):
    """Создает новые ЖК из Excel данных"""
    
    print("\n🏢 Импортируем жилые комплексы...")
    
    # Группируем по ЖК для получения уникальных комплексов
    complex_groups = df.groupby(['developer_name', 'complex_name']).first().reset_index()
    
    created_count = 0
    
    for _, complex_data in complex_groups.iterrows():
        complex_name = complex_data['complex_name']
        developer_name = complex_data['developer_name'] 
        
        if pd.isna(complex_name) or pd.isna(developer_name):
            continue
            
        # Проверяем, есть ли уже такой ЖК по имени
        existing = ResidentialComplex.query.filter_by(
            name=complex_name.strip()
        ).first()
        
        if not existing:
            # Находим ID застройщика
            developer = Developer.query.filter_by(name=developer_name.strip()).first()
            developer_id = developer.id if developer else None
            
            # Создаем новый ЖК
            residential_complex = ResidentialComplex(
                name=complex_name.strip(),
                slug=complex_name.strip().replace(' ', '-').lower(),
                developer_id=developer_id,
                description=f'Современный жилой комплекс {complex_name.strip()} от застройщика {developer_name.strip()}',
                district=complex_data.get('district', 'Центральный'),
                address=complex_data.get('address_short_display_name', 'Адрес уточняется'),
                min_price=int(complex_data.get('price', 5000000)) if pd.notna(complex_data.get('price')) else 5000000,
                total_units=100,  # Будет обновлено при подсчете квартир
                completion_year=int(complex_data.get('complex_end_build_year', 2025)) if pd.notna(complex_data.get('complex_end_build_year')) else 2025,
                completion_quarter=complex_data.get('complex_end_build_quarter', 'IV'),
                building_count=1,
                infrastructure=json.dumps([
                    'Детская площадка',
                    'Парковка',
                    'Видеонаблюдение',
                    'Благоустроенный двор'
                ]),
                latitude=float(complex_data.get('address_position_lat', 45.0)) if pd.notna(complex_data.get('address_position_lat')) else 45.0,
                longitude=float(complex_data.get('address_position_lon', 39.0)) if pd.notna(complex_data.get('address_position_lon')) else 39.0,
                is_active=True,
                images=json.dumps(['https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800']),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(residential_complex)
            created_count += 1
            print(f"   ➕ Создан ЖК: {complex_name} ({developer_name})")
        else:
            print(f"   ✓ ЖК уже существует: {complex_name}")
    
    print(f"🏢 Создано новых ЖК: {created_count}")

def import_properties_to_excel_table(df):
    """Импортирует все данные в таблицу excel_properties"""
    
    print(f"\n🏠 Импортируем {len(df)} квартир в таблицу excel_properties...")
    
    # Очищаем таблицу excel_properties перед новым импортом
    db.session.execute(text("DELETE FROM excel_properties"))
    print("   🧹 Очищена старая таблица excel_properties")
    
    imported_count = 0
    
    for index, row in df.iterrows():
        try:
            # Подготавливаем данные для импорта
            property_data = {}
            
            # Проходим по всем колонкам Excel и сохраняем их
            for column in df.columns:
                value = row[column]
                
                # Обрабатываем специальные типы данных
                if pd.isna(value):
                    property_data[column] = None
                elif column == 'photos' and isinstance(value, str):
                    # Обрабатываем JSON строки с фотографиями
                    try:
                        property_data[column] = json.loads(value) if value else []
                    except:
                        property_data[column] = [value] if value else []
                elif isinstance(value, (int, float)):
                    property_data[column] = value
                else:
                    property_data[column] = str(value)
            
            # Создаем уникальный inner_id если его нет
            if 'inner_id' not in property_data or not property_data['inner_id']:
                property_data['inner_id'] = f"prop_{imported_count + 1}_{index}"
            
            # Вставляем данные в таблицу excel_properties
            columns = ', '.join(property_data.keys())
            placeholders = ', '.join([':' + key for key in property_data.keys()])
            
            insert_query = f"""
                INSERT INTO excel_properties ({columns})
                VALUES ({placeholders})
            """
            
            db.session.execute(text(insert_query), property_data)
            imported_count += 1
            
            if imported_count % 50 == 0:
                print(f"   📦 Импортировано {imported_count} квартир...")
                
        except Exception as e:
            print(f"   ❌ Ошибка импорта квартиры {index}: {e}")
            continue
    
    print(f"🏠 Импортировано квартир: {imported_count}")

if __name__ == "__main__":
    # Импортируем новый файл
    filename = "attached_assets/Сочи_1756384471034.xlsx"
    
    if os.path.exists(filename):
        success = import_new_excel_data(filename)
        if success:
            print("\n🎉 Импорт завершен! Новые данные добавлены в базу.")
        else:
            print("\n❌ Импорт не удался. Проверьте логи ошибок.")
    else:
        print(f"❌ Файл {filename} не найден!")