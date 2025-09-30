#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def import_districts_to_database():
    """Импортирует все районы из JSON в базу данных"""
    
    # Подключение к базе данных
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Ошибка: DATABASE_URL не найден в переменных окружения")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Загружаем JSON файл с районами
        with open('data/extracted_districts.json', 'r', encoding='utf-8') as f:
            districts_data = json.load(f)
        
        print(f"📦 Загружено {len(districts_data)} районов из JSON файла")
        
        # Проверяем текущее количество районов в базе
        result = session.execute(text("SELECT COUNT(*) as count FROM districts")).fetchone()
        current_count = result.count
        print(f"📊 Текущее количество районов в базе: {current_count}")
        
        # Получаем список существующих slug'ов
        existing_slugs = set()
        existing_districts = session.execute(text("SELECT slug FROM districts")).fetchall()
        for district in existing_districts:
            existing_slugs.add(district.slug)
        
        # Импортируем районы
        imported_count = 0
        skipped_count = 0
        
        for district in districts_data:
            name = district['name']
            slug = district['slug']
            description = district['description']
            
            # Проверяем, есть ли уже такой район
            if slug in existing_slugs:
                skipped_count += 1
                continue
            
            try:
                # Вставляем новый район
                session.execute(text("""
                    INSERT INTO districts (name, slug, description, zoom_level, created_at, updated_at) 
                    VALUES (:name, :slug, :description, 12, NOW(), NOW())
                """), {
                    'name': name,
                    'slug': slug,
                    'description': description
                })
                
                existing_slugs.add(slug)  # Добавляем в множество чтобы избежать дубликатов
                imported_count += 1
                
                if imported_count % 10 == 0:
                    print(f"✅ Импортировано: {imported_count} районов...")
                    
            except Exception as e:
                print(f"❌ Ошибка при импорте района '{name}': {e}")
                continue
        
        # Подтверждаем изменения
        session.commit()
        session.close()
        
        print(f"\n🎉 Импорт завершен!")
        print(f"✅ Импортировано новых районов: {imported_count}")
        print(f"⏭️ Пропущено существующих: {skipped_count}")
        print(f"📊 Общее количество районов: {current_count + imported_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    success = import_districts_to_database()
    if success:
        print("\n🚀 Готово! Теперь можно запустить получение координат для районов:")
        print("python run_coordinates_batch.py 100")
    else:
        sys.exit(1)