#!/usr/bin/env python3
"""
Script to update properties database with real residential complexes
Replaces test names like "Комплекс-8" with actual ЖК names from our database
"""
import json
import random
from datetime import datetime

def load_real_complexes():
    """Load real residential complexes from our database"""
    with open('static/data/residential_complexes_expanded.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_current_properties():
    """Load current properties database"""
    with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_realistic_properties(complexes, target_count=200):
    """Generate realistic properties based on our real complexes"""
    properties = []
    property_id = 1
    
    for complex_data in complexes:
        # Generate 5-8 properties per complex
        properties_per_complex = random.randint(5, 8)
        
        for i in range(properties_per_complex):
            # Room configurations based on complex type
            if complex_data['building_class'] == 'эконом':
                room_options = [0, 1, 2, 3]  # More studios and 1-2 room
                room_weights = [0.2, 0.4, 0.3, 0.1]
            elif complex_data['building_class'] == 'комфорт':
                room_options = [1, 2, 3, 4]  # Balanced
                room_weights = [0.3, 0.4, 0.2, 0.1]
            else:  # Premium/business
                room_options = [2, 3, 4, 5]  # Larger apartments
                room_weights = [0.3, 0.3, 0.3, 0.1]
                
            rooms = random.choices(room_options, weights=room_weights)[0]
            
            # Generate realistic area based on rooms
            if rooms == 0:  # Studio
                area = round(random.uniform(25, 45), 1)
            elif rooms == 1:
                area = round(random.uniform(35, 55), 1)
            elif rooms == 2:
                area = round(random.uniform(50, 80), 1)
            elif rooms == 3:
                area = round(random.uniform(70, 120), 1)
            elif rooms == 4:
                area = round(random.uniform(90, 150), 1)
            else:  # 5+ rooms
                area = round(random.uniform(130, 200), 1)
            
            # Calculate price based on complex price range and area
            price_per_sqm = random.uniform(
                complex_data['price_from'] / 50,  # Assuming 50sqm average
                complex_data['price_to'] / 100    # Assuming 100sqm average
            )
            price = round(area * price_per_sqm)
            
            # Floor (random within complex range)
            floor = random.randint(2, complex_data['floors_max'] - 1)
            
            property_data = {
                "id": property_id,
                "rooms": rooms,
                "area": area,
                "price": price,
                "floor": floor,
                "total_floors": complex_data['floors_max'],
                "residential_complex": complex_data['name'],
                "residential_complex_id": complex_data['id'],
                "district": complex_data['district'],
                "developer": complex_data['developer'],
                "coordinates": complex_data['coordinates'],
                "building_class": complex_data['building_class'],
                "completion_date": complex_data['completion_date'],
                "status": complex_data['status'],
                "cashback_percent": complex_data.get('cashback_percent', 5),
                "image": f"https://via.placeholder.com/400x300/f3f4f6/9ca3af?text={rooms}-комн+{area}м²",
                "created_at": datetime.now().isoformat(),
                "mortgage_available": True,
                "parking": random.choice([True, False]),
                "balcony": random.choice([True, False]),
                "renovation": random.choice(['без отделки', 'предчистовая', 'чистовая'])
            }
            
            properties.append(property_data)
            property_id += 1
            
            # Don't exceed target count
            if len(properties) >= target_count:
                return properties
    
    return properties

def update_properties_database():
    """Main function to update properties with real complexes"""
    print("🏗️ Загружаю реальные ЖК...")
    complexes = load_real_complexes()
    print(f"✅ Загружено {len(complexes)} реальных ЖК")
    
    print("🏠 Генерирую новую базу недвижимости с реальными ЖК...")
    new_properties = generate_realistic_properties(complexes, target_count=200)
    print(f"✅ Создано {len(new_properties)} объектов недвижимости")
    
    # Backup old file
    import shutil
    shutil.copy('data/properties_expanded.json', 'data/properties_expanded_backup.json')
    print("💾 Создан backup старой базы")
    
    # Save new properties
    with open('data/properties_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(new_properties, f, ensure_ascii=False, indent=2)
    print("✅ Новая база недвижимости сохранена")
    
    # Show statistics
    print("\n📊 Статистика новой базы:")
    complex_counts = {}
    district_counts = {}
    room_counts = {}
    
    for prop in new_properties:
        # Count by complex
        complex_name = prop['residential_complex']
        complex_counts[complex_name] = complex_counts.get(complex_name, 0) + 1
        
        # Count by district
        district = prop['district']
        district_counts[district] = district_counts.get(district, 0) + 1
        
        # Count by rooms
        rooms = prop['rooms']
        room_counts[rooms] = room_counts.get(rooms, 0) + 1
    
    print(f"🏢 Топ-5 ЖК по количеству объектов:")
    for complex_name, count in sorted(complex_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {complex_name}: {count} объектов")
    
    print(f"🗺️ Распределение по районам:")
    for district, count in sorted(district_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {district}: {count} объектов")
    
    print(f"🏠 Распределение по комнатности:")
    for rooms in sorted(room_counts.keys()):
        room_text = 'Студия' if rooms == 0 else f"{rooms}-комн"
        print(f"   {room_text}: {room_counts[rooms]} объектов")
    
    print(f"\n💰 Ценовой диапазон: {min(p['price'] for p in new_properties):,} - {max(p['price'] for p in new_properties):,} ₽")
    print(f"📐 Площадь: {min(p['area'] for p in new_properties):.1f} - {max(p['area'] for p in new_properties):.1f} м²")
    
    print("\n🎉 База недвижимости успешно обновлена реальными ЖК!")

if __name__ == "__main__":
    update_properties_database()