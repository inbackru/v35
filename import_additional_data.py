#!/usr/bin/env python3
"""
Import additional data from Excel files
Saved searches, applications, callbacks, etc.
"""

import pandas as pd
import json
from flask import Flask
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

def load_excel_data(filename):
    """Load data from Excel file"""
    try:
        full_path = os.path.join('attached_assets', filename)
        if os.path.exists(full_path):
            print(f"📊 Загружаем {filename}...")
            df = pd.read_excel(full_path)
            print(f"   Найдено {len(df)} записей")
            return df
        else:
            print(f"❌ Файл {filename} не найден")
            return None
    except Exception as e:
        print(f"❌ Ошибка загрузки {filename}: {e}")
        return None

def import_additional_managers():
    """Import additional managers"""
    print("\n👔 Импортируем дополнительных менеджеров...")
    df = load_excel_data('managers (4)_1756031513985.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            email = str(row.get('email', f'manager{imported}@test.com')).strip()
            if not email or email == 'nan':
                email = f'manager{imported}@test.com'
                
            # Check if manager already exists
            existing = Manager.query.filter_by(email=email).first()
            if existing:
                continue
                
            manager = Manager(
                email=email,
                phone=str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else '',
                password_hash=password_hash,
                position=str(row.get('position', 'Менеджер по продажам')).strip(),
                department=str(row.get('department', 'Продажи')).strip(),
                hire_date=datetime.utcnow(),
                is_active=True,
                profile_image=str(row.get('profile_image', 'https://randomuser.me/api/portraits/men/45.jpg')).strip(),
                telegram_id=str(row.get('telegram_id', '')).strip() if pd.notna(row.get('telegram_id')) else '',
                manager_id=str(row.get('manager_id', f'MNG{1000 + imported}')).strip(),
                role=str(row.get('role', 'manager')).strip(),
                total_sales=int(row.get('total_sales', 0)) if pd.notna(row.get('total_sales')) else 0,
                monthly_target=int(row.get('monthly_target', 10)) if pd.notna(row.get('monthly_target')) else 10,
                commission_rate=float(row.get('commission_rate', 2.5)) if pd.notna(row.get('commission_rate')) else 2.5,
                access_level=str(row.get('access_level', 'standard')).strip(),
                is_team_leader=bool(row.get('is_team_leader', False)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            # Set full_name separately to avoid setter issues
            manager.first_name = str(row.get('full_name', f'Менеджер {imported}')).strip()
            db.session.add(manager)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта менеджера: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} дополнительных менеджеров")

def import_residential_complexes():
    """Import residential complexes"""
    print("\n🏢 Импортируем жилые комплексы...")
    df = load_excel_data('residential_complexes (4)_1756031513987.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            name = str(row.get('name', f'ЖК {imported}')).strip()
            
            # Check if complex already exists
            existing = ResidentialComplex.query.filter_by(name=name).first()
            if existing:
                continue
                
            # Find developer by name
            developer = None
            if pd.notna(row.get('developer_name')):
                developer = Developer.query.filter_by(name=str(row.get('developer_name')).strip()).first()
            
            complex_obj = ResidentialComplex(
                name=name,
                slug=name.lower().replace(' ', '-').replace('«', '').replace('»', ''),
                developer_id=developer.id if developer else None,
                developer_name=str(row.get('developer_name', '')).strip() if pd.notna(row.get('developer_name')) else '',
                address=str(row.get('address', '')).strip() if pd.notna(row.get('address')) else '',
                district=str(row.get('district', '')).strip() if pd.notna(row.get('district')) else '',
                latitude=float(row.get('latitude', 45.035)) if pd.notna(row.get('latitude')) else 45.035,
                longitude=float(row.get('longitude', 38.975)) if pd.notna(row.get('longitude')) else 38.975,
                construction_start=datetime.utcnow(),
                construction_end=datetime.utcnow(),
                status=str(row.get('status', 'В продаже')).strip(),
                total_apartments=int(row.get('total_apartments', 100)) if pd.notna(row.get('total_apartments')) else 100,
                available_apartments=int(row.get('available_apartments', 50)) if pd.notna(row.get('available_apartments')) else 50,
                min_price=int(row.get('min_price', 3000000)) if pd.notna(row.get('min_price')) else 3000000,
                max_price=int(row.get('max_price', 8000000)) if pd.notna(row.get('max_price')) else 8000000,
                min_area=float(row.get('min_area', 30)) if pd.notna(row.get('min_area')) else 30,
                max_area=float(row.get('max_area', 120)) if pd.notna(row.get('max_area')) else 120,
                floors=int(row.get('floors', 16)) if pd.notna(row.get('floors')) else 16,
                property_class=str(row.get('property_class', 'комфорт')).strip(),
                description=str(row.get('description', '')).strip() if pd.notna(row.get('description')) else '',
                features='[]',
                infrastructure='[]',
                transport='[]',
                parking=bool(row.get('parking', True)),
                security=bool(row.get('security', True)),
                playground=bool(row.get('playground', True)),
                fitness=bool(row.get('fitness', False)),
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(complex_obj)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта ЖК: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} жилых комплексов")

def import_blog_articles():
    """Import blog articles"""
    print("\n📝 Импортируем статьи блога...")
    df = load_excel_data('blog_articles (3)_1756031513986.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            title = str(row.get('title', f'Статья {imported}')).strip()
            
            # Check if article already exists
            existing = BlogPost.query.filter_by(title=title).first()
            if existing:
                continue
            
            # Find category by name
            category = None
            if pd.notna(row.get('category_name')):
                category = BlogCategory.query.filter_by(name=str(row.get('category_name')).strip()).first()
            
            # Find author by email
            author = None
            if pd.notna(row.get('author_email')):
                author = Admin.query.filter_by(email=str(row.get('author_email')).strip()).first()
                
            post = BlogPost(
                title=title,
                slug=title.lower().replace(' ', '-')[:50],
                excerpt=str(row.get('excerpt', '')).strip() if pd.notna(row.get('excerpt')) else '',
                content=str(row.get('content', '')).strip() if pd.notna(row.get('content')) else '',
                featured_image=str(row.get('featured_image', '')).strip() if pd.notna(row.get('featured_image')) else '',
                category_id=category.id if category else None,
                author_id=author.id if author else None,
                is_published=bool(row.get('is_published', True)),
                is_featured=bool(row.get('is_featured', False)),
                views_count=int(row.get('views_count', 0)) if pd.notna(row.get('views_count')) else 0,
                reading_time=int(row.get('reading_time', 5)) if pd.notna(row.get('reading_time')) else 5,
                meta_title=str(row.get('meta_title', title)).strip(),
                meta_description=str(row.get('meta_description', '')).strip() if pd.notna(row.get('meta_description')) else '',
                tags=str(row.get('tags', '')).strip() if pd.notna(row.get('tags')) else '',
                published_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(post)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта статьи: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} статей блога")

def import_callback_requests():
    """Import callback requests"""
    print("\n📞 Импортируем заявки на обратный звонок...")
    df = load_excel_data('callback_requests (2)_1756031513987.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            name = str(row.get('name', f'Клиент {imported}')).strip()
            phone = str(row.get('phone', '')).strip()
            
            if not phone:
                continue
                
            # Check if request already exists
            existing = CallbackRequest.query.filter_by(phone=phone, name=name).first()
            if existing:
                continue
            
            # Find assigned manager by email
            manager = None
            if pd.notna(row.get('assigned_manager_email')):
                manager = Manager.query.filter_by(email=str(row.get('assigned_manager_email')).strip()).first()
                
            callback = CallbackRequest(
                name=name,
                phone=phone,
                email=str(row.get('email', '')).strip() if pd.notna(row.get('email')) else None,
                preferred_time=str(row.get('preferred_time', '')).strip() if pd.notna(row.get('preferred_time')) else None,
                notes=str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None,
                interest=str(row.get('interest', '')).strip() if pd.notna(row.get('interest')) else None,
                budget=str(row.get('budget', '')).strip() if pd.notna(row.get('budget')) else None,
                timing=str(row.get('timing', '')).strip() if pd.notna(row.get('timing')) else None,
                status=str(row.get('status', 'Новая')).strip(),
                assigned_manager_id=manager.id if manager else None,
                manager_notes=str(row.get('manager_notes', '')).strip() if pd.notna(row.get('manager_notes')) else None,
                created_at=datetime.utcnow(),
                processed_at=datetime.utcnow() if row.get('status') != 'Новая' else None
            )
            db.session.add(callback)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта заявки: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} заявок на обратный звонок")

def import_saved_searches():
    """Import saved searches"""
    print("\n🔍 Импортируем сохраненные поиски...")
    df = load_excel_data('saved_searches (4)_1756031513985.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            search_name = str(row.get('search_name', f'Поиск {imported}')).strip()
            
            # Find user by email
            user = None
            if pd.notna(row.get('user_email')):
                user = User.query.filter_by(email=str(row.get('user_email')).strip()).first()
            
            if not user:
                continue
                
            # Check if search already exists
            existing = SavedSearch.query.filter_by(user_id=user.id, search_name=search_name).first()
            if existing:
                continue
                
            saved_search = SavedSearch(
                user_id=user.id,
                search_name=search_name,
                search_criteria=str(row.get('search_criteria', '{}')).strip(),
                notification_frequency=str(row.get('notification_frequency', 'weekly')).strip(),
                is_active=bool(row.get('is_active', True)),
                last_notified=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(saved_search)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта поиска: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} сохраненных поисков")

def main():
    """Main import function for additional data"""
    print("🚀 Импортируем дополнительные данные из Excel файлов...")
    
    with app.app_context():
        # Import additional data
        import_additional_managers()
        import_residential_complexes()
        import_blog_articles()
        import_callback_requests()
        import_saved_searches()
        
        # Get final statistics
        managers_count = Manager.query.count()
        complexes_count = ResidentialComplex.query.count()
        blog_posts_count = BlogPost.query.count()
        callback_count = CallbackRequest.query.count()
        saved_searches_count = SavedSearch.query.count()
        
        print("\n✅ Дополнительный импорт завершен!")
        print("\n📊 Обновленная статистика:")
        print(f"   👔 Менеджеры: {managers_count}")
        print(f"   🏢 Жилые комплексы: {complexes_count}")
        print(f"   📝 Статьи блога: {blog_posts_count}")
        print(f"   📞 Заявки на звонок: {callback_count}")
        print(f"   🔍 Сохраненные поиски: {saved_searches_count}")

if __name__ == '__main__':
    main()
