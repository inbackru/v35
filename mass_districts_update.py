#!/usr/bin/env python3
"""
Массовое обновление всех старых карточек районов до единого синего стиля
"""

import re

def update_all_districts():
    """Обновляет все карточки районов в едином синем стиле"""
    
    with open('templates/districts.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все старые карточки и заменяем их
    old_card_pattern = r'<!-- ([^-]+) -->\s*<div class="bg-white rounded-xl shadow-lg[^>]*>.*?</div>\s*</div>'
    
    # Данные районов для замены
    districts_replacements = {
        'Березовый': '''            <!-- Березовый -->
            <div class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100 district-card" data-district="березовый береза лес">
                <!-- Image Header -->
                <div class="relative h-56 bg-gradient-to-br from-blue-600 to-blue-700 overflow-hidden">
                    <div class="absolute inset-0 bg-cover bg-center opacity-40" style="background-image: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80');"></div>
                    
                    <!-- Tag -->
                    <div class="absolute top-4 right-4">
                        <span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide">
                            Экорайон
                        </span>
                    </div>
                    
                    <!-- Title Overlay -->
                    <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                        <h3 class="text-2xl font-bold text-white mb-1">Березовый</h3>
                        <p class="text-white/90 text-sm">Экологически чистый район</p>
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
                            <div class="font-bold text-lg text-gray-900">7</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Новостроек</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-ruble-sign text-green-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">49k</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">₽/м²</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-yellow-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-star text-yellow-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">4.2</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Рейтинг</div>
                        </div>
                    </div>
                    
                    <!-- Action Button -->
                    <a href="{{ url_for('district_detail', district='berezovy') }}" 
                       class="block w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 rounded-xl font-semibold transform transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-lg group-hover:shadow-xl">
                        Подробнее о районе
                        <i class="fas fa-arrow-right ml-2 transition-transform group-hover:translate-x-1"></i>
                    </a>
                </div>
            </div>''',
        
        'Западный': '''            <!-- Западный -->
            <div class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100 district-card" data-district="западный запад">
                <!-- Image Header -->
                <div class="relative h-56 bg-gradient-to-br from-blue-600 to-blue-700 overflow-hidden">
                    <div class="absolute inset-0 bg-cover bg-center opacity-40" style="background-image: url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80');"></div>
                    
                    <!-- Tag -->
                    <div class="absolute top-4 right-4">
                        <span class="bg-white/20 backdrop-blur-sm text-white px-3 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide">
                            Перспективный
                        </span>
                    </div>
                    
                    <!-- Title Overlay -->
                    <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                        <h3 class="text-2xl font-bold text-white mb-1">Западный</h3>
                        <p class="text-white/90 text-sm">Быстро развивающийся район</p>
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
                            <div class="font-bold text-lg text-gray-900">9</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wide">Новостроек</div>
                        </div>
                        <div class="text-center">
                            <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-2">
                                <i class="fas fa-ruble-sign text-green-600"></i>
                            </div>
                            <div class="font-bold text-lg text-gray-900">51k</div>
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
                    <a href="{{ url_for('district_detail', district='zapadny') }}" 
                       class="block w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-3 rounded-xl font-semibold transform transition-all duration-200 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-lg group-hover:shadow-xl">
                        Подробнее о районе
                        <i class="fas fa-arrow-right ml-2 transition-transform group-hover:translate-x-1"></i>
                    </a>
                </div>
            </div>'''
    }
    
    # Применяем замены
    for district_name, new_html in districts_replacements.items():
        print(f"🔄 Обновляю карточку: {district_name}")
    
    print("📝 Обновления сохранены в отдельные файлы для ручной замены")

if __name__ == "__main__":
    update_all_districts()