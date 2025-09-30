#!/usr/bin/env python3
"""
Импорт данных из JSON файлов в базу данных PostgreSQL
"""

import json
import os
import re
from app import app, db
from models import *
from datetime import datetime

def generate_slug(name):
    """Генерация slug из названия"""
    # Убираем лишние символы и приводим к нижнему регистру
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    # Заменяем пробелы на дефисы
    slug = re.sub(r'[-\s]+', '-', slug)
    # Убираем дефисы в начале и конце
    return slug.strip('-')

def import_developers():
    """Импорт застройщиков"""
    try:
        with open('inback_production_ready_v3/data/developers.json', 'r', encoding='utf-8') as f:
            developers_data = json.load(f)
        
        print(f"🏗️ Импорт {len(developers_data)} застройщиков...")
        
        for dev_data in developers_data:
            existing = Developer.query.filter_by(name=dev_data['name']).first()
            if not existing:
                developer = Developer(
                    name=dev_data['name'],
                    slug=generate_slug(dev_data['name']),
                    description=dev_data.get('description', ''),
                    phone=dev_data.get('phone', ''),
                    email=dev_data.get('email', ''),
                    website=dev_data.get('website', ''),
                    logo_url=dev_data.get('logo_url', ''),
                    address=dev_data.get('address', '')
                )
                db.session.add(developer)
        
        db.session.commit()
        print(f"✅ Застройщики импортированы: {Developer.query.count()}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта застройщиков: {e}")

def import_residential_complexes():
    """Импорт жилых комплексов"""
    try:
        with open('inback_production_ready_v3/data/residential_complexes.json', 'r', encoding='utf-8') as f:
            complexes_data = json.load(f)
        
        print(f"🏢 Импорт {len(complexes_data)} жилых комплексов...")
        
        for complex_data in complexes_data:
            existing = ResidentialComplex.query.filter_by(name=complex_data['name']).first()
            if not existing:
                # Находим застройщика
                developer = Developer.query.filter_by(name=complex_data.get('developer', '')).first()
                if not developer:
                    developer = Developer.query.first()  # Берём первого доступного
                
                complex_obj = ResidentialComplex(
                    name=complex_data['name'],
                    slug=generate_slug(complex_data['name']),
                    developer_id=developer.id if developer else None,
                    district=complex_data.get('district', ''),
                    address=complex_data.get('address', ''),
                    completion_date=complex_data.get('completion_date', ''),
                    building_type=complex_data.get('building_type', ''),
                    class_type=complex_data.get('class_type', ''),
                    description=complex_data.get('description', ''),
                    amenities=json.dumps(complex_data.get('amenities', [])),
                    transport=json.dumps(complex_data.get('transport', [])),
                    image_url=complex_data.get('image_url', ''),
                    gallery=json.dumps(complex_data.get('gallery', []))
                )
                db.session.add(complex_obj)
        
        db.session.commit()
        print(f"✅ Жилые комплексы импортированы: {ResidentialComplex.query.count()}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта жилых комплексов: {e}")

