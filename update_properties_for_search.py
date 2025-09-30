#!/usr/bin/env python3
import json

def update_properties_structure():
    """Update properties with additional fields for smart search"""
    
    # Load current properties
    with open('data/properties.json', 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    # Define property categories for smart search
    property_classes = ['Эконом', 'Комфорт', 'Бизнес', 'Премиум', 'Элит']
    wall_materials = ['Монолит', 'Кирпич', 'Панель', 'Монолит-кирпич', 'Газобетон']
    features_list = ['Балкон', 'Лоджия', 'Парковка', 'Консьерж', 'Детская площадка', 'Спортзал', 'Закрытая территория']

    # Update each property with missing fields
    for i, prop in enumerate(properties):
        # Add property class if missing
        if 'property_class' not in prop:
            # Assign based on price range
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
        if 'wall_material' not in prop:
            prop['wall_material'] = prop.get('building_type', 'Монолит')
        
        # Add features array if missing
        if 'features' not in prop:
            features = []
            if prop.get('has_balcony'):
                features.append('Балкон')
            # Assign some features based on property class
            if prop.get('property_class') in ['Премиум', 'Элит']:
                features.extend(['Парковка', 'Консьерж'])
            if prop.get('property_class') in ['Бизнес', 'Премиум', 'Элит']:
                features.append('Закрытая территория')
            prop['features'] = features
        
        # Add location if missing
        if 'location' not in prop:
            prop['location'] = prop.get('address', '')
        
        # Add complex name if missing
        if 'complex_name' not in prop:
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
        
        # Update specific properties to include houses for testing
        if i == 2:  # Property ID 3 - make it a house
            prop['title'] = 'Дом 233.3 м² в ЖК «Седьмое небо»'
            prop['property_type'] = 'Дом'
            prop['rooms'] = 4
            prop['area'] = 233.3
            prop['price'] = 22032642
            prop['district'] = 'Западный'
            prop['features'] = ['Парковка', 'Закрытая территория', 'Детская площадка']
            
        elif i == 4:  # Property ID 5 - make it a townhouse
            prop['title'] = 'Таунхаус 195.7 м² в ЖК «Панорама»'
            prop['property_type'] = 'Таунхаус'
            prop['rooms'] = 3
            prop['area'] = 195.7
            prop['price'] = 21772955
            prop['district'] = 'Прикубанский округ'
            prop['features'] = ['Парковка', 'Балкон', 'Закрытая территория']
            
        elif i == 6:  # Property ID 7 - make it a penthouse
            prop['title'] = 'Пентхаус 177.6 м² в ЖК «Северный ветер»'
            prop['property_type'] = 'Пентхаус'
            prop['rooms'] = 3
            prop['area'] = 177.6
            prop['price'] = 18761237
            prop['features'] = ['Лоджия', 'Парковка', 'Консьерж', 'Спортзал']
            
        elif i == 8:  # Property ID 9 - make it apartments
            prop['title'] = 'Апартаменты 65.4 м² в апарт-комплексе'
            prop['property_type'] = 'Апартаменты'
            prop['rooms'] = 2
            prop['features'] = ['Консьерж', 'Спортзал', 'Закрытая территория']
        
        # Ensure all required fields exist
        required_fields = {
            'property_class': 'Комфорт',
            'wall_material': 'Монолит',
            'features': [],
            'location': '',
            'complex_name': ''
        }
        
        for field, default_value in required_fields.items():
            if field not in prop:
                prop[field] = default_value

    # Save updated properties
    with open('data/properties.json', 'w', encoding='utf-8') as f:
        json.dump(properties, f, ensure_ascii=False, indent=2)
    
    print(f'Properties updated successfully!')
    print(f'Total properties: {len(properties)}')
    
    # Show summary of property types
    property_type_counts = {}
    for prop in properties:
        prop_type = prop.get('property_type', 'Квартира')
        property_type_counts[prop_type] = property_type_counts.get(prop_type, 0) + 1
    
    print('\nProperty types distribution:')
    for prop_type, count in property_type_counts.items():
        print(f'  {prop_type}: {count}')

if __name__ == '__main__':
    update_properties_structure()