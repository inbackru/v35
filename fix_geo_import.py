#!/usr/bin/env python3
"""
Исправленный импорт географических данных
"""

import pandas as pd
import os
from app import app, db
from sqlalchemy import text
import uuid

def safe_value(value):
    """Безопасное преобразование значений, включая NaN"""
    if pd.isna(value) or str(value) == 'nan' or value is None:
        return None
    if isinstance(value, str) and value.strip() == '':
        return None
    return value

def import_districts_safe():
    """Безопасный импорт районов"""
    
    with app.app_context():
        print("🗺️ Исправленный импорт районов...")
        
        try:
            # Создаем таблицу если не существует
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS districts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT UNIQUE,
                    latitude DECIMAL(10,6),
                    longitude DECIMAL(10,6), 
                    zoom_level INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    distance_to_center DECIMAL(10,2),
                    infrastructure_data TEXT
                );
            """))
            
            # Очищаем существующие данные
            db.session.execute(text("DELETE FROM districts"))
            db.session.commit()
            print("✅ Таблица районов очищена")
            
            # Читаем данные
            districts_df = pd.read_excel('attached_assets/districts (7)_1757524447190.xlsx')
            print(f"📍 Найдено {len(districts_df)} районов для импорта")
            
            imported = 0
            errors = 0
            
            for _, row in districts_df.iterrows():
                try:
                    # Подготовка данных
                    district_id = int(row['id'])
                    name = str(row['name'])
                    slug = safe_value(row['slug']) or f"district-{district_id}-{uuid.uuid4().hex[:8]}"
                    lat = safe_value(row['latitude'])
                    lon = safe_value(row['longitude'])
                    zoom = safe_value(row['zoom_level'])
                    desc = safe_value(row.get('description', ''))
                    distance = safe_value(row.get('distance_to_center'))
                    infra = safe_value(row.get('infrastructure_data')) or '{}'
                    
                    # Попытка вставки в отдельной транзакции
                    try:
                        db.session.execute(text("""
                            INSERT INTO districts (id, name, slug, latitude, longitude, zoom_level, 
                                                 description, distance_to_center, infrastructure_data)
                            VALUES (:id, :name, :slug, :lat, :lon, :zoom, :desc, :distance, :infra)
                        """), {
                            'id': district_id,
                            'name': name,
                            'slug': slug,
                            'lat': lat,
                            'lon': lon,
                            'zoom': zoom,
                            'desc': desc,
                            'distance': distance,
                            'infra': str(infra)
                        })
                        db.session.commit()
                        imported += 1
                        
                        if imported % 10 == 0:
                            print(f"✅ Импортировано {imported} районов...")
                            
                    except Exception as insert_error:
                        db.session.rollback()
                        errors += 1
                        print(f"❌ Ошибка вставки района {name}: {insert_error}")
                        
                except Exception as e:
                    errors += 1
                    print(f"❌ Ошибка обработки района {row.get('name', 'Unknown')}: {e}")
            
            print(f"📊 Импорт районов завершен:")
            print(f"   ✅ Успешно: {imported}")
            print(f"   ❌ Ошибок: {errors}")
            return imported
            
        except Exception as e:
            print(f"❌ Критическая ошибка импорта районов: {e}")
            db.session.rollback()
            return 0

def import_streets_safe():
    """Безопасный импорт улиц"""
    
    with app.app_context():
        print("🛣️ Исправленный импорт улиц...")
        
        try:
            # Создаем таблицу если не существует
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS streets (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT UNIQUE,
                    district_id INTEGER,
                    latitude DECIMAL(10,6),
                    longitude DECIMAL(10,6),
                    zoom_level INTEGER,
                    street_type TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    distance_to_center DECIMAL(10,2),
                    infrastructure_data TEXT,
                    FOREIGN KEY (district_id) REFERENCES districts (id)
                );
            """))
            
            # Очищаем существующие данные
            db.session.execute(text("DELETE FROM streets"))
            db.session.commit()
            print("✅ Таблица улиц очищена")
            
            # Читаем данные
            streets_df = pd.read_excel('attached_assets/streets (2)_1757524447189.xlsx')
            print(f"🛣️ Найдено {len(streets_df)} улиц для импорта")
            
            imported = 0
            errors = 0
            
            for _, row in streets_df.iterrows():
                try:
                    # Подготовка данных
                    street_id = int(row['id'])
                    name = str(row['name'])
                    slug = safe_value(row['slug']) or f"street-{street_id}-{uuid.uuid4().hex[:8]}"
                    district_id = safe_value(row.get('district_id'))
                    lat = safe_value(row['latitude'])
                    lon = safe_value(row['longitude'])
                    zoom = safe_value(row['zoom_level'])
                    street_type = safe_value(row.get('street_type'))
                    desc = safe_value(row.get('description'))
                    distance = safe_value(row.get('distance_to_center'))
                    infra = safe_value(row.get('infrastructure_data')) or '{}'
                    
                    # Попытка вставки в отдельной транзакции
                    try:
                        db.session.execute(text("""
                            INSERT INTO streets (id, name, slug, district_id, latitude, longitude, 
                                               zoom_level, street_type, description, distance_to_center, 
                                               infrastructure_data)
                            VALUES (:id, :name, :slug, :district_id, :lat, :lon, :zoom, :type, 
                                   :desc, :distance, :infra)
                        """), {
                            'id': street_id,
                            'name': name,
                            'slug': slug,
                            'district_id': district_id,
                            'lat': lat,
                            'lon': lon,
                            'zoom': zoom,
                            'type': street_type,
                            'desc': desc,
                            'distance': distance,
                            'infra': str(infra)
                        })
                        db.session.commit()
                        imported += 1
                        
                        if imported % 200 == 0:
                            print(f"✅ Импортировано {imported} улиц...")
                            
                    except Exception as insert_error:
                        db.session.rollback()
                        errors += 1
                        # Не логируем каждую ошибку для экономии места
                        if errors <= 10:
                            print(f"❌ Ошибка вставки улицы {name}: {insert_error}")
                        elif errors == 11:
                            print("❌ Слишком много ошибок, переключаемся в тихий режим...")
                        
                except Exception as e:
                    errors += 1
                    if errors <= 10:
                        print(f"❌ Ошибка обработки улицы {row.get('name', 'Unknown')}: {e}")
            
            print(f"📊 Импорт улиц завершен:")
            print(f"   ✅ Успешно: {imported}")
            print(f"   ❌ Ошибок: {errors}")
            return imported
            
        except Exception as e:
            print(f"❌ Критическая ошибка импорта улиц: {e}")
            db.session.rollback()
            return 0

if __name__ == "__main__":
    print("🚀 Начинаем исправленный импорт географических данных...")
    
    districts_imported = import_districts_safe()
    streets_imported = import_streets_safe()
    
    # Финальная проверка
    with app.app_context():
        districts_count = db.session.execute(text("SELECT COUNT(*) FROM districts")).scalar()
        streets_count = db.session.execute(text("SELECT COUNT(*) FROM streets")).scalar()
        
        print(f"\n🎉 Финальная статистика:")
        print(f"   📍 Районов в базе: {districts_count}")
        print(f"   🛣️ Улиц в базе: {streets_count}")
        
        if districts_count > 0:
            # Показать примеры данных с координатами
            sample_districts = db.session.execute(text("""
                SELECT name, latitude, longitude 
                FROM districts 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
                LIMIT 3
            """)).fetchall()
            
            if sample_districts:
                print(f"   🗺️ Примеры районов с координатами:")
                for d in sample_districts:
                    print(f"     - {d.name}: {d.latitude}, {d.longitude}")
    
    print("✅ Импорт завершен!")