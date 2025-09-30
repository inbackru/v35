#!/usr/bin/env python3
"""
Create test search recommendations to demonstrate the integration
"""
import os
import sys
import json
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Manager, SentSearch

def create_test_data():
    """Create test search recommendations"""
    with app.app_context():
        # Find or create test user
        test_user = User.query.filter_by(email='test@inback.ru').first()
        if not test_user:
            print("Test user not found. Creating one...")
            test_user = User(
                email='test@inback.ru',
                full_name='Тестовый Пользователь',
                phone='+7900123456',
                role='buyer',
                password_hash='dummy_hash'
            )
            db.session.add(test_user)
            db.session.commit()
        
        # Find or create test manager
        test_manager = Manager.query.filter_by(email='manager@inback.ru').first()
        if not test_manager:
            print("Test manager not found. Creating one...")
            test_manager = Manager(
                name='Анна Менеджер',
                email='manager@inback.ru',
                phone='+7900654321',
                specialization='Центральный район'
            )
            db.session.add(test_manager)
            db.session.commit()

        # Create test search recommendations
        searches = [
            {
                'name': '2-3 комнатные в центре',
                'description': 'Подбор квартир 2-3 комнаты в центральных районах до 5 млн рублей',
                'filters': json.dumps({
                    'rooms': ['2', '3'],
                    'districts': ['Центральный'],
                    'price_max': 5000000
                }),
                'status': 'sent'
            },
            {
                'name': 'Новостройки с хорошей транспортной доступностью',
                'description': 'Квартиры в новых ЖК с развитой инфраструктурой',
                'filters': json.dumps({
                    'completion': ['2025', '2024'],
                    'rooms': ['1', '2']
                }),
                'status': 'sent'
            },
            {
                'name': 'Инвестиционные квартиры-студии',
                'description': 'Студии для сдачи в аренду в перспективных районах',
                'filters': json.dumps({
                    'rooms': ['0'],  # Studios
                    'price_max': 3000000
                }),
                'status': 'viewed'
            }
        ]

        # Delete existing test searches to avoid duplicates
        SentSearch.query.filter_by(client_id=test_user.id).delete()
        
        for search_data in searches:
            sent_search = SentSearch(
                name=search_data['name'],
                description=search_data['description'],
                client_id=test_user.id,
                manager_id=test_manager.id,
                additional_filters=search_data['filters'],
                status=search_data['status'],
                sent_at=datetime.utcnow() - timedelta(days=1),
                viewed_at=datetime.utcnow() if search_data['status'] == 'viewed' else None
            )
            db.session.add(sent_search)
            print(f"Created search recommendation: {search_data['name']}")

        db.session.commit()
        print(f"\n✅ Successfully created {len(searches)} test search recommendations!")
        print(f"User: {test_user.email}")
        print(f"Manager: {test_manager.name}")

if __name__ == '__main__':
    create_test_data()