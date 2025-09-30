#!/usr/bin/env python3
"""
Проверка и исправление соответствия ссылок районов
"""

import re

def check_district_links():
    """Проверяет соответствие названий районов и их ссылок"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все карточки и извлекаем название и ссылку
    card_pattern = r'<!-- ([^-]+?) -->[^<]*<div[^>]*data-district="([^"]+)"[^>]*>.*?href="{{ url_for\(\'district_detail\', district=\'([^\']+)\'\) }}"'
    
    matches = re.findall(card_pattern, content, re.DOTALL)
    
    print("🔍 Проверяю соответствие ссылок районов:\n")
    
    # Правильные соответствия район -> route
    correct_mappings = {
        'Центральный': 'tsentralnyy',
        '40 лет Победы': '40-let-pobedy', 
        '9-й километр': '9i-kilometr',
        'Авиагородок': 'aviagorodok',
        'Аврора': 'avrora',
        'Фестивальный район': 'festivalny',
        'Баскет-Холл': 'basket-hall',
        'Березовый': 'berezovy',
        'Западный район': 'zapadny',
        'Карасунский район': 'karasunsky',
        'Прикубанский район': 'prikubansky',
        'Юбилейный район': 'yubileyny',
        'Гидростроителей район': 'gidrostroitelei',
        'Солнечный район': 'solnechny',
        'Музыкальный район': 'muzykalny',
        'Панорама район': 'panorama',
        'Комсомольский район': 'komsomolsky',
        'Прикубанский внутренний город': 'prikubansky-vnutrenny',
        'Дубинка': 'dubinka',
        'Черемушки': 'cheremushki',
        'Калинино': 'kalinino',
        'Пашковский': 'pashkovsky',
        'Старокорсунская': 'starokorsunskaya',
        'Горхутор': 'gorkhutor',
        'ХБК (Хлопчатобумажный комбинат)': 'khbk',
        'ККБ (Краснодарский кожевенный комбинат)': 'kkb',
        'Колосистый': 'kolosisty',
        'Кожзавод': 'kozhzavod',
        'Западный обход': 'zapadny-obkhod',
        'ЗИП Жукова (Завод имени Жукова)': 'zip-zhukova',
        'Немецкая деревня': 'nemetskaya-derevnya',
        'Новознаменский': 'novoznamensky',
        'Покровка': 'pokrovka',
        'Район аэропорта': 'aeroport',
        'Репино': 'repino',
        'Северный': 'severny',
        'Школьный': 'shkolny',
        'Славянский 2': 'slavyansky-2',
        'Славянский': 'slavyansky',
        'Табачная фабрика': 'tabachnaya-fabrika',
        'ТЭЦ (Теплоэлектроцентраль)': 'tets',
        'Вавилова': 'vavilova',
        'Яблоновский': 'yablonovsky',
        'Западный округ': 'zapadny-okrug'
    }
    
    issues = []
    for name, data_attr, route in matches:
        name = name.strip()
        expected_route = correct_mappings.get(name, 'UNKNOWN')
        
        if route != expected_route:
            issues.append({
                'name': name,
                'current_route': route,
                'expected_route': expected_route,
                'data_attr': data_attr
            })
            print(f"❌ {name}: {route} → должно быть {expected_route}")
        else:
            print(f"✅ {name}: {route}")
    
    print(f"\n📊 Найдено {len(issues)} несоответствий из {len(matches)} районов")
    
    if issues:
        print("\n🔧 Исправляю ссылки...")
        
        # Исправляем каждую проблемную ссылку
        for issue in issues:
            # Находим и заменяем некорректную ссылку
            old_pattern = f"<!-- {re.escape(issue['name'])} -->.*?district='{re.escape(issue['current_route'])}'"
            new_route = f"district='{issue['expected_route']}'"
            
            content = re.sub(
                f"(<!-- {re.escape(issue['name'])} -->.*?district=')({re.escape(issue['current_route'])})(')",
                f"\\g<1>{issue['expected_route']}\\g<3>",
                content,
                flags=re.DOTALL
            )
        
        # Сохраняем исправления
        with open('templates/districts.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Все ссылки исправлены!")
    else:
        print("✅ Все ссылки корректны!")

if __name__ == "__main__":
    check_district_links()