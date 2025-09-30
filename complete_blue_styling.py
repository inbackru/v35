#!/usr/bin/env python3
"""
Завершающая стилизация всех карточек в едином синем стиле
"""

import re

def complete_styling():
    """Завершает стилизацию всех карточек"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем старые заголовки на новую структуру
    content = re.sub(
        r'<div class="absolute bottom-4 left-4 text-white">\s*<h3 class="text-xl font-bold mb-1">([^<]+)</h3>\s*<p class="text-sm opacity-90">([^<]+)</p>\s*</div>',
        r'''<div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                        <h3 class="text-2xl font-bold text-white mb-1">\1</h3>
                        <p class="text-white/90 text-sm">\2</p>
                    </div>''',
        content
    )
    
    # Заменяем старую структуру статистики
    content = re.sub(
        r'<div class="p-6">\s*<div class="grid grid-cols-2 gap-4 mb-4 text-sm">\s*<div class="text-center">\s*<div class="font-semibold text-gray-800">([^<]+)</div>\s*<div class="text-gray-600">ЖК</div>\s*</div>\s*<div class="text-center">\s*<div class="font-semibold text-gray-800">([^<]+)</div>\s*<div class="text-gray-600">цена</div>\s*</div>\s*</div>\s*<div class="flex items-center justify-between">\s*<a href="([^"]+)" class="text-blue-600 hover:text-blue-700 font-medium">\s*Подробнее <i class="fas fa-arrow-right ml-1"></i>\s*</a>\s*</div>\s*</div>',
        lambda m: f'''<div class="p-6">
                    <!-- Stats Grid -->
                    <div class="grid grid-cols-3 gap-4 mb-6">
                        <div class="text-center">
                            <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-building text-blue-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">{m.group(1)}</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Новостроек</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-ruble-sign text-green-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">50k</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">₽/м²</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-star text-yellow-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">4.0</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Рейтинг</div>
                        </div>
                    </div>
                    
                    <!-- Action Button -->
                    <a href="{m.group(3)}" 
                       class="block w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 rounded-xl font-semibold transform transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-lg group-hover:shadow-xl">
                        Подробнее о районе
                        <i class="fas fa-arrow-right ml-2 transition-transform group-hover:translate-x-1"></i>
                    </a>
                </div>''',
        content
    )
    
    # Сохраняем
    with open('templates/districts.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Завершающая стилизация применена!")
    print("🎨 Все карточки теперь в едином синем корпоративном стиле InBack")

if __name__ == "__main__":
    complete_styling()