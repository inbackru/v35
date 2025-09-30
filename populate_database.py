#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных тестовыми данными
"""
import json
import random
from datetime import datetime, timedelta
from app import app, db
from models import (
    User, Manager, Admin, BlogPost, Collection, CollectionProperty, 
    CashbackApplication, FavoriteProperty, SavedSearch, UserNotification,
    Recommendation, RecommendationCategory, ManagerSavedSearch,
    CashbackRecord, Application, Favorite, District, Developer,
    ResidentialComplex, SearchCategory, SentSearch
)

def load_json_data():
    """Загружаем данные из JSON файлов"""
    print("Загружаем данные из JSON файлов...")
    
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            properties = json.load(f)
        
        with open('data/residential_complexes.json', 'r', encoding='utf-8') as f:
            complexes = json.load(f)
        
        with open('data/developers.json', 'r', encoding='utf-8') as f:
            developers = json.load(f)
        
        print(f"✓ Загружено {len(properties)} объектов недвижимости")
        print(f"✓ Загружено {len(complexes)} жилых комплексов")  
        print(f"✓ Загружено {len(developers)} застройщиков")
        
        return properties, complexes, developers
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: файл не найден {e}")
        return [], [], []

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
        },
        {
            'email': 'dmitry.volkov@email.ru',
            'full_name': 'Дмитрий Волков',
            'phone': '+7-918-678-90-12',
            'role': 'buyer',
            'client_status': 'Новый'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Проверяем, существует ли уже пользователь с таким email
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
        },
        {
            'email': 'sergey.lead@inback.ru',
            'first_name': 'Сергей',
            'last_name': 'Руководителев',
            'phone': '+7-918-333-44-55',
            'position': 'Руководитель отдела'
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

def create_districts_and_developers(developers_data):
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
    created_developers = []
    for dev_data in developers_data:
        slug = dev_data['name'].lower().replace(' ', '-').replace('«', '').replace('»', '').replace('.', '')
        existing_developer = Developer.query.filter_by(name=dev_data['name']).first()
        if not existing_developer:
            developer = Developer(
                name=dev_data['name'],
                slug=slug
            )
            db.session.add(developer)
            created_developers.append(developer)
        else:
            created_developers.append(existing_developer)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_districts)} районов")
    print(f"✓ Создано/найдено {len(created_developers)} застройщиков")
    
    return created_districts, created_developers

def create_residential_complexes(complexes_data, developers, districts):
    """Создание жилых комплексов"""
    print("\n🏢 Создаем жилые комплексы...")
    
    created_complexes = []
    for complex_data in complexes_data:
        existing_complex = ResidentialComplex.query.filter_by(name=complex_data['name']).first()
        if not existing_complex:
            # Найдем застройщика
            developer = None
            if complex_data.get('developer'):
                developer = next((d for d in developers if d.name == complex_data['developer']), None)
            
            # Обработка координат (могут быть в виде массива [lat, lng])
            coordinates = complex_data.get('coordinates', [])
            latitude = None
            longitude = None
            if isinstance(coordinates, list) and len(coordinates) >= 2:
                latitude = coordinates[0]
                longitude = coordinates[1]
            elif isinstance(coordinates, dict):
                latitude = coordinates.get('lat')
                longitude = coordinates.get('lng')
            
            # Создаем slug для комплекса
            complex_slug = complex_data['name'].lower().replace(' ', '-').replace('«', '').replace('»', '').replace('.', '')
            
            # Найдем район
            district = None
            if complex_data.get('district'):
                district = next((d for d in districts if d.name in complex_data['district']), None)
            
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
        {
            'name': 'Студии',
            'category_type': 'rooms',
            'slug': 'studio'
        },
        {
            'name': '1-комнатные',
            'category_type': 'rooms', 
            'slug': '1-room'
        },
        {
            'name': '2-комнатные',
            'category_type': 'rooms',
            'slug': '2-room'
        },
        {
            'name': '3-комнатные и больше',
            'category_type': 'rooms',
            'slug': '3-plus-room'
        },
        {
            'name': 'До 5 млн',
            'category_type': 'price',
            'slug': 'under-5m'
        },
        {
            'name': 'От 5 до 10 млн',
            'category_type': 'price',
            'slug': '5m-10m'
        },
        {
            'name': 'Премиум',
            'category_type': 'price',
            'slug': 'premium'
        }
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

def create_recommendation_categories():
    """Создание категорий рекомендаций"""
    print("\n💡 Создаем категории рекомендаций...")
    
    rec_categories_data = [
        {
            'name': 'Семейные',
            'description': 'Квартиры для семей с детьми',
            'filters': json.dumps({'rooms': ['2', '3'], 'near_schools': True})
        },
        {
            'name': 'Инвестиционные',
            'description': 'Объекты для инвестиций',
            'filters': json.dumps({'rental_yield': 'high', 'location': 'center'})
        },
        {
            'name': 'Молодая семья',
            'description': 'Первое жилье для молодых семей',
            'filters': json.dumps({'price_max': 7000000, 'mortgage': True})
        },
        {
            'name': 'Премиум',
            'description': 'Элитное жилье',
            'filters': json.dumps({'price_min': 15000000, 'class': 'premium'})
        }
    ]
    
    created_rec_categories = []
    for rec_data in rec_categories_data:
        existing_rec = RecommendationCategory.query.filter_by(name=rec_data['name']).first()
        if not existing_rec:
            rec_category = RecommendationCategory(**rec_data)
            db.session.add(rec_category)
            created_rec_categories.append(rec_category)
        else:
            created_rec_categories.append(existing_rec)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_rec_categories)} категорий рекомендаций")
    return created_rec_categories

def create_test_data(users, managers, properties):
    """Создание тестовых данных: избранное, заявки, уведомления"""
    print("\n📋 Создаем тестовые данные...")
    
    # Создаем избранные объекты
    favorites_created = 0
    for user in users[:3]:  # Только для первых 3 пользователей
        user_properties = random.sample(properties, min(5, len(properties)))
        for prop in user_properties:
            existing_favorite = FavoriteProperty.query.filter_by(
                user_id=user.id, 
                property_id=prop.get('id', '')
            ).first()
            
            if not existing_favorite:
                favorite = FavoriteProperty(
                    user_id=user.id,
                    property_id=prop.get('id', ''),
                    property_name=f"{prop.get('rooms', 'N/A')}-комн квартира",
                    property_type=prop.get('rooms', ''),
                    property_size=prop.get('area', 0),
                    property_price=prop.get('price', 0),
                    complex_name=prop.get('complex', ''),
                    developer_name=prop.get('developer', ''),
                    cashback_amount=int(prop.get('price', 0) * 0.02) if prop.get('price') else 0,
                    cashback_percent=2.0
                )
                db.session.add(favorite)
                favorites_created += 1
    
    # Создаем заявки на кешбек
    applications_created = 0
    for user in users[:4]:  # Только для первых 4 пользователей
        user_properties = random.sample(properties, min(2, len(properties)))
        for prop in user_properties:
            existing_app = CashbackApplication.query.filter_by(
                user_id=user.id,
                property_id=prop.get('id', '')
            ).first()
            
            if not existing_app:
                cashback_amount = int(prop.get('price', 0) * 0.02) if prop.get('price') else 0
                application = CashbackApplication(
                    user_id=user.id,
                    property_id=prop.get('id', ''),
                    property_name=f"{prop.get('rooms', 'N/A')}-комн квартира",
                    property_type=prop.get('rooms', ''),
                    property_size=prop.get('area', 0),
                    property_price=prop.get('price', 0),
                    complex_name=prop.get('complex', ''),
                    developer_name=prop.get('developer', ''),
                    cashback_amount=cashback_amount,
                    cashback_percent=2.0,
                    status=random.choice(['На рассмотрении', 'Одобрена', 'Выплачена']),
                    approved_by_manager_id=managers[0].id if managers else None
                )
                db.session.add(application)
                applications_created += 1
    
    # Создаем уведомления
    notifications_created = 0
    for user in users:
        notification_texts = [
            'Добро пожаловать на платформу!',
            'Ваша заявка на кешбек рассмотрена',
            'Новые объекты по вашим критериям',
            'Изменение цен в избранных ЖК'
        ]
        
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
            {'rooms': ['1'], 'price_max': 5000000},
            {'rooms': ['2', '3'], 'district': 'Центральный'},
            {'price_min': 3000000, 'price_max': 8000000}
        ]
        
        for params in random.sample(search_params, 1):
            saved_search = SavedSearch(
                user_id=user.id,
                name=f"Поиск {random.randint(1, 100)}",
                filters=json.dumps(params),
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
            'content': 'Полное руководство по выбору квартиры в новостройке...',
            'excerpt': 'Основные критерии выбора квартиры в новостройке',
            'category': 'Советы покупателям',
            'status': 'published'
        },
        {
            'title': 'Ипотека в 2024 году: все что нужно знать',
            'content': 'Актуальная информация об ипотечных программах...',
            'excerpt': 'Обзор ипотечных программ и условий',
            'category': 'Ипотека',
            'status': 'published'
        },
        {
            'title': 'Инвестиции в недвижимость Краснодара',
            'content': 'Анализ рынка недвижимости для инвесторов...',
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

def create_collections(managers, users, properties):
    """Создание тестовых коллекций"""
    print("\n📚 Создаем коллекции недвижимости...")
    
    if not managers or not users or not properties:
        print("⚠️ Недостаточно данных для создания коллекций")
        return []
    
    collections_data = [
        {
            'title': 'Лучшие предложения для семьи',
            'description': 'Подборка 2-3 комнатных квартир в семейных районах',
            'tags': '["семейная", "детские сады", "школы"]'
        },
        {
            'title': 'Инвестиционный портфель',
            'description': 'Квартиры с высоким потенциалом роста стоимости',
            'tags': '["инвестиция", "рост стоимости", "центр"]'
        },
        {
            'title': 'Первое жилье',
            'description': 'Доступные варианты для молодых семей',
            'tags': '["молодая семья", "доступное жилье", "ипотека"]'
        }
    ]
    
    created_collections = []
    for i, collection_data in enumerate(collections_data):
        existing_collection = Collection.query.filter_by(title=collection_data['title']).first()
        if not existing_collection:
            collection = Collection(
                title=collection_data['title'],
                description=collection_data['description'],
                tags=collection_data['tags'],
                created_by_manager_id=managers[0].id,
                assigned_to_user_id=users[i % len(users)].id if i < len(users) else None,
                status='Отправлена',
                is_public=True,
                sent_at=datetime.utcnow() - timedelta(days=random.randint(1, 7))
            )
            db.session.add(collection)
            db.session.flush()  # Чтобы получить ID коллекции
            
            # Добавляем объекты в коллекцию
            collection_properties = random.sample(properties, min(5, len(properties)))
            for j, prop in enumerate(collection_properties):
                collection_property = CollectionProperty(
                    collection_id=collection.id,
                    property_id=prop.get('id', f'prop_{j}'),
                    property_name=f"{prop.get('rooms', 'N/A')}-комн квартира",
                    property_price=prop.get('price', 0),
                    complex_name=prop.get('complex', ''),
                    property_type=prop.get('rooms', ''),
                    property_size=prop.get('area', 0),
                    manager_note=f"Отличный вариант для {collection_data['title'].lower()}",
                    order_index=j
                )
                db.session.add(collection_property)
            
            created_collections.append(collection)
        else:
            created_collections.append(existing_collection)
    
    db.session.commit()
    print(f"✓ Создано/найдено {len(created_collections)} коллекций")
    return created_collections

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
        # Загружаем данные из JSON
        properties, complexes, developers_data = load_json_data()
        
        # Создаем базовые данные
        users = create_test_users()
        managers = create_test_managers()
        admins = create_test_admins()
        
        # Создаем справочники
        districts, developers = create_districts_and_developers(developers_data)
        residential_complexes = create_residential_complexes(complexes, developers, districts)
        search_categories = create_search_categories()
        recommendation_categories = create_recommendation_categories()
        
        # Создаем связанные данные
        assign_users_to_managers(users, managers)
        create_test_data(users, managers, properties)
        blog_posts = create_blog_posts(admins)
        collections = create_collections(managers, users, properties)
        
        print("\n✅ Заполнение базы данных завершено!")
        print("\n📊 Статистика:")
        print(f"   👥 Пользователи: {len(users)}")
        print(f"   🏢 Менеджеры: {len(managers)}")
        print(f"   🔑 Администраторы: {len(admins)}")
        print(f"   🏘️ Районы: {len(districts)}")
        print(f"   🏗️ Застройщики: {len(developers)}")
        print(f"   🏢 Жилые комплексы: {len(residential_complexes)}")
        print(f"   🔍 Категории поиска: {len(search_categories)}")
        print(f"   💡 Категории рекомендаций: {len(recommendation_categories)}")
        print(f"   📝 Статьи блога: {len(blog_posts)}")
        print(f"   📚 Коллекции: {len(collections)}")
        
        print(f"\n🔐 Тестовые аккаунты:")
        print(f"   📧 Пользователь: demo@inback.ru / demo123")
        print(f"   👥 Менеджер: manager@inback.ru / demo123")
        print(f"   🔑 Администратор: admin@inback.ru / admin123")

if __name__ == '__main__':
    main()