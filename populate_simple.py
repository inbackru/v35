#!/usr/bin/env python3
"""
Упрощенный скрипт для заполнения базы данных основными тестовыми данными
"""
import json
import random
from datetime import datetime, timedelta
from app import app, db
from models import (
    User, Manager, Admin, BlogPost, Collection, CollectionProperty, 
    CashbackApplication, FavoriteProperty, SavedSearch, UserNotification,
    CashbackRecord, Application, Favorite, District, Developer,
    ResidentialComplex, SearchCategory, SentSearch
)

def create_test_users():
    """Создание тестовых пользователей"""
    print("\n📝 Создаем тестовых пользователей...")
    
    users_data = [
        {
            'email': 'demo@inback.ru',
            'full_name': 'Демо Пользователь',
            'phone': '+7-918-123-45-67',
            'role': 'buyer',
            'is_demo': True,
            'is_verified': True,
            'client_status': 'Активный'
        },
        {
            'email': 'ivan.petrov@email.ru',
            'full_name': 'Иван Петров',
            'phone': '+7-918-234-56-78',
            'role': 'buyer',
            'client_status': 'Активный'
        },
        {
            'email': 'maria.sidorova@email.ru',
            'full_name': 'Мария Сидорова',
            'phone': '+7-918-345-67-89',
            'role': 'buyer',
            'client_status': 'Новый'
        },
        {
            'email': 'alex.kozlov@email.ru',
            'full_name': 'Александр Козлов',
            'phone': '+7-918-456-78-90',
            'role': 'buyer',
            'client_status': 'В работе'
        },
        {
            'email': 'elena.smirnova@email.ru',
            'full_name': 'Елена Смирнова',
            'phone': '+7-918-567-89-01',
            'role': 'buyer',
            'client_status': 'Активный'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            user = User(**user_data)
            user.set_password('demo123')
            db.session.add(user)
            created_users.append(user)
        else:
            created_users.append(existing_user)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_users)} пользователей")
    return created_users

def create_test_managers():
    """Создание тестовых менеджеров"""
    print("\n👥 Создаем тестовых менеджеров...")
    
    managers_data = [
        {
            'email': 'manager@inback.ru',
            'first_name': 'Демо',
            'last_name': 'Менеджер',
            'phone': '+7-918-111-22-33',
            'position': 'Старший менеджер'
        },
        {
            'email': 'anna.manager@inback.ru',
            'first_name': 'Анна',
            'last_name': 'Менеджерова',
            'phone': '+7-918-222-33-44',
            'position': 'Менеджер по продажам'
        }
    ]
    
    created_managers = []
    for manager_data in managers_data:
        existing_manager = Manager.query.filter_by(email=manager_data['email']).first()
        if not existing_manager:
            manager = Manager(**manager_data)
            manager.set_password('demo123')
            db.session.add(manager)
            created_managers.append(manager)
        else:
            created_managers.append(existing_manager)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_managers)} менеджеров")
    return created_managers

def create_test_admins():
    """Создание тестовых администраторов"""
    print("\n🔑 Создаем тестовых администраторов...")
    
    admins_data = [
        {
            'email': 'admin@inback.ru',
            'full_name': 'Супер Администратор',
            'phone': '+7-918-000-11-22',
            'role': 'Super Admin',
            'is_super_admin': True
        }
    ]
    
    created_admins = []
    for admin_data in admins_data:
        existing_admin = Admin.query.filter_by(email=admin_data['email']).first()
        if not existing_admin:
            admin = Admin(**admin_data)
            admin.set_password('admin123')
            db.session.add(admin)
            created_admins.append(admin)
        else:
            created_admins.append(existing_admin)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_admins)} администраторов")
    return created_admins

