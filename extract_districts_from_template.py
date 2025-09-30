#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

def extract_districts_from_template():
    """Извлекает все районы из HTML шаблона"""
    
    districts = []
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все ссылки на районы
    pattern = r"href=\"\{\{ url_for\('district_detail', district='([^']+)'\) \}\}"
    matches = re.findall(pattern, content)
    
    # Находим названия районов
    name_pattern = r'<h3 class="text-xl font-bold mb-1">([^<]+)</h3>'
    names = re.findall(name_pattern, content)
    
    print(f"Найдено {len(matches)} slug'ов районов")
    print(f"Найдено {len(names)} названий районов")
    
    # Создаем список районов
    for i, (slug, name) in enumerate(zip(matches, names)):
        districts.append({
            'id': i + 1,
            'name': name.strip(),
            'slug': slug,
            'description': f'Район {name.strip()} в Краснодаре'
        })
    
    # Сохраняем в JSON
    with open('data/extracted_districts.json', 'w', encoding='utf-8') as f:
        json.dump(districts, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Извлечено {len(districts)} районов:")
    for district in districts:
        print(f"  - {district['name']} ({district['slug']})")
    
    return districts

if __name__ == "__main__":
    districts = extract_districts_from_template()
    print(f"\n📁 Данные сохранены в data/extracted_districts.json")