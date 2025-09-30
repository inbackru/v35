#!/usr/bin/env python3
"""
Полный импорт данных из Excel файлов
"""

import pandas as pd
import numpy as np
import os
import re
import json
from app import app, db
from models import *
from datetime import datetime
from werkzeug.security import generate_password_hash

def generate_slug(name):
    """Генерация slug из названия"""
    if not name:
        return 'unnamed'
    slug = re.sub(r'[^\w\s-]', '', str(name).lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def safe_get(row, field, default=None):
    """Безопасно получить значение поля"""
    try:
        value = row.get(field, default)
        if pd.isna(value) or value is None or value == '':
            return default
        return value
    except:
        return default

def safe_str(value, default=''):
    """Безопасно преобразовать в строку"""
    if pd.isna(value) or value is None:
        return default
    return str(value).strip()

def safe_int(value, default=0):
    """Безопасно преобразовать в int"""
    if pd.isna(value) or value is None:
        return default
    try:
        return int(float(value))
    except:
        return default

def safe_float(value, default=0.0):
    """Безопасно преобразовать в float"""
    if pd.isna(value) or value is None:
        return default
    try:
        return float(value)
    except:
        return default

def import_file(file_path, model_class, field_mapping):
    """Универсальная функция импорта из Excel"""
    try:
        print(f"📊 Импорт {file_path}...")
        df = pd.read_excel(file_path)
        
        if df.empty:
            print(f"⚠️ Файл {file_path} пустой")
            return 0
        
        count = 0
        for _, row in df.iterrows():
            try:
                # Создаем объект с полями из mapping
                obj_data = {}
                for db_field, excel_field in field_mapping.items():
                    if excel_field in row:
                        value = safe_get(row, excel_field)
                        
                        # Специальная обработка для разных типов полей
                        if db_field in ['created_at', 'updated_at', 'parsed_at', 'last_used']:
                            obj_data[db_field] = datetime.utcnow()
                        elif db_field == 'slug':
                            obj_data[db_field] = generate_slug(value) + f'-{count}'
                        elif db_field == 'password_hash':
                            obj_data[db_field] = generate_password_hash('demo123')
                        elif 'is_' in db_field or db_field in ['active', 'published', 'verified']:
                            obj_data[db_field] = bool(value) if value is not None else False
                        elif db_field in ['gallery', 'features', 'amenities', 'transport', 'filters']:
                            obj_data[db_field] = json.dumps(value if isinstance(value, list) else [])
                        else:
                            obj_data[db_field] = value
                
                # Проверяем обязательные поля
                if 'name' in field_mapping.values() and not obj_data.get('name'):
                    continue
                if 'title' in field_mapping.values() and not obj_data.get('title'):
                    continue
                    
                # Создаем объект
                obj = model_class(**obj_data)
                db.session.add(obj)
                count += 1
                
            except Exception as e:
                print(f"⚠️ Ошибка импорта строки: {e}")
                continue
        
        db.session.commit()
        print(f"✅ Импортировано {count} записей из {file_path}")
        return count
        
    except Exception as e:
        print(f"❌ Ошибка импорта {file_path}: {e}")
        db.session.rollback()
        return 0

def main():
    """Главная функция импорта"""
    with app.app_context():
        print("🚀 ПОЛНЫЙ ИМПОРТ ДАННЫХ ИЗ EXCEL ФАЙЛОВ")
        print("=" * 60)
        
        # Очищаем существующие данные для чистого импорта
        print("🧹 Очистка базы данных...")
        try:
            # Удаляем все данные кроме системных
            for table in ['properties', 'residential_complexes', 'blog_articles', 'blog_categories']:
                db.session.execute(f"DELETE FROM {table}")
            db.session.commit()
            print("✅ База данных очищена")
        except Exception as e:
            print(f"⚠️ Ошибка очистки: {e}")
            db.session.rollback()
        
        # Определяем файлы и их маппинги
        files_mapping = {
            'attached_assets/properties_1756280785033.xlsx': {
                'model': Property,
                'fields': {
                    'title': 'title',
                    'slug': 'title',  # Будет сгенерирован автоматически
                    'rooms': 'rooms',
                    'area': 'area',
                    'floor': 'floor',
                    'total_floors': 'total_floors',
                    'price': 'price',
                    'price_per_sqm': 'price_per_sqm',
                    'district': 'district',
                    'location': 'address',
                    'building_type': 'building_type',
                    'finishing': 'finishing',
                    'description': 'description',
                    'created_at': 'created_at'
                }
            },
            'attached_assets/residential_complexes (5)_1756280785029.xlsx': {
                'model': ResidentialComplex,
                'fields': {
                    'name': 'name',
                    'slug': 'name',
                    'district': 'district',
                    'address': 'address',
                    'completion_date': 'completion_date',
                    'building_type': 'building_type',
                    'class_type': 'class_type',
                    'description': 'description',
                    'created_at': 'created_at'
                }
            },
            'attached_assets/developers (5)_1756280785030.xlsx': {
                'model': Developer,
                'fields': {
                    'name': 'name',
                    'slug': 'name',
                    'description': 'description',
                    'phone': 'phone',
                    'email': 'email',
                    'website': 'website',
                    'address': 'address',
                    'created_at': 'created_at'
                }
            },
            'attached_assets/blog_categories (4)_1756280785032.xlsx': {
                'model': BlogCategory,
                'fields': {
                    'name': 'name',
                    'slug': 'name',
                    'description': 'description',
                    'created_at': 'created_at'
                }
            },
            'attached_assets/blog_posts (4)_1756280785031.xlsx': {
                'model': BlogArticle,
                'fields': {
                    'title': 'title',
                    'slug': 'title',
                    'content': 'content',
                    'excerpt': 'excerpt',
                    'featured_image': 'featured_image',
                    'is_published': 'is_published',
                    'created_at': 'created_at'
                }
            }
        }
        
        # Импортируем файлы
        total_imported = 0
        for file_path, config in files_mapping.items():
            if os.path.exists(file_path):
                imported = import_file(file_path, config['model'], config['fields'])
                total_imported += imported
            else:
                print(f"⚠️ Файл {file_path} не найден")
        
        print(f"\n📊 ИТОГО ИМПОРТИРОВАНО: {total_imported} записей")
        
        # Проверяем финальную статистику
        print("\n📈 ФИНАЛЬНАЯ СТАТИСТИКА:")
        try:
            print(f"Застройщики: {Developer.query.count()}")
            print(f"Жилые комплексы: {ResidentialComplex.query.count()}")
            print(f"Объекты недвижимости: {Property.query.count()}")
            print(f"Категории блога: {BlogCategory.query.count()}")
            print(f"Статьи блога: {BlogArticle.query.count()}")
            print(f"Пользователи: {User.query.count()}")
            print(f"Менеджеры: {Manager.query.count()}")
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
        
        print("\n✅ ИМПОРТ ЗАВЕРШЕН!")

if __name__ == "__main__":
    main()