def create_districts_and_developers():
    """Создание районов и застройщиков"""
    print("\n🏘️ Создаем районы и застройщиков...")
    
    # Создаем районы
    districts_data = [
        'Центральный', 'Западный', 'Северный', 'Карасунский', 
        'Прикубанский', 'Фестивальный', 'Юбилейный', 'Комсомольский'
    ]
    
    created_districts = []
    for district_name in districts_data:
        slug = district_name.lower().replace(' ', '-').replace('ый', 'y').replace('ий', 'y')
        existing_district = District.query.filter_by(name=district_name).first()
        if not existing_district:
            district = District(name=district_name, slug=slug)
            db.session.add(district)
            created_districts.append(district)
        else:
            created_districts.append(existing_district)
    
    # Создаем застройщиков
    developers_data = [
        'ГК "Инвестстройкуб"', 'СК "Стройград"', 'ООО "Кубань Строй"',
        'ГК "Премьер"', 'СК "Новый дом"'
    ]
    
    created_developers = []
    for dev_name in developers_data:
        slug = dev_name.lower().replace(' ', '-').replace('«', '').replace('»', '').replace('"', '').replace('.', '')
        existing_developer = Developer.query.filter_by(name=dev_name).first()
        if not existing_developer:
            developer = Developer(name=dev_name, slug=slug)
            db.session.add(developer)
            created_developers.append(developer)
        else:
            created_developers.append(existing_developer)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_districts)} районов")
    print(f"✓ Создано/найдено {len(created_developers)} застройщиков")
    
    return created_districts, created_developers

def create_residential_complexes(developers, districts):
    """Создание жилых комплексов"""
    print("\n🏢 Создаем жилые комплексы...")
    
    complexes_data = [
        {'name': 'ЖК «Первое место»', 'developer_idx': 0, 'district_idx': 4},
        {'name': 'ЖК «Солнечный город»', 'developer_idx': 1, 'district_idx': 0},
        {'name': 'ЖК «Премьер парк»', 'developer_idx': 3, 'district_idx': 0},
        {'name': 'ЖК «Кубанские просторы»', 'developer_idx': 2, 'district_idx': 3},
        {'name': 'ЖК «Новый квартал»', 'developer_idx': 4, 'district_idx': 1},
        {'name': 'ЖК «Центральный парк»', 'developer_idx': 0, 'district_idx': 0},
        {'name': 'ЖК «Мечта»', 'developer_idx': 1, 'district_idx': 2},
        {'name': 'ЖК «Зеленый берег»', 'developer_idx': 2, 'district_idx': 4}
    ]
    
    created_complexes = []
    for complex_data in complexes_data:
        existing_complex = ResidentialComplex.query.filter_by(name=complex_data['name']).first()
        if not existing_complex:
            complex_slug = complex_data['name'].lower().replace(' ', '-').replace('«', '').replace('»', '').replace('.', '')
            
            developer = developers[complex_data['developer_idx']] if complex_data['developer_idx'] < len(developers) else None
            district = districts[complex_data['district_idx']] if complex_data['district_idx'] < len(districts) else None
            
            complex_obj = ResidentialComplex(
                name=complex_data['name'],
                slug=complex_slug,
                developer_id=developer.id if developer else None,
                district_id=district.id if district else None
            )
            db.session.add(complex_obj)
            created_complexes.append(complex_obj)
        else:
            created_complexes.append(existing_complex)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_complexes)} жилых комплексов")
    return created_complexes

def create_search_categories():
    """Создание категорий поиска"""
    print("\n🔍 Создаем категории поиска...")
    
    categories_data = [
        {'name': 'Студии', 'category_type': 'rooms', 'slug': 'studio'},
        {'name': '1-комнатные', 'category_type': 'rooms', 'slug': '1-room'},
        {'name': '2-комнатные', 'category_type': 'rooms', 'slug': '2-room'},
        {'name': '3-комнатные и больше', 'category_type': 'rooms', 'slug': '3-plus-room'},
        {'name': 'До 5 млн', 'category_type': 'price', 'slug': 'under-5m'},
        {'name': 'От 5 до 10 млн', 'category_type': 'price', 'slug': '5m-10m'},
        {'name': 'Премиум', 'category_type': 'price', 'slug': 'premium'}
    ]
    
    created_categories = []
    for category_data in categories_data:
        existing_category = SearchCategory.query.filter_by(name=category_data['name']).first()
        if not existing_category:
            category = SearchCategory(**category_data)
            db.session.add(category)
            created_categories.append(category)
        else:
            created_categories.append(existing_category)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_categories)} категорий поиска")
    return created_categories

