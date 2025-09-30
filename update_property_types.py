import json
import random

# Загружаем данные
with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
    properties = json.load(f)

# Определяем различные типы недвижимости
property_types = [
    {"type": "студия", "rooms": 0, "area_range": (25, 35), "title_template": "Студия {} м²"},
    {"type": "1-комн", "rooms": 1, "area_range": (35, 50), "title_template": "1-комнатная квартира {} м²"},
    {"type": "2-комн", "rooms": 2, "area_range": (55, 75), "title_template": "2-комнатная квартира {} м²"},
    {"type": "3-комн", "rooms": 3, "area_range": (75, 95), "title_template": "3-комнатная квартира {} м²"},
    {"type": "4+-комн", "rooms": 4, "area_range": (95, 120), "title_template": "4-комнатная квартира {} м²"},
    {"type": "пентхаус", "rooms": 3, "area_range": (120, 180), "title_template": "Пентхаус {} м²"},
    {"type": "апартаменты", "rooms": 1, "area_range": (40, 60), "title_template": "Апартаменты {} м²"},
    {"type": "таунхаус", "rooms": 3, "area_range": (140, 200), "title_template": "Таунхаус {} м²"},
    {"type": "дом", "rooms": 4, "area_range": (180, 250), "title_template": "Дом {} м²"}
]

# Обновляем свойства для создания разнообразия
for i, prop in enumerate(properties):
    # Выбираем случайный тип недвижимости
    prop_type = random.choice(property_types)
    
    # Обновляем данные объекта
    prop["type"] = prop_type["type"]
    prop["rooms"] = prop_type["rooms"]
    
    # Генерируем новую площадь в зависимости от типа
    new_area = round(random.uniform(*prop_type["area_range"]), 1)
    prop["area"] = new_area
    
    # Обновляем заголовок
    prop["title"] = prop_type["title_template"].format(new_area)
    
    # Корректируем цену в зависимости от площади и типа
    base_price_per_sqm = random.randint(120000, 180000)  # цена за м²
    
    # Коэффициенты для разных типов
    type_multipliers = {
        "студия": 1.0,
        "1-комн": 1.0,
        "2-комн": 0.95,
        "3-комн": 0.9,
        "4+-комн": 0.85,
        "пентхаус": 1.4,
        "апартаменты": 1.1,
        "таунхаус": 0.8,
        "дом": 0.7
    }
    
    multiplier = type_multipliers.get(prop["type"], 1.0)
    new_price = int(new_area * base_price_per_sqm * multiplier)
    prop["price"] = new_price
    
    # Обновляем изображение
    color_codes = {
        "студия": "FF9800",
        "1-комн": "4CAF50", 
        "2-комн": "2196F3",
        "3-комн": "9C27B0",
        "4+-комн": "F44336",
        "пентхаус": "FFD700",
        "апартаменты": "00BCD4",
        "таунхаус": "795548",
        "дом": "607D8B"
    }
    
    color = color_codes.get(prop["type"], "4CAF50")
    prop["image"] = f"https://via.placeholder.com/400x300/{color}/FFFFFF?text={prop['type']}+{new_area}м²"

# Сохраняем обновленные данные
with open('data/properties_expanded.json', 'w', encoding='utf-8') as f:
    json.dump(properties, f, ensure_ascii=False, indent=2)

print(f"Обновлено {len(properties)} объектов недвижимости с разнообразными типами")

# Подсчитываем статистику по типам
type_stats = {}
for prop in properties:
    prop_type = prop["type"]
    type_stats[prop_type] = type_stats.get(prop_type, 0) + 1

print("Статистика по типам:")
for prop_type, count in type_stats.items():
    print(f"  {prop_type}: {count} объектов")