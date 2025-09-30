#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import random

# Читаем PHP файл с улицами
with open('attached_assets/streets_1754347274172.php', 'r', encoding='utf-8') as f:
    content = f.read()

# Извлекаем все улицы из HTML
street_pattern = r'<span>([^<]+)</span>'
streets_raw = re.findall(street_pattern, content)

# Фильтруем только улицы (исключаем цифры и короткие значения)
streets_filtered = []
for street in streets_raw:
    street = street.strip()
    # Пропускаем числа, короткие строки и нежелательные значения
    if (len(street) > 2 and 
        not street.isdigit() and 
        street not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and
        'text-' not in street and
        'px-' not in street):
        streets_filtered.append(street)

# Убираем дубликаты и сортируем
streets_unique = sorted(list(set(streets_filtered)))

print(f"Найдено уникальных улиц: {len(streets_unique)}")

# Определяем районы Краснодара
districts = [
    "Центральный округ",
    "Прикубанский округ", 
    "Карасунский округ",
    "Западный округ",
    "Фестивальный микрорайон",
    "Юбилейный микрорайон",
    "Гидростроителей",
    "Дубинка",
    "Энка",
    "Российский",
    "Славянский"
]

# Функция для определения первой буквы для группировки
def get_first_letter(street_name):
    first_char = street_name[0].upper()
    if first_char.isdigit():
        return first_char
    elif first_char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return first_char
    else:
        return first_char

# Генерируем JSON данные
streets_data = []
for i, street in enumerate(streets_unique):
    # Случайно выбираем район
    district = random.choice(districts)
    
    # Генерируем случайные, но реалистичные данные
    properties_count = random.randint(5, 80)
    new_buildings = random.randint(1, max(1, properties_count // 8))
    
    # Определяем букву для группировки
    letter = get_first_letter(street)
    
    street_data = {
        "id": i + 1,
        "name": street,
        "district": district,
        "properties_count": properties_count,
        "new_buildings": new_buildings,
        "letter": letter
    }
    
    streets_data.append(street_data)

# Сохраняем в JSON файл
with open('data/streets.json', 'w', encoding='utf-8') as f:
    json.dump(streets_data, f, ensure_ascii=False, indent=2)

print(f"Сохранено {len(streets_data)} улиц в data/streets.json")

# Показываем статистику по буквам
from collections import Counter
letter_counts = Counter([s['letter'] for s in streets_data])
print("\nСтатистика по буквам:")
for letter in sorted(letter_counts.keys()):
    print(f"{letter}: {letter_counts[letter]} улиц")