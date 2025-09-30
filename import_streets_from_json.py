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
    
    # Убираем повторяющиеся дефисы и пробелы
    while '--' in result:
        result = result.replace('--', '-')
    
    return result.strip('-')

def import_streets_from_json():
    """Импортирует все улицы из JSON в базу данных"""
    
    # Подключение к базе данных
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ Ошибка: DATABASE_URL не найден в переменных окружения")
        return False
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Загружаем JSON файл с улицами
        with open('data/streets.json', 'r', encoding='utf-8') as f:
            streets_data = json.load(f)
        
        print(f"📦 Загружено {len(streets_data)} улиц из JSON файла")
        
        # Проверяем текущее количество улиц в базе
        result = session.execute(text("SELECT COUNT(*) as count FROM streets")).fetchone()
        current_count = result.count
        print(f"📊 Текущее количество улиц в базе: {current_count}")
        
        # Получаем список существующих slug'ов
        existing_slugs = set()
        existing_streets = session.execute(text("SELECT slug FROM streets")).fetchall()
        for street in existing_streets:
            existing_slugs.add(street.slug)
        
        # Импортируем улицы
        imported_count = 0
        skipped_count = 0
        
        for street in streets_data:
            name = street['name']
            slug = translit_to_slug(name)
            
            # Проверяем, есть ли уже такая улица
            if slug in existing_slugs:
                skipped_count += 1
                continue
            
            try:
                # Вставляем новую улицу
                session.execute(text("""
                    INSERT INTO streets (name, slug, zoom_level, created_at, updated_at) 
                    VALUES (:name, :slug, 15, NOW(), NOW())
                """), {
                    'name': name,
                    'slug': slug
                })
                
                existing_slugs.add(slug)  # Добавляем в множество чтобы избежать дубликатов
                imported_count += 1
                
                if imported_count % 100 == 0:
                    print(f"✅ Импортировано: {imported_count} улиц...")
                    
            except Exception as e:
                print(f"❌ Ошибка при импорте улицы '{name}': {e}")
                continue
        
        # Подтверждаем изменения
        session.commit()
        session.close()
        
        print(f"\n🎉 Импорт завершен!")
        print(f"✅ Импортировано новых улиц: {imported_count}")
        print(f"⏭️ Пропущено существующих: {skipped_count}")
        print(f"📊 Общее количество улиц: {current_count + imported_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    success = import_streets_from_json()
    if success:
        print("\n🚀 Готово! Теперь можно запустить получение координат:")
        print("python run_coordinates_batch.py 500")
    else:
        sys.exit(1)