#!/usr/bin/env python3
import json

def debug_search():
    """Debug search filtering"""
    
    # Load properties
    with open('data/properties.json', 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    print(f"Total properties loaded: {len(properties)}")
    print()
    
    # Check property classes distribution
    class_counts = {}
    for prop in properties:
        prop_class = prop.get('property_class', 'Unknown')
        class_counts[prop_class] = class_counts.get(prop_class, 0) + 1
    
    print("Property class distribution:")
    for cls, count in class_counts.items():
        print(f"  {cls}: {count}")
    print()
    
    # Test class filtering manually
    test_keyword = "Комфорт"
    matching_props = []
    for prop in properties:
        prop_class = prop.get('property_class', '')
        if test_keyword.lower() == prop_class.lower():
            matching_props.append(prop)
    
    print(f"Manual filter test for '{test_keyword}':")
    print(f"Found {len(matching_props)} matching properties")
    for prop in matching_props[:3]:
        print(f"  - ID {prop['id']}: {prop['title']} (class: {prop.get('property_class')})")
    print()
    
    # Test with different classes
    for test_class in ['Эконом', 'Бизнес', 'Премиум']:
        matching = [p for p in properties if p.get('property_class', '').lower() == test_class.lower()]
        print(f"'{test_class}': {len(matching)} properties")

if __name__ == '__main__':
    debug_search()