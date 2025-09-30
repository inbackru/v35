#!/usr/bin/env python3
"""
Скрипт для импорта данных из XLSX файлов в базу данных PostgreSQL
"""

import pandas as pd
import os
from datetime import datetime
from app import app, db
from models import BlogCategory, BlogArticle

def safe_convert_datetime(date_str):
    """Безопасное преобразование строки в datetime"""
    if pd.isna(date_str) or date_str is None or date_str == '':
        return datetime.utcnow()
    
    if isinstance(date_str, datetime):
        return date_str
    
    try:
        # Пробуем разные форматы даты
        date_str = str(date_str)
        if 'GMT' in date_str:
            # Убираем GMT часть
            date_str = date_str.split(' GMT')[0]
        
        # Пробуем стандартные форматы
        for fmt in ['%a %b %d %Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d.%m.%Y', '%d-%m-%Y']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.utcnow()
    except:
        return datetime.utcnow()

def import_blog_categories_from_xlsx():
    """Импортирует категории блога из XLSX файла"""
    print("Импортирую категории блога из XLSX...")
    
    file_path = 'attached_assets/blog_categories (1)_1755110853167.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} категорий из файла")
        
        imported_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            category_id = int(row['id']) if not pd.isna(row['id']) else None
            slug = str(row['slug']) if not pd.isna(row['slug']) else f"category-{category_id}"
            
            # Проверяем, существует ли категория по ID или по slug
            existing = None
            if category_id:
                existing = BlogCategory.query.filter_by(id=category_id).first()
            if not existing and slug:
                existing = BlogCategory.query.filter_by(slug=slug).first()
            
            category_data = {
                'name': str(row['name']) if not pd.isna(row['name']) else 'Без названия',
                'slug': slug,
                'description': str(row['description']) if not pd.isna(row['description']) else '',
                'color': str(row['color']) if not pd.isna(row['color']) else '#2563eb',
                'icon': str(row['icon']) if not pd.isna(row['icon']) else '',
                'meta_title': str(row['meta_title']) if not pd.isna(row['meta_title']) else '',
                'meta_description': str(row['meta_description']) if not pd.isna(row['meta_description']) else '',
                'sort_order': int(row['sort_order']) if not pd.isna(row['sort_order']) else 0,
                'is_active': bool(row['is_active']) if not pd.isna(row['is_active']) else True,
                'articles_count': int(row['articles_count']) if not pd.isna(row['articles_count']) else 0,
                'views_count': int(row['views_count']) if not pd.isna(row['views_count']) else 0,
                'updated_at': safe_convert_datetime(row['updated_at'])
            }
            
            if existing:
                # Обновляем существующую категорию
                for key, value in category_data.items():
                    setattr(existing, key, value)
                updated_count += 1
                print(f"Обновлена категория: {category_data['name']}")
            else:
                # Создаем новую категорию
                category_data['id'] = category_id
                category_data['created_at'] = safe_convert_datetime(row['created_at'])
                
                category = BlogCategory(**category_data)
                db.session.add(category)
                imported_count += 1
                print(f"Создана категория: {category_data['name']}")
        
        db.session.commit()
        print(f"Категории: импортировано {imported_count}, обновлено {updated_count}")
        
    except Exception as e:
        print(f"Ошибка при импорте категорий: {e}")
        db.session.rollback()

def import_blog_articles_from_xlsx():
    """Импортирует статьи блога из XLSX файла"""
    print("Импортирую статьи блога из XLSX...")
    
    file_path = 'attached_assets/blog_articles (1)_1755110853169.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"Загружено {len(df)} статей из файла")
        
        imported_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            article_id = int(row['id']) if not pd.isna(row['id']) else None
            slug = str(row['slug']) if not pd.isna(row['slug']) else f"article-{article_id}"
            
            # Проверяем, существует ли статья
            existing = BlogArticle.query.filter_by(id=article_id).first() if article_id else None
            
            article_data = {
                'title': str(row['title']) if not pd.isna(row['title']) else 'Без названия',
                'slug': slug,
                'excerpt': str(row['excerpt']) if not pd.isna(row['excerpt']) else '',
                'content': str(row['content']) if not pd.isna(row['content']) else '',
                'author_id': int(row['author_id']) if not pd.isna(row['author_id']) else None,
                'author_name': str(row['author_name']) if not pd.isna(row['author_name']) else 'Автор',
                'category_id': int(row['category_id']) if not pd.isna(row['category_id']) else 1,
                'status': str(row['status']) if not pd.isna(row['status']) else 'published',
                'published_at': safe_convert_datetime(row['published_at']),
                'scheduled_at': safe_convert_datetime(row['scheduled_at']) if not pd.isna(row['scheduled_at']) else None,
                'meta_title': str(row['meta_title']) if not pd.isna(row['meta_title']) else '',
                'meta_description': str(row['meta_description']) if not pd.isna(row['meta_description']) else '',
                'meta_keywords': str(row['meta_keywords']) if not pd.isna(row['meta_keywords']) else '',
                'featured_image': str(row['featured_image']) if not pd.isna(row['featured_image']) else '',
                'featured_image_alt': str(row['featured_image_alt']) if not pd.isna(row['featured_image_alt']) else '',
                'is_featured': bool(row['is_featured']) if not pd.isna(row['is_featured']) else False,
                'allow_comments': bool(row['allow_comments']) if not pd.isna(row['allow_comments']) else True,
                'views_count': int(row['views_count']) if not pd.isna(row['views_count']) else 0,
                'reading_time': int(row['reading_time']) if not pd.isna(row['reading_time']) else 5,
                'updated_at': safe_convert_datetime(row['updated_at'])
            }
            
            if existing:
                # Обновляем существующую статью
                for key, value in article_data.items():
                    setattr(existing, key, value)
                updated_count += 1
                print(f"Обновлена статья: {article_data['title']}")
            else:
                # Создаем новую статью
                article_data['id'] = article_id
                article_data['created_at'] = safe_convert_datetime(row['created_at'])
                
                article = BlogArticle(**article_data)
                db.session.add(article)
                imported_count += 1
                print(f"Создана статья: {article_data['title']}")
        
        db.session.commit()
        print(f"Статьи: импортировано {imported_count}, обновлено {updated_count}")
        
    except Exception as e:
        print(f"Ошибка при импорте статей: {e}")
        db.session.rollback()
        import traceback
        traceback.print_exc()

def main():
    """Основная функция импорта"""
    print("Начинаю импорт данных из XLSX файлов...")
    
    with app.app_context():
        # Создаем таблицы, если их нет
        try:
            db.create_all()
            print("Таблицы базы данных готовы")
        except Exception as e:
            print(f"Ошибка создания таблиц: {e}")
            return
        
        # Импортируем данные
        import_blog_categories_from_xlsx()
        import_blog_articles_from_xlsx()
        
        # Проверяем результаты
        categories_count = BlogCategory.query.count()
        articles_count = BlogArticle.query.count()
        
        print(f"\nРезультаты импорта:")
        print(f"Категории блога: {categories_count}")
        print(f"Статьи блога: {articles_count}")
        print("\nИмпорт данных блога завершен!")

if __name__ == '__main__':
    main()