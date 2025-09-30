#!/usr/bin/env python3
"""
Массовое обновление ВСЕХ старых карточек районов до единого синего стиля InBack
"""

import re

def create_blue_card(district_name, data_district, description, tag, image_url, buildings, price, rating, route_name):
    """Создает HTML для единообразной синей карточки района"""
    return f'''            <!-- {district_name} -->
            <div class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100 district-card" data-district="{data_district}">
                <!-- Image Header -->
                <div class="relative h-56 bg-gradient-to-br from-blue-600 to-blue-700 overflow-hidden">
                    <div class="absolute inset-0 bg-cover bg-center opacity-40" style="background-image: url('{image_url}');"></div>
                    
                    <!-- Tag -->
                    <div class="absolute top-4 right-4">
                        <span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide">
                            {tag}
                        </span>
                    </div>
                    
                    <!-- Title Overlay -->
                    <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                        <h3 class="text-2xl font-bold text-white mb-1">{district_name}</h3>
                        <p class="text-white/90 text-sm">{description}</p>
                    </div>
                </div>
                
                <!-- Content -->
                <div class="p-6">
                    <!-- Stats Grid -->
                    <div class="grid grid-cols-3 gap-4 mb-6">
                        <div class="text-center">
                            <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-building text-blue-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">{buildings}</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Новостроек</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-ruble-sign text-green-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">{price}k</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">₽/м²</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-star text-yellow-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">{rating}</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Рейтинг</div>
                        </div>
                    </div>
                    
                    <!-- Action Button -->
                    <a href="{{{{ url_for('district_detail', district='{route_name}') }}}}" 
                       class="block w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 rounded-xl font-semibold transform transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-lg group-hover:shadow-xl">
                        Подробнее о районе
                        <i class="fas fa-arrow-right ml-2 transition-transform group-hover:translate-x-1"></i>
                    </a>
                </div>
            </div>'''

def mass_update_districts():
    """Массово обновляет все старые карточки"""
    
    # Читаем файл
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Паттерн для поиска старых карточек
    old_card_pattern = r'            <!-- ([^-]+?) -->\s*\n            <div class="bg-white rounded-xl shadow-lg[^>]*?>.*?</div>\s*</div>'
    
    # Найдем все старые карточки
    matches = re.findall(old_card_pattern, content, re.DOTALL)
    print(f"Найдено {len(matches)} старых карточек для обновления:")
    for match in matches:
        print(f"  - {match.strip()}")
    
    # Заменяем все старые карточки разом
    updated_content = re.sub(
        r'<div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:-translate-y-2',
        '<div class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100',
        content
    )
    
    # Обновляем header градиенты на синие
    updated_content = re.sub(
        r'<div class="h-48 bg-cover bg-center relative"',
        '<div class="relative h-56 bg-gradient-to-br from-blue-600 to-blue-700 overflow-hidden">\n                    <div class="absolute inset-0 bg-cover bg-center opacity-40"',
        updated_content
    )
    
    # Обновляем старую структуру на новую
    updated_content = re.sub(
        r'<div class="absolute top-4 right-4">\s*<span class="bg-white bg-opacity-20 text-white px-3 py-1 rounded-full text-sm font-medium">([^<]+)</span>\s*</div>',
        r'''<div class="absolute top-4 right-4">
                        <span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide">
                            \1
                        </span>
                    </div>''',
        updated_content
    )
    
    # Сохраняем
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Массовое обновление завершено!")

if __name__ == "__main__":
    mass_update_districts()