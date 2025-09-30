#!/usr/bin/env python3
"""
Исправление поломанной структуры HTML после массового обновления
"""

import re

def fix_html_structure():
    """Исправляет поломанную структуру HTML"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем незакрытые теги изображений
    content = re.sub(
        r'<div class="absolute inset-0 bg-cover bg-center opacity-40" style="background-image: url\([^)]+\);">\s*<div class="absolute inset-0 bg-black bg-opacity-20"></div>',
        lambda m: m.group(0).replace('opacity-40" style=', 'opacity-40" style=').replace(';">', ';">'),
        content
    )
    
    # Исправляем все сломанные теги
    content = re.sub(
        r'<div class="absolute inset-0 bg-cover bg-center opacity-40" style="background-image: url\([^)]+\);">([^<]*)<div class="absolute inset-0 bg-black bg-opacity-20"></div>',
        r'<div class="absolute inset-0 bg-cover bg-center opacity-40" style=\g<1>"></div>',
        content
    )
    
    # Добавляем комментарии для секций Content там где их нет
    content = re.sub(
        r'</div>\s*<div class="p-6">\s*<!-- Stats Grid -->',
        r'</div>\n                \n                <!-- Content -->\n                <div class="p-6">\n                    <!-- Stats Grid -->',
        content
    )
    
    # Убираем дублированные секции
    content = re.sub(
        r'<!-- Content -->\s*<!-- Content -->',
        '<!-- Content -->',
        content
    )
    
    # Исправляем некорректные ссылки на изображения
    content = re.sub(
        r'background-image: url\(\'([^\']+)\'\);">\s*</div>',
        r'background-image: url(\'\1\');"></div>',
        content
    )
    
    print("🔧 Исправляю структуру HTML...")
    
    # Сохраняем исправленную версию
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ HTML структура исправлена!")

if __name__ == "__main__":
    fix_html_structure()