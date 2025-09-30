#!/usr/bin/env python3
"""
Create demo data for testing
"""

from app import db, app
from models import User, Manager, Admin, Collection, CollectionProperty
from werkzeug.security import generate_password_hash
from datetime import datetime
import secrets

def create_demo_data():
    """Create demo users and data"""
    with app.app_context():
        # Create admin user
        admin = Admin(
            email='admin@inback.ru',
            password_hash=generate_password_hash('demo123'),
            first_name='Администратор',
            last_name='Системы',
            is_active=True
        )
        db.session.add(admin)
        
        # Create manager
        manager = Manager(
            email='manager@inback.ru',
            password_hash=generate_password_hash('demo123'),
            first_name='Иван',
            last_name='Менеджеров',
            phone='+7 (900) 123-45-67',
            is_active=True
        )
        db.session.add(manager)
        
        # Create demo client
        user_id = secrets.token_hex(4).upper()
        user = User(
            first_name='Демо',
            last_name='Покупатель',
            email='demo@inback.ru',
            phone='+7 (900) 111-22-33',
            password_hash=generate_password_hash('demo123'),
            user_id=user_id,
            assigned_manager_id=1,  # Will be set after manager is created
            client_status='Новый'
        )
        db.session.add(user)
        
        try:
            db.session.commit()
            
            # Update user with correct manager ID
            user.assigned_manager_id = manager.id
            db.session.commit()
            
            # Create demo collection
            collection = Collection(
                title='Лучшие квартиры в центре',
                description='Подборка квартир в центральных районах Краснодара с максимальным кешбеком',
                created_by_manager_id=manager.id,
                assigned_to_user_id=user.id,
                status='Отправлена',
                sent_at=datetime.utcnow(),
                tags='центр,новостройка,кешбек'
            )
            db.session.add(collection)
            db.session.commit()
            
            # Add properties to collection
            properties = [
                CollectionProperty(
                    collection_id=collection.id,
                    property_id='1',
                    property_name='2-комн в ЖК "Солнечный"',
                    property_price=5500000,
                    complex_name='ЖК "Солнечный"',
                    property_type='2-комн',
                    property_size=65.5,
                    manager_note='Отличная планировка, вид на парк',
                    order_index=1
                ),
                CollectionProperty(
                    collection_id=collection.id,
                    property_id='2',
                    property_name='3-комн в ЖК "Центральный"',
                    property_price=7200000,
                    complex_name='ЖК "Центральный"',
                    property_type='3-комн',
                    property_size=88.2,
                    manager_note='Премиум класс, готова к заселению',
                    order_index=2
                )
            ]
            
            for prop in properties:
                db.session.add(prop)
            
            db.session.commit()
            print("Demo data created successfully!")
            print("Users created:")
            print("- Admin: admin@inback.ru / demo123")
            print("- Manager: manager@inback.ru / demo123")
            print("- Client: demo@inback.ru / demo123")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating demo data: {e}")

if __name__ == "__main__":
    create_demo_data()