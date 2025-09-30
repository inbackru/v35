#!/usr/bin/env python3
"""
Полный импорт ВСЕХ данных из Excel файлов
"""

import pandas as pd
import numpy as np
import os
from app import app, db
from models import *
from datetime import datetime
import json

def safe_get(row, field, default=None):
    """Безопасно получить значение поля"""
    value = row.get(field, default)
    if pd.isna(value) or value is None or value == '':
        return default
    return value

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

def safe_bool(value, default=False):
    """Безопасно преобразовать в bool"""
    if pd.isna(value) or value is None:
        return default
    if isinstance(value, bool):
        return value
    try:
        return bool(int(value))
    except:
        return str(value).lower() in ['true', '1', 'yes', 'да']

def parse_date(date_str):
    """Парсинг даты из разных форматов"""
    if pd.isna(date_str) or date_str == '' or date_str is None:
        return datetime.utcnow()
    
    if isinstance(date_str, datetime):
        return date_str
    
    try:
        date_str = str(date_str)
        # Убираем GMT и таймзоны
        if 'GMT' in date_str:
            date_str = date_str.split(' GMT')[0]
        
        # Попробуем разные форматы
        formats = [
            '%a %b %d %Y %H:%M:%S',  # Mon Aug 11 2025 03:34:16
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d.%m.%Y',
            '%d/%m/%Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.utcnow()
    except:
        return datetime.utcnow()

def import_admins():
    """Импорт администраторов"""
    print("=== ИМПОРТ АДМИНИСТРАТОРОВ ===")
    
    try:
        df = pd.read_excel('attached_assets/admins (3)_1755342720987.xlsx')
        print(f"Найдено администраторов: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                admin_id = safe_int(row.get('id'))
                email = safe_str(row.get('email'))
                
                if not email or admin_id <= 0:
                    continue
                
                # Проверяем, есть ли такой админ
                existing = Admin.query.filter_by(id=admin_id).first() if 'Admin' in globals() else None
                if existing:
                    continue
                
                if 'Admin' in globals():
                    admin = Admin(
                        id=admin_id,
                        email=email,
                        password_hash=safe_str(row.get('password_hash')),
                        full_name=safe_str(row.get('full_name')),
                        admin_id=safe_str(row.get('admin_id')),
                        role=safe_str(row.get('role', 'admin')),
                        permissions=safe_str(row.get('permissions', '{}')),
                        is_active=safe_bool(row.get('is_active', True)),
                        is_super_admin=safe_bool(row.get('is_super_admin', False)),
                        profile_image=safe_str(row.get('profile_image')),
                        phone=safe_str(row.get('phone')),
                        created_at=parse_date(row.get('created_at')),
                        updated_at=parse_date(row.get('updated_at'))
                    )
                    
                    db.session.add(admin)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта админа {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано администраторов: {imported}")
        else:
            print("⚠️ Модель Admin не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта администраторов: {e}")
        db.session.rollback()

def import_streets():
    """Импорт улиц"""
    print("=== ИМПОРТ УЛИЦ ===")
    
    try:
        df = pd.read_excel('attached_assets/streets_1755342720989.xlsx')
        print(f"Найдено улиц: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                street_id = safe_int(row.get('id'))
                name = safe_str(row.get('name'))
                
                if not name or street_id <= 0:
                    continue
                
                # Проверяем, есть ли такая улица
                existing = Street.query.filter_by(id=street_id).first() if 'Street' in globals() else None
                if existing:
                    continue
                
                if 'Street' in globals():
                    street = Street(
                        id=street_id,
                        name=name,
                        slug=safe_str(row.get('slug'), name.lower().replace(' ', '-')),
                        district_id=safe_int(row.get('district_id')) if pd.notna(row.get('district_id')) else None
                    )
                    
                    db.session.add(street)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта улицы {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано улиц: {imported}")
        else:
            print("⚠️ Модель Street не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта улиц: {e}")
        db.session.rollback()

def import_managers():
    """Импорт менеджеров"""
    print("=== ИМПОРТ МЕНЕДЖЕРОВ ===")
    
    try:
        df = pd.read_excel('attached_assets/managers (3)_1755342720986.xlsx')
        print(f"Найдено менеджеров: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                manager_id = safe_int(row.get('id'))
                email = safe_str(row.get('email'))
                
                if not email or manager_id <= 0:
                    continue
                
                # Проверяем, есть ли такой менеджер
                existing = Manager.query.filter_by(id=manager_id).first() if 'Manager' in globals() else None
                if existing:
                    continue
                
                if 'Manager' in globals():
                    manager = Manager(
                        id=manager_id,
                        email=email,
                        password_hash=safe_str(row.get('password_hash')),
                        first_name=safe_str(row.get('first_name')),
                        last_name=safe_str(row.get('last_name')),
                        phone=safe_str(row.get('phone')),
                        position=safe_str(row.get('position', 'Менеджер')),
                        can_approve_cashback=safe_bool(row.get('can_approve_cashback', True)),
                        can_manage_documents=safe_bool(row.get('can_manage_documents', True)),
                        can_create_collections=safe_bool(row.get('can_create_collections', True)),
                        max_cashback_approval=safe_int(row.get('max_cashback_approval', 500000)),
                        is_active=safe_bool(row.get('is_active', True)),
                        profile_image=safe_str(row.get('profile_image')),
                        manager_id=safe_str(row.get('manager_id')),
                        created_at=parse_date(row.get('created_at')),
                        updated_at=parse_date(row.get('updated_at'))
                    )
                    
                    db.session.add(manager)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта менеджера {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано менеджеров: {imported}")
        else:
            print("⚠️ Модель Manager не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта менеджеров: {e}")
        db.session.rollback()

def import_blog_articles():
    """Импорт статей блога"""
    print("=== ИМПОРТ СТАТЕЙ БЛОГА ===")
    
    try:
        df = pd.read_excel('attached_assets/blog_articles (2)_1755342720986.xlsx')
        print(f"Найдено статей блога: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                article_id = safe_int(row.get('id'))
                title = safe_str(row.get('title'))
                
                if not title or article_id <= 0:
                    continue
                
                # Проверяем, есть ли такая статья
                existing = BlogArticle.query.filter_by(id=article_id).first() if 'BlogArticle' in globals() else None
                if existing:
                    continue
                
                if 'BlogArticle' in globals():
                    article = BlogArticle(
                        id=article_id,
                        title=title,
                        slug=safe_str(row.get('slug')),
                        excerpt=safe_str(row.get('excerpt')),
                        content=safe_str(row.get('content')),
                        author_id=safe_int(row.get('author_id')),
                        author_name=safe_str(row.get('author_name')),
                        category_id=safe_int(row.get('category_id')),
                        status=safe_str(row.get('status', 'draft')),
                        published_at=parse_date(row.get('published_at')),
                        meta_title=safe_str(row.get('meta_title')),
                        meta_description=safe_str(row.get('meta_description')),
                        meta_keywords=safe_str(row.get('meta_keywords')),
                        featured_image=safe_str(row.get('featured_image')),
                        is_featured=safe_bool(row.get('is_featured', False)),
                        allow_comments=safe_bool(row.get('allow_comments', True)),
                        views_count=safe_int(row.get('views_count')),
                        reading_time=safe_int(row.get('reading_time')),
                        created_at=parse_date(row.get('created_at')),
                        updated_at=parse_date(row.get('updated_at'))
                    )
                    
                    db.session.add(article)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта статьи {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано статей блога: {imported}")
        else:
            print("⚠️ Модель BlogArticle не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта статей блога: {e}")
        db.session.rollback()

def import_favorites():
    """Импорт избранных объектов"""
    print("=== ИМПОРТ ИЗБРАННЫХ ОБЪЕКТОВ ===")
    
    try:
        df = pd.read_excel('attached_assets/favorite_properties (3)_1755342720991.xlsx')
        print(f"Найдено избранных: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                fav_id = safe_int(row.get('id'))
                user_id = safe_int(row.get('user_id'))
                property_id = safe_int(row.get('property_id'))
                
                if fav_id <= 0 or user_id <= 0:
                    continue
                
                # Проверяем, есть ли такое избранное
                existing = Favorite.query.filter_by(id=fav_id).first() if 'Favorite' in globals() else None
                if existing:
                    continue
                
                if 'Favorite' in globals():
                    favorite = Favorite(
                        id=fav_id,
                        user_id=user_id,
                        property_id=property_id,
                        property_name=safe_str(row.get('property_name')),
                        property_type=safe_str(row.get('property_type')),
                        property_size=safe_float(row.get('property_size')),
                        property_price=safe_int(row.get('property_price')),
                        complex_name=safe_str(row.get('complex_name')),
                        developer_name=safe_str(row.get('developer_name')),
                        property_image=safe_str(row.get('property_image')),
                        property_url=safe_str(row.get('property_url')),
                        cashback_amount=safe_int(row.get('cashback_amount')),
                        cashback_percent=safe_int(row.get('cashback_percent')),
                        created_at=parse_date(row.get('created_at'))
                    )
                    
                    db.session.add(favorite)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта избранного {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано избранных: {imported}")
        else:
            print("⚠️ Модель Favorite не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта избранных: {e}")
        db.session.rollback()

def import_callback_requests():
    """Импорт запросов обратного звонка"""
    print("=== ИМПОРТ ЗАПРОСОВ ОБРАТНОГО ЗВОНКА ===")
    
    try:
        df = pd.read_excel('attached_assets/callback_requests (1)_1755342720987.xlsx')
        print(f"Найдено запросов: {len(df)}")
        
        imported = 0
        for index, row in df.iterrows():
            try:
                request_id = safe_int(row.get('id'))
                name = safe_str(row.get('name'))
                phone = safe_str(row.get('phone'))
                
                if request_id <= 0 or not name:
                    continue
                
                # Проверяем, есть ли такой запрос
                existing = CallbackRequest.query.filter_by(id=request_id).first() if 'CallbackRequest' in globals() else None
                if existing:
                    continue
                
                if 'CallbackRequest' in globals():
                    callback = CallbackRequest(
                        id=request_id,
                        name=name,
                        phone=phone,
                        email=safe_str(row.get('email')),
                        preferred_time=safe_str(row.get('preferred_time')),
                        notes=safe_str(row.get('notes')),
                        interest=safe_str(row.get('interest')),
                        budget=safe_str(row.get('budget')),
                        timing=safe_str(row.get('timing')),
                        status=safe_str(row.get('status', 'Новая')),
                        assigned_manager_id=safe_int(row.get('assigned_manager_id')) if pd.notna(row.get('assigned_manager_id')) else None,
                        manager_notes=safe_str(row.get('manager_notes')),
                        created_at=parse_date(row.get('created_at')),
                        processed_at=parse_date(row.get('processed_at')) if pd.notna(row.get('processed_at')) else None
                    )
                    
                    db.session.add(callback)
                    imported += 1
                
            except Exception as e:
                print(f"Ошибка импорта запроса {index}: {e}")
                continue
        
        if imported > 0:
            db.session.commit()
            print(f"✅ Импортировано запросов обратного звонка: {imported}")
        else:
            print("⚠️ Модель CallbackRequest не найдена или нет данных")
        
    except Exception as e:
        print(f"❌ Ошибка импорта запросов обратного звонка: {e}")
        db.session.rollback()

def main():
    """Основная функция полного импорта"""
    with app.app_context():
        print("🚀 ПОЛНЫЙ ИМПОРТ ВСЕХ ДАННЫХ")
        print("=" * 60)
        
        # Импортируем все данные
        import_admins()
        import_streets()
        import_managers()
        import_blog_articles()
        import_favorites()
        import_callback_requests()
        
        # Финальная статистика
        print("\n" + "=" * 60)
        print("📊 ФИНАЛЬНАЯ СТАТИСТИКА")
        
        try:
            users_count = User.query.count()
            developers_count = Developer.query.count()
            complexes_count = ResidentialComplex.query.count()
            categories_count = BlogCategory.query.count() if 'BlogCategory' in globals() else 0
            streets_count = Street.query.count() if 'Street' in globals() else 0
            managers_count = Manager.query.count() if 'Manager' in globals() else 0
            
            print(f"Пользователи: {users_count}")
            print(f"Застройщики: {developers_count}")
            print(f"Жилые комплексы: {complexes_count}")
            print(f"Категории блога: {categories_count}")
            print(f"Улицы: {streets_count}")
            print(f"Менеджеры: {managers_count}")
            
        except Exception as e:
            print(f"Ошибка получения статистики: {e}")
        
        print("\n✅ ПОЛНЫЙ ИМПОРТ ЗАВЕРШЕН!")

if __name__ == "__main__":
    main()