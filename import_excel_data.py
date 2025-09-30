#!/usr/bin/env python3
"""
Import real data from Excel files to populate the database
All users will have password: demo123
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

def import_users():
    """Import users from Excel"""
    print("\n👥 Импортируем пользователей...")
    df = load_excel_data('users (5)_1756031503648.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            # Check if user already exists
            existing = User.query.filter_by(email=row.get('email', '')).first()
            if existing:
                continue
                
            user = User(
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                full_name=row.get('full_name', ''),
                password_hash=password_hash,
                user_id=row.get('user_id', f'CB{1000 + imported}'),
                role=row.get('role', 'buyer'),
                is_active=True,
                is_verified=True,
                profile_image=row.get('profile_image', 'https://randomuser.me/api/portraits/men/32.jpg'),
                telegram_id=row.get('telegram_id', ''),
                preferred_contact=row.get('preferred_contact', 'email'),
                email_notifications=True,
                telegram_notifications=row.get('telegram_notifications', False),
                registration_source=row.get('registration_source', 'Website'),
                client_status=row.get('client_status', 'Новый'),
                preferred_district=row.get('preferred_district', ''),
                property_type=row.get('property_type', ''),
                room_count=row.get('room_count', ''),
                budget_range=row.get('budget_range', ''),
                quiz_completed=row.get('quiz_completed', False),
                created_at=pd.to_datetime(row.get('created_at', datetime.utcnow())),
                updated_at=pd.to_datetime(row.get('updated_at', datetime.utcnow()))
            )
            db.session.add(user)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта пользователя: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} пользователей")

def import_managers():
    """Import managers from Excel"""
    print("\n👔 Импортируем менеджеров...")
    df = load_excel_data('managers (4)_1756031513985.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            # Check if manager already exists
            existing = Manager.query.filter_by(email=row.get('email', '')).first()
            if existing:
                continue
                
            manager = Manager(
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                full_name=row.get('full_name', ''),
                password_hash=password_hash,
                position=row.get('position', 'Менеджер по продажам'),
                department=row.get('department', 'Продажи'),
                hire_date=pd.to_datetime(row.get('hire_date', datetime.utcnow())),
                is_active=True,
                profile_image=row.get('profile_image', 'https://randomuser.me/api/portraits/men/45.jpg'),
                telegram_id=row.get('telegram_id', ''),
                manager_id=row.get('manager_id', f'MNG{1000 + imported}'),
                role=row.get('role', 'manager'),
                total_sales=row.get('total_sales', 0),
                monthly_target=row.get('monthly_target', 10),
                commission_rate=row.get('commission_rate', 2.5),
                access_level=row.get('access_level', 'standard'),
                is_team_leader=row.get('is_team_leader', False),
                created_at=pd.to_datetime(row.get('created_at', datetime.utcnow())),
                updated_at=pd.to_datetime(row.get('updated_at', datetime.utcnow()))
            )
            db.session.add(manager)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта менеджера: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} менеджеров")

def import_admins():
    """Import admins from Excel"""
    print("\n🔑 Импортируем администраторов...")
    df = load_excel_data('admins (4)_1756031513986.xlsx')
    if df is None:
        return
    
    imported = 0
    password_hash = generate_password_hash('demo123')
    
    for _, row in df.iterrows():
        try:
            # Check if admin already exists
            existing = Admin.query.filter_by(email=row.get('email', '')).first()
            if existing:
                continue
                
            admin = Admin(
                email=row.get('email', ''),
                phone=row.get('phone', ''),
                full_name=row.get('full_name', ''),
                password_hash=password_hash,
                position=row.get('position', 'Администратор'),
                is_active=True,
                profile_image=row.get('profile_image', 'https://randomuser.me/api/portraits/men/50.jpg'),
                telegram_id=row.get('telegram_id', ''),
                access_level=row.get('access_level', 'full'),
                can_manage_users=True,
                can_manage_content=True,
                can_manage_finances=True,
                can_manage_system=True,
                created_at=pd.to_datetime(row.get('created_at', datetime.utcnow())),
                updated_at=pd.to_datetime(row.get('updated_at', datetime.utcnow()))
            )
            db.session.add(admin)
            imported += 1
        except Exception as e:
            print(f"   Ошибка импорта администратора: {e}")
            continue
    
    db.session.commit()
    print(f"✓ Импортировано {imported} администраторов")

def main():
    """Main import function"""
    print("🚀 Начинаем импорт данных из Excel файлов...")
    print("🔑 Все пользователи будут иметь пароль: demo123")
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Import basic data
        import_users()
        import_managers()
        import_admins()
        
        # Get final statistics
        users_count = User.query.count()
        managers_count = Manager.query.count()
        admins_count = Admin.query.count()
        
        print("\n✅ Импорт завершен!")
        print("\n📊 Итоговая статистика:")
        print(f"   👥 Пользователи: {users_count}")
        print(f"   👔 Менеджеры: {managers_count}")
        print(f"   🔑 Администраторы: {admins_count}")
        print(f"\n🔑 Пароль для всех пользователей: demo123")

if __name__ == '__main__':
    main()
