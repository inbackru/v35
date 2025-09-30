#!/usr/bin/env python3
"""
Упрощенный генератор sitemap для InBack.ru
Создает полную карту сайта без зависимости от Flask url_for
"""

import os
import json
import re
from datetime import datetime
from urllib.parse import quote

def clean_url_part(text):
    """Очищает текст для использования в URL"""
    if not text:
        return ""
    # Убираем специальные символы и заменяем пробелы на дефисы
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9а-яё\s\-.]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    return quote(text.encode('utf-8'))

def get_streets_data():
    """Получаем данные по всем улицам"""
    streets = []
    try:
        with open('data/streets.json', 'r', encoding='utf-8') as f:
            streets_data = json.load(f)
            # Сортируем по количеству объектов (популярные сначала) и берем ВСЕ улицы
            sorted_streets = sorted(streets_data, key=lambda x: x.get('properties_count', 0), reverse=True)
            streets = [street['name'] for street in sorted_streets if street.get('name')]
    except Exception as e:
        print(f"Error loading streets: {e}")
    return streets

def generate_full_sitemap():
    """Создание полной XML карты сайта"""
    
    print("🔄 Создание полной карты сайта InBack.ru...")
    
    base_url = "https://inback.ru"
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''

    url_count = 0
    
    # 1. Главные страницы (высокий приоритет)
    main_pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'url': '/properties', 'priority': '0.9', 'changefreq': 'daily'},
        {'url': '/residential-complexes', 'priority': '0.9', 'changefreq': 'daily'},
        {'url': '/developers', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': '/map', 'priority': '0.8', 'changefreq': 'weekly'},
    ]
    
    # 2. О компании
    company_pages = [
        {'url': '/about', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/how-it-works', 'priority': '0.8', 'changefreq': 'monthly'},
        {'url': '/reviews', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': '/contacts', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/security', 'priority': '0.6', 'changefreq': 'monthly'},
        {'url': '/careers', 'priority': '0.5', 'changefreq': 'monthly'},
    ]
    
    # 3. Контент
    content_pages = [
        {'url': '/blog', 'priority': '0.8', 'changefreq': 'daily'},
        {'url': '/news', 'priority': '0.7', 'changefreq': 'daily'},
        {'url': '/streets', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': '/districts', 'priority': '0.7', 'changefreq': 'weekly'},
    ]
    
    # 4. Ипотека
    mortgage_pages = [
        {'url': '/ipoteka', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': '/family-mortgage', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/it-mortgage', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/military-mortgage', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/developer-mortgage', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/maternal-capital', 'priority': '0.7', 'changefreq': 'monthly'},
    ]
    
    # 5. Сервисные страницы
    service_pages = [
        {'url': '/comparison', 'priority': '0.6', 'changefreq': 'weekly'},
        {'url': '/complex-comparison', 'priority': '0.6', 'changefreq': 'weekly'},
        {'url': '/favorites', 'priority': '0.5', 'changefreq': 'daily'},
        {'url': '/thank-you', 'priority': '0.3', 'changefreq': 'yearly'},
    ]
    
    # 6. Районы Краснодара
    districts = [
        'tsentralnyy', 'zapadny', 'karasunsky', 'festivalny', 'gidrostroitelei', 
        'yubileynyy', 'pashkovsky', 'prikubansky', 'enka', 'solnechny', 
        'panorama', 'vavilova', 'yablonovskiy', 'uchhoz-kuban', 'dubinka',
        'komsomolsky', 'kolosistiy', 'kozhzavod', 'kubansky', 'krasnodarskiy',
        'aviagorodok', 'avrora', 'basket-hall', 'berezovy', 'cheremushki', 
        'gorkhutor', 'hbk', 'kalinino', 'kkb', 'ksk', 'krasnaya-ploshad', 
        '40-let-pobedy', 'tsiolkovskogo', 'stasova', 'kalinovaya', 
        'kotliarevskogo', 'akademika-lukianenko', 'starokorsunskaya',
        'im-40-letiya-pobedy', 'rossiyskaya', 'turgenevsky', 'slavyansky',
        'novorossiysky', 'tbilissky', 'severo-kavkazsky', 'adygeysky',
        'prochorzhsky', 'kievsky', 'dneprovskiy', 'moldavsky', 'sovetsky',
        'universitetsky', 'industrialny', 'shevchenko'
    ]
    
    # 7. Категории блога
    blog_categories = ['cashback', 'districts', 'mortgage', 'market', 'legal', 'tips']
    
    # Добавление всех страниц в sitemap
    all_pages = main_pages + company_pages + content_pages + mortgage_pages + service_pages
    
    print("📄 Добавление основных страниц...")
    for page in all_pages:
        sitemap_xml += f'''  <url>
    <loc>{base_url}{page['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
'''
        url_count += 1
    
    # Добавление районов
    print("📍 Добавление районов...")
    for district in districts:
        sitemap_xml += f'''  <url>
    <loc>{base_url}/districts/{district}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
        url_count += 1
    
    # Добавление всех улиц
    print("🛣️ Добавление всех улиц Краснодара...")
    streets = get_streets_data()
    print(f"Найдено {len(streets)} улиц для sitemap")
    for street_name in streets:
        street_slug = clean_url_part(street_name)
        if street_slug:
            sitemap_xml += f'''  <url>
    <loc>{base_url}/streets/{street_slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
'''
            url_count += 1
    
    # Добавление категорий блога
    print("📝 Добавление категорий блога...")
    for category in blog_categories:
        sitemap_xml += f'''  <url>
    <loc>{base_url}/blog/category/{category}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
'''
        url_count += 1
    
    # Добавление примерных объектов недвижимости (ID 1-50)
    print("🏠 Добавление объектов недвижимости...")
    for i in range(1, 51):
        sitemap_xml += f'''  <url>
    <loc>{base_url}/object/{i}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
        url_count += 1
    
    # Добавление жилых комплексов (ID 1-20)
    print("🏢 Добавление жилых комплексов...")
    for i in range(1, 21):
        sitemap_xml += f'''  <url>
    <loc>{base_url}/residential_complex/{i}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
        url_count += 1
    
    # Добавление застройщиков (ID 1-10)
    print("🏗️ Добавление застройщиков...")
    for i in range(1, 11):
        sitemap_xml += f'''  <url>
    <loc>{base_url}/developer/{i}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
        url_count += 1
    
    sitemap_xml += '</urlset>'
    
    # Сохраняем файл
    os.makedirs('static', exist_ok=True)
    with open('static/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    
    print(f"✅ Полная карта сайта создана!")
    print(f"📊 Всего URL: {url_count}")
    print(f"📁 Файл: static/sitemap.xml")
    print(f"🌐 Доступ: https://inback.ru/sitemap.xml")
    
    return sitemap_xml

def create_robots_txt():
    """Создание robots.txt"""
    
    robots_content = f"""User-agent: *
Allow: /

# Ограничения для ботов
Disallow: /admin/
Disallow: /manager/
Disallow: /api/
Disallow: /uploads/
Disallow: /static/temp/
Disallow: /login
Disallow: /logout
Disallow: *.pdf$
Disallow: /*?print=*
Disallow: /*?*sort=*
Disallow: /*?*filter=*

# Разрешаем важные ресурсы
Allow: /static/css/
Allow: /static/js/
Allow: /static/images/
Allow: /static/sitemap.xml
Allow: /sitemap.xml

# Время между запросами
Crawl-delay: 1

# Карта сайта
Sitemap: https://inback.ru/sitemap.xml

# Настройки для разных поисковиков
User-agent: Googlebot
Crawl-delay: 1
Allow: /api/properties
Allow: /api/residential-complexes

User-agent: Yandex
Crawl-delay: 1
Allow: /api/properties
Allow: /api/residential-complexes

User-agent: Bingbot  
Crawl-delay: 2

# Блокировка нежелательных ботов
User-agent: SemrushBot
Disallow: /

User-agent: AhrefsBot
Disallow: /

User-agent: MJ12bot
Disallow: /
"""
    
    os.makedirs('static', exist_ok=True)
    with open('static/robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("🤖 robots.txt обновлен")

if __name__ == '__main__':
    print("🚀 Генерация полной карты сайта InBack.ru")
    generate_full_sitemap()
    create_robots_txt()
    print("✅ Готово! Sitemap и robots.txt созданы")