#!/usr/bin/env python3
"""
Create demo accounts for easy testing
"""

from flask import Flask
from app import app, db
from models import *
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_demo_accounts():
    """Create demo accounts with known credentials"""
    print("🎯 Создаем демо-аккаунты для тестирования...")
    
    with app.app_context():
        password_hash = generate_password_hash('demo123')
        
        # Demo Admin
        admin_email = 'admin@inback.ru'
        existing_admin = Admin.query.filter_by(email=admin_email).first()
        if not existing_admin:
            demo_admin = Admin(
                email=admin_email,
                phone='+7 (861) 123-45-67',
                full_name='Демо Администратор',
                password_hash=password_hash,
                position='Главный администратор',
                is_active=True,
                profile_image='https://randomuser.me/api/portraits/men/85.jpg',
                access_level='full',
                can_manage_users=True,
                can_manage_content=True,
                can_manage_finances=True,
                can_manage_system=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(demo_admin)
            print("✓ Создан демо администратор: admin@inback.ru")
        
        # Demo Manager
        manager_email = 'manager@inback.ru'
        existing_manager = Manager.query.filter_by(email=manager_email).first()
        if not existing_manager:
            demo_manager = Manager(
                email=manager_email,
                phone='+7 (861) 234-56-78',
                full_name='Демо Менеджер',
                password_hash=password_hash,
                position='Старший менеджер по продажам',
                department='Продажи',
                hire_date=datetime.utcnow(),
                is_active=True,
                profile_image='https://randomuser.me/api/portraits/women/68.jpg',
                manager_id='MNG001',
                role='manager',
                total_sales=15,
                monthly_target=20,
                commission_rate=3.0,
                access_level='standard',
                is_team_leader=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(demo_manager)
            print("✓ Создан демо менеджер: manager@inback.ru")
        
        # Demo User
        user_email = 'user@inback.ru'
        existing_user = User.query.filter_by(email=user_email).first()
        if not existing_user:
            demo_user = User(
                email=user_email,
                phone='+7 (861) 345-67-89',
                full_name='Демо Пользователь',
                password_hash=password_hash,
                user_id='CB001',
                role='buyer',
                is_active=True,
                is_verified=True,
                profile_image='https://randomuser.me/api/portraits/men/32.jpg',
                preferred_contact='email',
                email_notifications=True,
                telegram_notifications=False,
                registration_source='Website',
                client_status='Активный',
                preferred_district='Центральный',
                property_type='квартира',
                room_count='2',
                budget_range='5-8 млн',
                quiz_completed=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(demo_user)
            print("✓ Создан демо пользователь: user@inback.ru")
        
        db.session.commit()
        
        print("\n🎯 Демо-аккаунты готовы!")
        print("\n📝 Данные для входа:")
        print("   🔑 Администратор: admin@inback.ru / demo123")
        print("   👔 Менеджер: manager@inback.ru / demo123") 
        print("   👤 Пользователь: user@inback.ru / demo123")
        print("\n🌐 Все аккаунты готовы для тестирования функций сайта!")

if __name__ == '__main__':
    create_demo_accounts()
