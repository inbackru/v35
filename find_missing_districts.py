#!/usr/bin/env python3
"""
Поиск районов без отдельных страниц и проверка данных
"""

import re

def find_missing_districts():
    """Находит районы без данных в app.py"""
    
    # Читаем список районов из districts.html
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        districts_content = f.read()
    
    # Извлекаем все районы и их route
    district_pattern = r'<!-- ([^-]+?) -->[^<]*<div[^>]*data-district="([^"]+)"[^>]*>.*?href="{{ url_for\(\'district_detail\', district=\'([^\']+)\'\) }}"'
    districts_from_html = re.findall(district_pattern, districts_content, re.DOTALL)
    
    # Читаем данные районов из app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Находим функцию get_district_data и извлекаем существующие районы
    start_idx = app_content.find('def get_district_data(district_slug):')
    end_idx = app_content.find('def district_detail(district):', start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("❌ Не найдена функция get_district_data в app.py")
        return
    
    district_data_section = app_content[start_idx:end_idx]
    
    # Извлекаем ключи существующих районов
    existing_districts = re.findall(r"'([^']+)':\s*{", district_data_section)
    
    print("🔍 Анализ районов:")
    print(f"📋 Всего районов в HTML: {len(districts_from_html)}")
    print(f"📋 Районов с данными в app.py: {len(existing_districts)}")
    
    print("\n✅ Районы с данными:")
    for district in existing_districts:
        print(f"  - {district}")
    
    print("\n❌ Районы БЕЗ данных:")
    missing_districts = []
    for name, data_attr, route in districts_from_html:
        name = name.strip()
        if route not in existing_districts:
            missing_districts.append((name, route))
            print(f"  - {name} ({route})")
    
    print(f"\n📊 Итого недостающих районов: {len(missing_districts)}")
    
    return missing_districts

if __name__ == "__main__":
    find_missing_districts()