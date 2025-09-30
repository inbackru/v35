#!/usr/bin/env python3
"""
Скрипт для импорта данных блога из JSON файлов в базу данных PostgreSQL
"""

import json
import os
import sys
from datetime import datetime
from app import app, db
from models import BlogCategory, BlogArticle, BlogPost

def load_json_file(filename):
    """Загружает данные из JSON файла"""
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл data/{filename} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле data/{filename}")
        return []

def import_blog_categories():
    """Импортирует категории блога"""
    print("Импортирую категории блога...")
    
    categories_data = load_json_file('blog_categories.json')
    if not categories_data:
        print("Нет данных категорий для импорта")
        return
    
    imported_count = 0
    for cat_data in categories_data:
        # Проверяем, не существует ли уже такая категория
        existing = BlogCategory.query.filter_by(slug=cat_data['slug']).first()
        if existing:
            print(f"Категория {cat_data['name']} уже существует, обновляю...")
            existing.name = cat_data['name']
            existing.description = cat_data.get('description', '')
            existing.color = cat_data.get('color', '#2563eb')
        else:
            category = BlogCategory(
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=cat_data.get('description', ''),
                color=cat_data.get('color', '#2563eb')
            )
            db.session.add(category)
            imported_count += 1
    
    try:
        db.session.commit()
        print(f"Импортировано {imported_count} категорий блога")
    except Exception as e:
        print(f"Ошибка при импорте категорий: {e}")
        db.session.rollback()

def import_blog_articles():
    """Импортирует статьи блога"""
    print("Импортирую статьи блога...")
    
    articles_data = load_json_file('blog_articles.json')
    if not articles_data:
        print("Нет данных статей для импорта")
        return
    
    imported_count = 0
    for article_data in articles_data:
        # Проверяем, не существует ли уже такая статья
        existing = BlogArticle.query.filter_by(slug=article_data['slug']).first()
        if existing:
            print(f"Статья {article_data['title']} уже существует, обновляю...")
            existing.title = article_data['title']
            existing.content = article_data.get('content', '')
            existing.excerpt = article_data.get('excerpt', '')
            existing.author = article_data.get('author', 'Автор')
            existing.author_position = article_data.get('author_position', '')
            existing.category_name = article_data.get('category', 'Общее')
            existing.reading_time = article_data.get('reading_time', 5)
            existing.views = article_data.get('views', 0)
            existing.featured = article_data.get('featured', False)
            existing.image = article_data.get('image', '')
            existing.meta_description = article_data.get('meta_description', '')
            existing.seo_keywords = article_data.get('seo_keywords', '')
            existing.updated_at = datetime.utcnow()
        else:
            # Парсим дату
            date_str = article_data.get('date', '2024-01-01')
            try:
                published_at = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                published_at = datetime.utcnow()
            
            article = BlogArticle(
                title=article_data['title'],
                slug=article_data['slug'],
                content=article_data.get('content', ''),
                excerpt=article_data.get('excerpt', ''),
                author=article_data.get('author', 'Автор'),
                author_position=article_data.get('author_position', ''),
                category_name=article_data.get('category', 'Общее'),
                reading_time=article_data.get('reading_time', 5),
                views=article_data.get('views', 0),
                featured=article_data.get('featured', False),
                image=article_data.get('image', ''),
                meta_description=article_data.get('meta_description', ''),
                seo_keywords=article_data.get('seo_keywords', ''),
                published_at=published_at,
                status='published',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(article)
            imported_count += 1
    
    try:
        db.session.commit()
        print(f"Импортировано {imported_count} статей блога")
    except Exception as e:
        print(f"Ошибка при импорте статей: {e}")
        db.session.rollback()

def main():
    """Основная функция импорта"""
    print("Начинаю импорт данных блога...")
    
    with app.app_context():
        # Создаем таблицы, если их нет
        try:
            db.create_all()
            print("Таблицы базы данных готовы")
        except Exception as e:
            print(f"Ошибка создания таблиц: {e}")
            return
        
        # Импортируем данные
        import_blog_categories()
        import_blog_articles()
        
        # Проверяем результаты
        categories_count = BlogCategory.query.count()
        articles_count = BlogArticle.query.count()
        posts_count = BlogPost.query.count()
        
        print(f"\nРезультаты импорта:")
        print(f"Категории блога: {categories_count}")
        print(f"Статьи блога: {articles_count}")
        print(f"Посты блога: {posts_count}")
        print("\nИмпорт данных блога завершен!")

if __name__ == '__main__':
    main()