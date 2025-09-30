#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def translit_to_slug(text):
    """Создает slug из русского текста"""
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-', '.': '', ',': '', '(': '', ')': '', '№': 'n'
    }
    
    result = ''
    for char in text.lower():
        if char in translit_map:
            result += translit_map[char]
        elif char.isalpha() or char.isdigit() or char == '-':
            result += char
    
    # Убираем повторяющиеся дефисы
    while '--' in result:
        result = result.replace('--', '-')
    
    return result.strip('-')

def import_streets_batch(batch_size=50):
    """Импортирует улицы пачками с частыми коммитами"""
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Ошибка: DATABASE_URL не найден")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        
        # Загружаем JSON
        with open('data/streets.json', 'r', encoding='utf-8') as f:
            streets_data = json.load(f)
        
        print(f"📦 Всего улиц в JSON: {len(streets_data)}")
        
        # Проверяем текущее состояние
        session = Session()
        result = session.execute(text("SELECT COUNT(*) as count FROM streets")).fetchone()
        current_count = result.count
        print(f"📊 Уже в базе: {current_count}")
        
        # Получаем существующие slug'и  
        existing_slugs = set()
        existing_streets = session.execute(text("SELECT slug FROM streets")).fetchall()
        for street in existing_streets:
            existing_slugs.add(street.slug)
        session.close()
        
        # Импортируем пачками
        imported_total = 0
        batch_data = []
        
        for i, street in enumerate(streets_data):
            name = street['name']
            slug = translit_to_slug(name)
            
            if slug in existing_slugs:
                continue
                
            batch_data.append({'name': name, 'slug': slug})
            existing_slugs.add(slug)
            
            # Когда набрали пачку или дошли до конца
            if len(batch_data) >= batch_size or i == len(streets_data) - 1:
                if batch_data:  # Если есть что импортировать
                    session = Session()
                    try:
                        # Импортируем пачку
                        for street_data in batch_data:
                            session.execute(text("""
                                INSERT INTO streets (name, slug, zoom_level, created_at, updated_at) 
                                VALUES (:name, :slug, 15, NOW(), NOW())
                            """), street_data)
                        
                        session.commit()
                        imported_total += len(batch_data)
                        print(f"✅ Импортировано: {imported_total} (пачка: {len(batch_data)})")
                        
                    except Exception as e:
                        session.rollback()
                        print(f"❌ Ошибка в пачке: {e}")
                    finally:
                        session.close()
                    
                    batch_data = []  # Очищаем пачку
        
        print(f"\n🎉 Импорт завершен!")
        print(f"✅ Всего импортировано: {imported_total}")
        return True
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

if __name__ == "__main__":
    success = import_streets_batch(batch_size=100)
    if success:
        print("\n🚀 Теперь запускаем получение координат...")
    else:
        sys.exit(1)