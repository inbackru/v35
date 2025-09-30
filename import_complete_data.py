#!/usr/bin/env python3
"""
Complete import script with proper datetime handling
All users password: demo123
"""

import pandas as pd
import json
from flask import Flask
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
import re

def clean_datetime(date_str):
    """Clean datetime string from JavaScript format"""
    if pd.isna(date_str) or date_str == '':
        return datetime.utcnow()
    
    try:
        # Handle JavaScript datetime format
        if isinstance(date_str, str) and 'GMT' in date_str:
            # Extract the date part before GMT
            clean_date = re.sub(r' GMT.*', '', str(date_str))
            return pd.to_datetime(clean_date, errors='coerce')
        
        # Try direct conversion
        return pd.to_datetime(date_str, errors='coerce')
    except:
        return datetime.utcnow()

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

def import_users():
    """Import users with fixed datetime"""
    print("\n👥 Импортируем пользователей...")
    df = load_excel_data('users (5)_1756031503648.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            email = str(row.get('email', f'user{imported}@test.com')).strip()
            if not email or email == 'nan':
                email = f'user{imported}@test.com'
                
            # Check if user already exists
            existing = User.query.filter_by(email=email).first()
            if existing:
                continue
                
            user = User(
                email=email,
                phone=str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else '',
                full_name=str(row.get('full_name', f'Пользователь {imported}')).strip(),
                password_hash=password_hash,
                user_id=str(row.get('user_id', f'CB{1000 + imported}')).strip(),
                role=str(row.get('role', 'buyer')).strip(),
                is_active=True,
                is_verified=True,
                profile_image=str(row.get('profile_image', 'https://randomuser.me/api/portraits/men/32.jpg')).strip(),
                telegram_id=str(row.get('telegram_id', '')).strip() if pd.notna(row.get('telegram_id')) else '',
                preferred_contact=str(row.get('preferred_contact', 'email')).strip(),
                email_notifications=True,
                telegram_notifications=bool(row.get('telegram_notifications', False)),
                registration_source=str(row.get('registration_source', 'Website')).strip(),
                client_status=str(row.get('client_status', 'Новый')).strip(),
                preferred_district=str(row.get('preferred_district', '')).strip() if pd.notna(row.get('preferred_district')) else '',
                property_type=str(row.get('property_type', '')).strip() if pd.notna(row.get('property_type')) else '',
                room_count=str(row.get('room_count', '')).strip() if pd.notna(row.get('room_count')) else '',
                budget_range=str(row.get('budget_range', '')).strip() if pd.notna(row.get('budget_range')) else '',
                quiz_completed=bool(row.get('quiz_completed', False)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(user)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта пользователя: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} пользователей")

def import_managers():
    """Import managers with fixed datetime"""
    print("\n👔 Импортируем менеджеров...")
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
                full_name=str(row.get('full_name', f'Менеджер {imported}')).strip(),
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
            db.session.add(manager)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта менеджера: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} менеджеров")

def import_admins():
    """Import admins with fixed datetime"""
    print("\n🔑 Импортируем администраторов...")
    df = load_excel_data('admins (4)_1756031513986.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            email = str(row.get('email', f'admin{imported}@test.com')).strip()
            if not email or email == 'nan':
                email = f'admin{imported}@test.com'
                
            # Check if admin already exists
            existing = Admin.query.filter_by(email=email).first()
            if existing:
                continue
                
            admin = Admin(
                email=email,
                phone=str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else '',
                full_name=str(row.get('full_name', f'Администратор {imported}')).strip(),
                password_hash=password_hash,
                position=str(row.get('position', 'Администратор')).strip(),
                is_active=True,
                profile_image=str(row.get('profile_image', 'https://randomuser.me/api/portraits/men/50.jpg')).strip(),
                telegram_id=str(row.get('telegram_id', '')).strip() if pd.notna(row.get('telegram_id')) else '',
                access_level=str(row.get('access_level', 'full')).strip(),
                can_manage_users=True,
                can_manage_content=True,
                can_manage_finances=True,
                can_manage_system=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(admin)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта администратора: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} администраторов")

def import_developers():
    """Import developers"""
    print("\n🏗️ Импортируем застройщиков...")
    df = load_excel_data('developers (4)_1756031503650.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            name = str(row.get('name', f'Застройщик {imported}')).strip()
            
            # Check if developer already exists
            existing = Developer.query.filter_by(name=name).first()
            if existing:
                continue
                
            developer = Developer(
                name=name,
                slug=name.lower().replace(' ', '-').replace('«', '').replace('»', ''),
                full_name=str(row.get('full_name', name)).strip(),
                established_year=int(row.get('established_year', 2010)) if pd.notna(row.get('established_year')) else 2010,
                description=str(row.get('description', '')).strip() if pd.notna(row.get('description')) else '',
                logo_url=str(row.get('logo_url', '')).strip() if pd.notna(row.get('logo_url')) else '',
                phone=str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else '',
                email=str(row.get('email', '')).strip() if pd.notna(row.get('email')) else '',
                website=str(row.get('website', '')).strip() if pd.notna(row.get('website')) else '',
                address=str(row.get('address', '')).strip() if pd.notna(row.get('address')) else '',
                latitude=float(row.get('latitude', 45.035)) if pd.notna(row.get('latitude')) else 45.035,
                longitude=float(row.get('longitude', 38.975)) if pd.notna(row.get('longitude')) else 38.975,
                total_complexes=int(row.get('total_complexes', 0)) if pd.notna(row.get('total_complexes')) else 0,
                total_properties=int(row.get('total_properties', 0)) if pd.notna(row.get('total_properties')) else 0,
                properties_sold=int(row.get('properties_sold', 0)) if pd.notna(row.get('properties_sold')) else 0,
                rating=float(row.get('rating', 4.8)) if pd.notna(row.get('rating')) else 4.8,
                experience_years=int(row.get('experience_years', 10)) if pd.notna(row.get('experience_years')) else 10,
                min_price=int(row.get('min_price', 3000000)) if pd.notna(row.get('min_price')) else 3000000,
                max_cashback_percent=float(row.get('max_cashback_percent', 10.0)) if pd.notna(row.get('max_cashback_percent')) else 10.0,
                features='[]',
                infrastructure='[]',
                is_active=True,
                is_partner=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(developer)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта застройщика: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} застройщиков")

def import_blog_categories():
    """Import blog categories"""
    print("\n📂 Импортируем категории блога...")
    df = load_excel_data('blog_categories (3)_1756031503650.xlsx')
    if df is None:
        return
    
    imported = 0
    
    for _, row in df.iterrows():
        try:
            name = str(row.get('name', f'Категория {imported}')).strip()
            
            # Check if category already exists
            existing = BlogCategory.query.filter_by(name=name).first()
            if existing:
                continue
                
            category = BlogCategory(
                name=name,
                slug=name.lower().replace(' ', '-'),
                description=str(row.get('description', '')).strip() if pd.notna(row.get('description')) else '',
                color=str(row.get('color', 'blue')).strip(),
                is_active=True,
                sort_order=int(row.get('sort_order', 0)) if pd.notna(row.get('sort_order')) else 0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(category)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта категории блога: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} категорий блога")

def main():
    """Main import function"""
    print("🚀 Начинаем полный импорт данных из Excel файлов...")
    print("🔑 Все пользователи будут иметь пароль: demo123")
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Import data in proper order
        import_users()
        import_managers()
        import_admins()
        import_developers()
        import_blog_categories()
        
        # Get final statistics
        users_count = User.query.count()
        managers_count = Manager.query.count()
        admins_count = Admin.query.count()
        developers_count = Developer.query.count()
        blog_categories_count = BlogCategory.query.count()
        
        print("\n✅ Полный импорт завершен!")
        print("\n📊 Итоговая статистика:")
        print(f"   👥 Пользователи: {users_count}")
        print(f"   👔 Менеджеры: {managers_count}")
        print(f"   🔑 Администраторы: {admins_count}")
        print(f"   🏗️ Застройщики: {developers_count}")
        print(f"   📂 Категории блога: {blog_categories_count}")
        print(f"\n🔑 Пароль для всех пользователей: demo123")
        print("\n🎯 Теперь можно войти в систему с любым email и паролем demo123")

if __name__ == '__main__':
    main()