def create_test_data(users, managers):
    """Создание тестовых данных: избранное, заявки, уведомления"""
    print("\n📋 Создаем тестовые данные...")
    
    # Создаем избранные объекты
    favorites_created = 0
    for i, user in enumerate(users[:3]):  # Только для первых 3 пользователей
        for j in range(random.randint(2, 5)):
            existing_favorite = FavoriteProperty.query.filter_by(
                user_id=user.id, 
                property_id=f'prop_{i}_{j}'
            ).first()
            
            if not existing_favorite:
                favorite = FavoriteProperty(
                    user_id=user.id,
                    property_id=f'prop_{i}_{j}',
                    property_name=f"{random.choice(['1', '2', '3'])}-комн квартира",
                    property_type=random.choice(['1', '2', '3']),
                    property_size=random.randint(35, 120),
                    property_price=random.randint(3000000, 15000000),
                    complex_name=f'ЖК "Тестовый-{j+1}"',
                    developer_name='Тестовый застройщик',
                    cashback_amount=random.randint(50000, 300000),
                    cashback_percent=2.0
                )
                db.session.add(favorite)
                favorites_created += 1
    
    # Создаем заявки на кешбек
    applications_created = 0
    for i, user in enumerate(users[:4]):  # Только для первых 4 пользователей
        for j in range(random.randint(1, 3)):
            existing_app = CashbackApplication.query.filter_by(
                user_id=user.id,
                property_id=f'app_{i}_{j}'
            ).first()
            
            if not existing_app:
                price = random.randint(4000000, 12000000)
                cashback_amount = int(price * 0.02)
                application = CashbackApplication(
                    user_id=user.id,
                    property_id=f'app_{i}_{j}',
                    property_name=f"{random.choice(['1', '2', '3'])}-комн квартира",
                    property_type=random.choice(['1', '2', '3']),
                    property_size=random.randint(35, 120),
                    property_price=price,
                    complex_name=f'ЖК "Заявка-{j+1}"',
                    developer_name='Застройщик заявок',
                    cashback_amount=cashback_amount,
                    cashback_percent=2.0,
                    status=random.choice(['На рассмотрении', 'Одобрена', 'Выплачена']),
                    approved_by_manager_id=managers[0].id if managers else None
                )
                db.session.add(application)
                applications_created += 1
    
    # Создаем уведомления
    notifications_created = 0
    notification_texts = [
        'Добро пожаловать на платформу!',
        'Ваша заявка на кешбек рассмотрена',
        'Новые объекты по вашим критериям',
        'Изменение цен в избранных ЖК'
    ]
    
    for user in users:
        for text in random.sample(notification_texts, 2):
            notification = UserNotification(
                user_id=user.id,
                title='Уведомление',
                message=text,
                notification_type='info',
                is_read=random.choice([True, False])
            )
            db.session.add(notification)
            notifications_created += 1
    
    # Создаем сохраненные поиски
    searches_created = 0
    for user in users[:3]:
        search_params = [
            '{"rooms": ["1"], "price_max": 5000000}',
            '{"rooms": ["2", "3"], "district": "Центральный"}',
            '{"price_min": 3000000, "price_max": 8000000}'
        ]
        
        for params in random.sample(search_params, 1):
            saved_search = SavedSearch(
                user_id=user.id,
                name=f"Поиск {random.randint(1, 100)}",
                filters=params,
                is_active=True
            )
            db.session.add(saved_search)
            searches_created += 1
    
    db.session.commit()
    
    print(f"✓ Создано {favorites_created} избранных объектов")
    print(f"✓ Создано {applications_created} заявок на кешбек")
    print(f"✓ Создано {notifications_created} уведомлений")
    print(f"✓ Создано {searches_created} сохраненных поисков")

