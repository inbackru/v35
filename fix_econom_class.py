#!/usr/bin/env python3
import json

# Load properties
with open('data/properties_expanded.json', 'r', encoding='utf-8') as f:
    properties = json.load(f)

# Change some cheapest properties to Econom class
count = 0
for prop in properties:
    if prop.get('price', 0) < 2500000 and count < 15:  # First 15 cheapest
        prop['property_class'] = 'Эконом'
        count += 1

# Save updated data
with open('data/properties_expanded.json', 'w', encoding='utf-8') as f:
    json.dump(properties, f, ensure_ascii=False, indent=2)

# Count classes
class_counts = {}
for prop in properties:
    cls = prop.get('property_class', 'Unknown')
    class_counts[cls] = class_counts.get(cls, 0) + 1

print('Fixed class distribution:')
for cls, count in class_counts.items():
    print(f'  {cls}: {count}')