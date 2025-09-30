#!/usr/bin/env python3
import json
import random

def update_expanded_properties():
    """Update properties_expanded.json with all fields for smart search"""
    
    # Load the expanded properties file that the app actually uses
    with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    print(f"Updating {len(properties)} properties in properties_expanded.json")
    
    # Define property types and classes for assignment  
    property_types = ['Квартира', 'Дом', 'Таунхаус', 'Пентхаус', 'Апартаменты']
    property_classes = ['Эконом', 'Комфорт', 'Бизнес', 'Премиум', 'Элит']
    wall_materials = ['Монолит', 'Кирпич', 'Панель', 'Монолит-кирпич', 'Газобетон']
    features_pool = ['Балкон', 'Лоджия', 'Парковка', 'Консьерж', 'Детская площадка', 'Спортзал', 'Закрытая территория']

    # Update each property with missing fields
    type_counter = {'дом': 0, 'таунхаус': 0, 'пентхаус': 0, 'апартаменты': 0}
    
    for i, prop in enumerate(properties):
        # Add property class based on price
        if 'property_class' not in prop or not prop.get('property_class'):
            price = prop.get('price', 0)
            if price < 3000000:
                prop['property_class'] = 'Эконом'
            elif price < 5000000:
                prop['property_class'] = 'Комфорт'
            elif price < 8000000:
                prop['property_class'] = 'Бизнес'
            elif price < 15000000:
                prop['property_class'] = 'Премиум'
            else:
                prop['property_class'] = 'Элит'
        
        # Add wall material if missing
        if 'wall_material' not in prop or not prop.get('wall_material'):
            prop['wall_material'] = prop.get('building_type', 'Монолит')
        
        # Add features if missing
        if 'features' not in prop or not prop.get('features'):
            features = []
            if prop.get('has_balcony'):
                features.append('Балкон')
            # Add features based on class
            if prop.get('property_class') in ['Премиум', 'Элит']:
                features.extend(['Парковка', 'Консьерж'])
            if prop.get('property_class') in ['Бизнес', 'Премиум', 'Элит']:
                features.append('Закрытая территория')
            prop['features'] = features
        
        # Add location if missing  
        if 'location' not in prop or not prop.get('location'):
            prop['location'] = prop.get('address', '')
        
        # Add complex name if missing
        if 'complex_name' not in prop or not prop.get('complex_name'):
            title = prop.get('title', '')
            if 'ЖК' in title:
                complex_start = title.find('ЖК')
                complex_part = title[complex_start:]
                if '»' in complex_part:
                    complex_name = complex_part[:complex_part.find('»') + 1]
                    prop['complex_name'] = complex_name
                else:
                    prop['complex_name'] = 'ЖК'
            else:
                prop['complex_name'] = ''
        
        # Set property type - keep most as apartments but diversify some
        if 'property_type' not in prop or not prop.get('property_type'):
            # Distribute property types based on index and some logic
            if i % 20 == 3 and type_counter['дом'] < 15:  # Every 20th starting at 3 = house
                prop['property_type'] = 'Дом'
                prop['title'] = f"Дом {prop.get('area', 200):.1f} м²"
                prop['rooms'] = 4
                type_counter['дом'] += 1
            elif i % 25 == 7 and type_counter['таунхаус'] < 10:  # Every 25th starting at 7 = townhouse
                prop['property_type'] = 'Таунхаус'
                prop['title'] = f"Таунхаус {prop.get('area', 180):.1f} м²"
                prop['rooms'] = 3
                type_counter['таунхаус'] += 1
            elif i % 30 == 12 and type_counter['пентхаус'] < 20:  # Every 30th starting at 12 = penthouse
                prop['property_type'] = 'Пентхаус'
                prop['title'] = f"Пентхаус {prop.get('area', 150):.1f} м²"
                prop['rooms'] = 3
                type_counter['пентхаус'] += 1
            elif i % 40 == 18 and type_counter['апартаменты'] < 8:  # Every 40th starting at 18 = apartments
                prop['property_type'] = 'Апартаменты'
                prop['title'] = f"Апартаменты {prop.get('area', 65):.1f} м²"
                type_counter['апартаменты'] += 1
            else:
                prop['property_type'] = 'Квартира'  # Default to apartment
        
        # Ensure all required fields exist
        required_fields = {
            'property_class': 'Комфорт',
            'wall_material': 'Монолит',
            'features': [],
            'location': '',
            'complex_name': ''
        }
        
        for field, default_value in required_fields.items():
            if field not in prop or not prop.get(field):
                prop[field] = default_value

    # Save updated properties
    with open('data/properties_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(properties, f, ensure_ascii=False, indent=2)
    
    print('Properties_expanded.json updated successfully!')
    print(f'Total properties: {len(properties)}')
    
    # Show summary of property types and classes
    property_type_counts = {}
    property_class_counts = {}
    
    for prop in properties:
        prop_type = prop.get('property_type', 'Квартира')
        property_type_counts[prop_type] = property_type_counts.get(prop_type, 0) + 1
        
        prop_class = prop.get('property_class', 'Комфорт')
        property_class_counts[prop_class] = property_class_counts.get(prop_class, 0) + 1
    
    print('\nProperty types distribution:')
    for prop_type, count in property_type_counts.items():
        print(f'  {prop_type}: {count}')
        
    print('\nProperty classes distribution:')
    for prop_class, count in property_class_counts.items():
        print(f'  {prop_class}: {count}')

if __name__ == '__main__':
    update_expanded_properties()