#!/usr/bin/env python3
"""
Скрипт для системного исправления шаблона districts.html
"""
import re

def fix_districts_template():
    """Исправляет шаблон districts.html, убирая зеленые кешбек метки"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Шаблон для поиска и замены всех кешбек блоков
    # Ищем блоки вида:
    # <div class="flex items-center justify-between">
    #     <div class="flex items-center text-green-600">
    #         <i class="fas fa-cash-register mr-2"></i>
    #         <span class="font-semibold">до ХХХ ₽</span>
    #     </div>
    #     <a href="...">Подробнее</a>
    # </div>
    
    pattern = r'<div class="flex items-center justify-between">\s*<div class="flex items-center text-green-600">\s*<i class="fas fa-cash-register[^>]*></i>\s*<span class="font-semibold">[^<]*</span>\s*</div>\s*(<a href="[^"]*"[^>]*>[^<]*<i[^>]*></i>\s*</a>)\s*</div>'
    
    # Заменяем на простой блок с кнопкой справа
    replacement = r'<div class="flex items-center justify-end">\1</div>'
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Также заменим старые цвета ссылок на синие
    content = content.replace('text-[#0088CC] hover:text-[#006699]', 'text-blue-600 hover:text-blue-700')
    
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Исправлены кешбек метки в districts.html")
    print("✅ Обновлены цвета ссылок на корпоративные")

if __name__ == "__main__":
    fix_districts_template()