def create_blog_posts(admins):
    """Создание тестовых статей блога"""
    print("\n📝 Создаем статьи блога...")
    
    if not admins:
        print("⚠️ Нет администраторов для создания статей")
        return []
    
    blog_posts_data = [
        {
            'title': 'Как выбрать квартиру в новостройке',
            'content': 'Полное руководство по выбору квартиры в новостройке. При выборе квартиры в новостройке важно учитывать множество факторов: расположение, застройщика, планировку, инфраструктуру и сроки сдачи объекта.',
            'excerpt': 'Основные критерии выбора квартиры в новостройке',
            'category': 'Советы покупателям',
            'status': 'published'
        },
        {
            'title': 'Ипотека в 2024 году: все что нужно знать',
            'content': 'Актуальная информация об ипотечных программах 2024 года. Льготные программы, условия банков, требования к заемщикам.',
            'excerpt': 'Обзор ипотечных программ и условий',
            'category': 'Ипотека', 
            'status': 'published'
        },
        {
            'title': 'Инвестиции в недвижимость Краснодара',
            'content': 'Анализ рынка недвижимости Краснодара для инвесторов. Перспективные районы, доходность, риски.',
            'excerpt': 'Перспективы инвестиций в краснодарскую недвижимость',
            'category': 'Инвестиции',
            'status': 'published'
        }
    ]
    
    created_posts = []
    for post_data in blog_posts_data:
        existing_post = BlogPost.query.filter_by(title=post_data['title']).first()
        if not existing_post:
            post = BlogPost(
                title=post_data['title'],
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                category=post_data['category'],
                status=post_data['status'],
                author_id=admins[0].id,
                published_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(post)
            created_posts.append(post)
        else:
            created_posts.append(existing_post)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_posts)} статей блога")
    return created_posts

def assign_users_to_managers(users, managers):
    """Назначение пользователей менеджерам"""
    print("\n👥 Назначаем пользователей менеджерам...")
    
    if not managers:
        print("⚠️ Нет менеджеров для назначения")
        return
    
    assigned_count = 0
    for i, user in enumerate(users):
        if not user.assigned_manager_id:  # Если еще не назначен
            manager = managers[i % len(managers)]
            user.assigned_manager_id = manager.id
            assigned_count += 1
    
    db.session.commit()
    print(f"✓ Назначено {assigned_count} пользователей менеджерам")

def main():
    """Основная функция"""
    print("🚀 Начинаем заполнение базы данных тестовыми данными...")
    
    with app.app_context():
        # Создаем базовые данные
        users = create_test_users()
        managers = create_test_managers()
        admins = create_test_admins()
        
        # Создаем справочники
        districts, developers = create_districts_and_developers()
        residential_complexes = create_residential_complexes(developers, districts)
        search_categories = create_search_categories()
        
        # Создаем связанные данные
        assign_users_to_managers(users, managers)
        create_test_data(users, managers)
        blog_posts = create_blog_posts(admins)
        
        print("\n✅ Заполнение базы данных завершено!")
        print("\n📊 Статистика:")
        print(f"   👥 Пользователи: {len(users)}")
        print(f"   🏢 Менеджеры: {len(managers)}")
        print(f"   🔑 Администраторы: {len(admins)}")
        print(f"   🏘️ Районы: {len(districts)}")
        print(f"   🏗️ Застройщики: {len(developers)}")
        print(f"   🏢 Жилые комплексы: {len(residential_complexes)}")
        print(f"   🔍 Категории поиска: {len(search_categories)}")
        print(f"   📝 Статьи блога: {len(blog_posts)}")
        
        print(f"\n🔐 Тестовые аккаунты:")
        print(f"   📧 Пользователь: demo@inback.ru / demo123")
        print(f"   👥 Менеджер: manager@inback.ru / demo123")
        print(f"   🔑 Администратор: admin@inback.ru / admin123")

if __name__ == '__main__':
    main()