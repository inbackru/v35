#!/usr/bin/env python3
"""
Полная карта сайта для InBack.ru
Создает XML sitemap со всеми страницами включая динамические маршруты
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, url_for
from app import app, db
from models import ExcelProperty, ResidentialComplex
from sqlalchemy import text

def get_real_data():
    """Получение реальных данных из базы"""
    data = {
        'properties': [],
        'complexes': [],
        'developers': [],
        'streets': []
    }
    
    with app.app_context():
        try:
            # Объекты недвижимости (первые 100 для sitemap)
            properties = db.session.execute(
                text("SELECT property_id FROM excel_properties WHERE property_id IS NOT NULL ORDER BY property_id LIMIT 100")
            ).fetchall()
            data['properties'] = [str(row[0]) for row in properties if row[0]]
            
            # Жилые комплексы
            complexes = db.session.execute(
                text("SELECT id, slug FROM residential_complexes WHERE id IS NOT NULL")
            ).fetchall()
            data['complexes'] = [(str(row[0]), row[1]) for row in complexes if row[0]]
            
            # Застройщики (уникальные)
            developers = db.session.execute(
                text("SELECT DISTINCT developer_name FROM excel_properties WHERE developer_name IS NOT NULL AND developer_name != '' ORDER BY developer_name")
            ).fetchall()
            data['developers'] = [row[0] for row in developers if row[0]]
            
        except Exception as e:
            print(f"Error getting database data: {e}")
    
    # Улицы из JSON
    try:
        with open('data/streets.json', 'r', encoding='utf-8') as f:
            streets_data = json.load(f)
            # Берем первые 200 улиц для sitemap
            data['streets'] = [street['name'] for street in streets_data[:200] if street.get('name')]
    except Exception as e:
        print(f"Error loading streets: {e}")
    
    return data

# Основные статические страницы с приоритетами
STATIC_ROUTES = {
    # Главные страницы - высокий приоритет
    'index': {'priority': '1.0', 'changefreq': 'daily'},
    'properties': {'priority': '0.9', 'changefreq': 'daily'},
    'residential_complexes': {'priority': '0.9', 'changefreq': 'daily'},
    'developers': {'priority': '0.8', 'changefreq': 'weekly'},
    'map_view': {'priority': '0.8', 'changefreq': 'weekly'},
    
    # О компании
    'about': {'priority': '0.8', 'changefreq': 'monthly'},
    'how_it_works': {'priority': '0.8', 'changefreq': 'monthly'},
    'reviews': {'priority': '0.7', 'changefreq': 'weekly'},
    'contacts': {'priority': '0.7', 'changefreq': 'monthly'},
    'security': {'priority': '0.6', 'changefreq': 'monthly'},
    'careers': {'priority': '0.5', 'changefreq': 'monthly'},
    
    # Контент
    'blog': {'priority': '0.8', 'changefreq': 'daily'},
    'news': {'priority': '0.7', 'changefreq': 'daily'},
    'streets': {'priority': '0.7', 'changefreq': 'weekly'},
    'districts': {'priority': '0.7', 'changefreq': 'weekly'},
    
    # Ипотека
    'ipoteka': {'priority': '0.8', 'changefreq': 'weekly'},
    'family_mortgage': {'priority': '0.7', 'changefreq': 'monthly'},
    'it_mortgage': {'priority': '0.7', 'changefreq': 'monthly'},
    'military_mortgage': {'priority': '0.7', 'changefreq': 'monthly'},
    'developer_mortgage': {'priority': '0.7', 'changefreq': 'monthly'},
    'maternal_capital': {'priority': '0.7', 'changefreq': 'monthly'},
    
    # Сервисные страницы
    'comparison': {'priority': '0.6', 'changefreq': 'weekly'},
    'complex_comparison': {'priority': '0.6', 'changefreq': 'weekly'},
    'favorites': {'priority': '0.5', 'changefreq': 'daily'},
    'thank_you': {'priority': '0.3', 'changefreq': 'yearly'},
    
    # Политики
    'privacy_policy': {'priority': '0.3', 'changefreq': 'yearly'},
    'data_processing_consent': {'priority': '0.3', 'changefreq': 'yearly'}
}

# Районы Краснодара с SEO-именами
DISTRICTS = [
    'tsentralnyy', 'zapadny', 'karasunsky', 'festivalny', 'gidrostroitelei', 
    'yubileynyy', 'pashkovsky', 'prikubansky', 'enka', 'solnechny', 
    'panorama', 'vavilova', 'yablonovskiy', 'uchhoz-kuban', 'dubinka',
    'komsomolsky', 'kolosistiy', 'kozhzavod', 'kubansky', 'krasnodarskiy',
    '9i-kilometr', 'aviagorodok', 'avrora', 'basket-hall', 'berezovy',
    'cheremushki', 'gorkhutor', 'hbk', 'kalinino', 'kkb', 'ksk', 
    'krasnaya-ploshad', '40-let-pobedy', 'tsiolkovskogo', 'stasova',
    'kalinovaya', 'kotliarevskogo', 'akademika-lukianenko', 'starokorsunskaya',
    'im-40-letiya-pobedy', 'rossiyskaya', 'turgenevsky', 'slavyansky',
    'novorossiysky', 'tbilissky', 'severo-kavkazsky', 'adygeysky',
    'prochorzhsky', 'kievsky', 'dneprovskiy', 'moldavsky', 'sovetsky',
    'universitetsky', 'industrialny', 'shevchenko'
]

# Категории блога
BLOG_CATEGORIES = ['cashback', 'districts', 'mortgage', 'market', 'legal', 'tips']

def generate_sitemap():
    """Создание полной XML карты сайта"""
    
    print("🔄 Создание полной карты сайта...")
    
    # Получаем реальные данные
    data = get_real_data()
    print(f"📊 Данные: {len(data['properties'])} объектов, {len(data['complexes'])} ЖК, {len(data['developers'])} застройщиков, {len(data['streets'])} улиц")
    
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''

    base_url = "https://inback.ru"
    today = datetime.now().strftime('%Y-%m-%d')
    url_count = 0
    
    with app.app_context():
        # 1. Статические страницы
        print("📄 Добавление статических страниц...")
        for route, config in STATIC_ROUTES.items():
            try:
                url = url_for(route)
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{config['changefreq']}</changefreq>
    <priority>{config['priority']}</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем маршрут {route}: {e}")
        
        # 2. Объекты недвижимости
        print("🏠 Добавление объектов недвижимости...")
        for property_id in data['properties']:
            try:
                url = url_for('property_detail', property_id=int(property_id))
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем объект {property_id}: {e}")
        
        # 3. Жилые комплексы
        print("🏢 Добавление жилых комплексов...")
        for complex_id, slug in data['complexes']:
            try:
                # Основной маршрут
                url = url_for('residential_complex_detail', complex_id=int(complex_id))
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
                url_count += 1
                
                # SEO маршрут если есть slug
                if slug:
                    sitemap_xml += f'''  <url>
    <loc>{base_url}/zk/{slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
                    url_count += 1
                    
            except Exception as e:
                print(f"⚠️ Пропускаем ЖК {complex_id}: {e}")
        
        # 4. Застройщики
        print("🏗️ Добавление застройщиков...")
        for i, developer in enumerate(data['developers'], 1):
            try:
                url = url_for('developer_detail', developer_id=i)
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем застройщика {developer}: {e}")
        
        # 5. Районы
        print("📍 Добавление районов...")
        for district in DISTRICTS:
            try:
                url = f"/districts/{district}"
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем район {district}: {e}")
        
        # 6. Улицы (первые 200)
        print("🛣️ Добавление улиц...")
        for street_name in data['streets']:
            try:
                # Создаем безопасный URL для улицы
                street_url = street_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('/', '-')
                url = f"/streets/{street_url}"
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем улицу {street_name}: {e}")
        
        # 7. Категории блога
        print("📝 Добавление категорий блога...")
        for category in BLOG_CATEGORIES:
            try:
                url = url_for('blog_category', category_slug=category)
                sitemap_xml += f'''  <url>
    <loc>{base_url}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
'''
                url_count += 1
            except Exception as e:
                print(f"⚠️ Пропускаем категорию блога {category}: {e}")
    
    sitemap_xml += '</urlset>'
    
    # Сохраняем файл
    os.makedirs('static', exist_ok=True)
    with open('static/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    
    print(f"✅ Карта сайта создана! Всего URL: {url_count}")
    print(f"📁 Файл сохранен: static/sitemap.xml")
    print(f"🌐 Доступен по адресу: {base_url}/sitemap.xml")
    
    return sitemap_xml

def update_robots_txt():
    """Обновление robots.txt с указанием на sitemap"""
    
    robots_content = f"""User-agent: *
Allow: /

# Ограничения для ботов
Disallow: /admin/
Disallow: /manager/
Disallow: /api/
Disallow: /uploads/
Disallow: /static/
Disallow: /login
Disallow: /logout
Disallow: *.pdf$
Disallow: /*?*

# Время между запросами
Crawl-delay: 1

# Карта сайта
Sitemap: https://inback.ru/sitemap.xml

# Специфичные настройки для разных ботов
User-agent: Googlebot
Crawl-delay: 1

User-agent: Yandex
Crawl-delay: 1

User-agent: Bingbot  
Crawl-delay: 2
"""
    
    with open('static/robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("🤖 robots.txt обновлен")

if __name__ == '__main__':
    print("🚀 Запуск генерации карты сайта InBack.ru")
    generate_sitemap()
    update_robots_txt()
    print("✅ Готово! Карта сайта и robots.txt созданы")