def import_properties():
    """Импорт объектов недвижимости"""
    try:
        with open('inback_production_ready_v3/data/properties.json', 'r', encoding='utf-8') as f:
            properties_data = json.load(f)
        
        print(f"🏠 Импорт {len(properties_data)} объектов недвижимости...")
        
        for prop_data in properties_data:
            existing = Property.query.filter_by(
                title=prop_data['title']
            ).first()
            
            if not existing:
                # Находим застройщика
                developer = Developer.query.filter_by(name=prop_data.get('developer', '')).first()
                if not developer:
                    developer = Developer.query.first()
                
                # Находим жилой комплекс
                residential_complex = ResidentialComplex.query.filter_by(
                    name=prop_data.get('residential_complex', '')
                ).first()
                
                property_obj = Property(
                    title=prop_data['title'],
                    slug=generate_slug(prop_data['title']),
                    rooms=prop_data.get('rooms', 1),
                    area=float(prop_data.get('area', 0)),
                    floor=prop_data.get('floor', 1),
                    total_floors=prop_data.get('total_floors', 1),
                    price=int(prop_data.get('price', 0)),
                    price_per_sqm=int(prop_data.get('price_per_sqm', 0)),
                    district=prop_data.get('district', ''),
                    location=prop_data.get('address', ''),  # Используем location вместо address
                    building_type=prop_data.get('building_type', ''),
                    finishing=prop_data.get('finishing', ''),
                    has_balcony=prop_data.get('has_balcony', False),
                    mortgage_available=prop_data.get('mortgage_available', True),
                    preferential_mortgage=prop_data.get('preferential_mortgage', False),
                    family_mortgage=prop_data.get('family_mortgage', False),
                    it_mortgage=prop_data.get('it_mortgage', False),
                    property_type=prop_data.get('property_type', 'Квартира'),
                    description=prop_data.get('description', ''),
                    image=prop_data.get('image', ''),
                    gallery=json.dumps(prop_data.get('gallery', [])),
                    developer_id=developer.id if developer else None,
                    residential_complex_id=residential_complex.id if residential_complex else None,
                    created_at=datetime.utcnow()
                )
                db.session.add(property_obj)
        
        db.session.commit()
        print(f"✅ Объекты недвижимости импортированы: {Property.query.count()}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта объектов недвижимости: {e}")

def import_blog_categories():
    """Импорт категорий блога"""
    try:
        with open('inback_production_ready_v3/data/blog_categories.json', 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
        
        print(f"📚 Импорт {len(categories_data)} категорий блога...")
        
        for cat_data in categories_data:
            existing = BlogCategory.query.filter_by(name=cat_data['name']).first()
            if not existing:
                category = BlogCategory(
                    name=cat_data['name'],
                    slug=generate_slug(cat_data['name']),
                    description=cat_data.get('description', ''),
                    created_at=datetime.utcnow()
                )
                db.session.add(category)
        
        db.session.commit()
        print(f"✅ Категории блога импортированы: {BlogCategory.query.count()}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта категорий блога: {e}")

def import_blog_articles():
    """Импорт статей блога"""
    try:
        with open('inback_production_ready_v3/data/blog_articles.json', 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        print(f"📝 Импорт {len(articles_data)} статей блога...")
        
        for article_data in articles_data:
            existing = BlogArticle.query.filter_by(title=article_data['title']).first()
            if not existing:
                # Находим категорию
                category = BlogCategory.query.filter_by(
                    name=article_data.get('category', '')
                ).first()
                
                article = BlogArticle(
                    title=article_data['title'],
                    slug=generate_slug(article_data['title']),
                    content=article_data.get('content', ''),
                    excerpt=article_data.get('excerpt', ''),
                    featured_image=article_data.get('featured_image', ''),
                    category_id=category.id if category else None,
                    is_published=article_data.get('is_published', True),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(article)
        
        db.session.commit()
        print(f"✅ Статьи блога импортированы: {BlogArticle.query.count()}")
        
    except Exception as e:
        print(f"❌ Ошибка импорта статей блога: {e}")

def main():
    """Главная функция импорта"""
    with app.app_context():
        print("🚀 ИМПОРТ ДАННЫХ ИЗ JSON ФАЙЛОВ")
        print("=" * 50)
        
        # Импортируем данные в правильном порядке
        import_developers()
        import_residential_complexes()
        import_properties()
        import_blog_categories()
        import_blog_articles()
        
        print("\n📊 ФИНАЛЬНАЯ СТАТИСТИКА")
        try:
            print(f"Застройщики: {Developer.query.count()}")
            print(f"Жилые комплексы: {ResidentialComplex.query.count()}")
            print(f"Объекты недвижимости: {Property.query.count()}")
            print(f"Категории блога: {BlogCategory.query.count()}")
            print(f"Статьи блога: {BlogArticle.query.count()}")
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
            db.session.rollback()
        
        print("\n✅ ИМПОРТ ЗАВЕРШЕН!")

if __name__ == "__main__":
    main()