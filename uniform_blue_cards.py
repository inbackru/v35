#!/usr/bin/env python3
"""
Обновление всех карточек районов до единого синего корпоративного стиля InBack
"""

def create_uniform_blue_card(name, slug_attrs, description, tag, image_url, buildings, price, rating, route_name):
    """Создает HTML для единообразной синей карточки района"""
    return f'''            <!-- {name} -->
            <div class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100 district-card" data-district="{slug_attrs}">
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
                        <h3 class="text-2xl font-bold text-white mb-1">{name}</h3>
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

# Данные всех районов для единого оформления
districts_data = [
    # Уже обновленные - приведем к синему стилю
    ('Центральный', 'центральный центр', 'Исторический центр Краснодара', 'Центр города', 
     'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
     '12', '75', '5.0', 'tsentralnyy'),
    
    ('40 лет Победы', '40 лет победы сорок победа', 'Район с богатой историей', 'Исторический',
     'https://images.unsplash.com/photo-1590736969955-71cc94901144?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '8', '58', '4.2', '40-let-pobedy'),
    
    ('9-й километр', '9 километр девятый', 'Крупнейший торговый район', 'Торговый центр',
     'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '6', '52', '4.0', '9i-kilometr'),
    
    ('Авиагородок', 'авиагородок авиа аэропорт', 'Престижный авиационный район', 'Авиационный',
     'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '4', '56', '4.3', 'aviagorodok'),
    
    ('Аврора', 'аврора утренняя заря', 'Уютный жилой микрорайон', 'Уютный',
     'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '5', '54', '4.1', 'avrora'),
    
    ('Фестивальный', 'фестивальный фестиваль', 'Культурный центр города', 'Культурный',
     'https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '18', '68', '5.0', 'festivalny'),
    
    # Новые карточки для обновления
    ('Баскет-Холл', 'баскет холл баскетбол спорт', 'Современный спортивный район', 'Спортивный',
     'https://images.unsplash.com/photo-1574923226119-24e8495ba4ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '3', '62', '4.4', 'basket-hall'),
    
    ('Березовый', 'березовый береза лес', 'Экологически чистый район', 'Экорайон',
     'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '7', '49', '4.2', 'berezovy'),
    
    ('Западный', 'западный запад', 'Быстро развивающийся район', 'Перспективный',
     'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '9', '51', '4.0', 'zapadny'),
    
    ('Комсомольский', 'комсомольский молодежный', 'Молодежный активный район', 'Молодежный',
     'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '6', '47', '3.9', 'komsomolsky'),
    
    ('Прикубанский', 'прикубанский кубань река', 'Престижный район у реки', 'Престижный',
     'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '11', '67', '4.5', 'prikubansky'),
    
    ('Юбилейный', 'юбилейный праздничный', 'Торжественный микрорайон', 'Торжественный',
     'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
     '4', '53', '4.0', 'yubileyny')
]

def main():
    """Создает все карточки в едином синем стиле"""
    print("🎨 Создаю карточки районов в едином синем корпоративном стиле InBack...")
    
    for i, district_data in enumerate(districts_data):
        card_html = create_uniform_blue_card(*district_data)
        filename = f'blue_card_{i+1}_{district_data[0].lower().replace(" ", "_").replace("-", "_")}.html'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(card_html)
    
    print(f"✅ Создано {len(districts_data)} карточек в едином синем стиле")
    print("📋 Список созданных карточек:")
    for i, (name, _, _, _, _, _, _, _, _) in enumerate(districts_data):
        print(f"  {i+1}. {name}")

if __name__ == "__main__":
    main()