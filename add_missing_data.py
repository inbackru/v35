#!/usr/bin/env python3
"""
Скрипт для добавления недостающих тестовых данных
"""
import json
import random
from datetime import datetime, timedelta
from app import app, db
from models import (
    User, Manager, Admin, BlogPost, Collection, CollectionProperty,
    CashbackApplication, FavoriteProperty, SavedSearch, UserNotification
)

def load_properties_data():
    """Загружаем данные о недвижимости из JSON"""
    try:
        with open('data/properties.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Файл properties.json не найден, создаем тестовые данные")
        return []

def create_favorite_properties(users, properties_data):
    """Создание избранных объектов"""
    print("❤️ Создаем избранные объекты...")
    
    created_count = 0
    for i, user in enumerate(users[:4]):  # Для первых 4 пользователей
        # Создаем 3-7 избранных объектов для каждого пользователя
        favorites_count = random.randint(3, 7)
        
        for j in range(favorites_count):
            property_id = f'fav_{user.id}_{j}'
            existing = FavoriteProperty.query.filter_by(user_id=user.id, property_id=property_id).first()
            
            if not existing:
                # Используем данные из JSON или создаем тестовые
                if properties_data and j < len(properties_data):
                    prop = properties_data[j]
                    property_name = f"{prop.get('rooms', '2')}-комн квартира"
                    property_size = prop.get('area', random.randint(40, 120))
                    property_price = prop.get('price', random.randint(4000000, 15000000))
                    complex_name = prop.get('complex', f'ЖК Тестовый-{j+1}')
                    developer_name = prop.get('developer', 'Тестовый застройщик')
                else:
                    # Тестовые данные
                    rooms = random.choice(['1', '2', '3', '4'])
                    property_name = f"{rooms}-комн квартира"
                    property_size = random.randint(35, 150)
                    property_price = random.randint(3500000, 18000000)
                    complex_name = f'ЖК {random.choice(["Солнечный", "Центральный", "Премьер", "Элитный", "Комфорт"])}-{j+1}'
                    developer_name = random.choice(['ГК "Инвестстройкуб"', 'ПИК', 'Самолет Девелопмент'])
                
                cashback_amount = int(property_price * random.uniform(0.015, 0.025))
                
                favorite = FavoriteProperty(
                    user_id=user.id,
                    property_id=property_id,
                    property_name=property_name,
                    property_type=rooms if 'rooms' in locals() else random.choice(['1', '2', '3']),
                    property_size=property_size,
                    property_price=property_price,
                    complex_name=complex_name,
                    developer_name=developer_name,
                    property_image=f'https://images.unsplash.com/photo-{random.randint(1500000000, 1700000000)}-apartment',
                    cashback_amount=cashback_amount,
                    cashback_percent=round(cashback_amount / property_price * 100, 2)
                )
                db.session.add(favorite)
                created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} избранных объектов")

def create_cashback_applications(users, managers):
    """Создание заявок на кешбек"""
    print("💰 Создаем заявки на кешбек...")
    
    created_count = 0
    statuses = ['На рассмотрении', 'Одобрена', 'Выплачена', 'Отклонена']
    
    for user in users[:5]:  # Для первых 5 пользователей
        applications_count = random.randint(1, 4)
        
        for i in range(applications_count):
            property_id = f'app_{user.id}_{i}'
            existing = CashbackApplication.query.filter_by(user_id=user.id, property_id=property_id).first()
            
            if not existing:
                rooms = random.choice(['1', '2', '3', '4'])
                property_size = random.randint(40, 120)
                property_price = random.randint(4000000, 16000000)
                cashback_amount = int(property_price * random.uniform(0.015, 0.03))
                status = random.choice(statuses)
                
                app_date = datetime.utcnow() - timedelta(days=random.randint(5, 90))
                approved_date = app_date + timedelta(days=random.randint(1, 14)) if status in ['Одобрена', 'Выплачена'] else None
                payout_date = approved_date + timedelta(days=random.randint(7, 30)) if status == 'Выплачена' else None
                
                application = CashbackApplication(
                    user_id=user.id,
                    property_id=property_id,
                    property_name=f"{rooms}-комн квартира",
                    property_type=rooms,
                    property_size=property_size,
                    property_price=property_price,
                    complex_name=f'ЖК {random.choice(["Премьер", "Элитный", "Солнечный", "Центральный"])}',
                    developer_name=random.choice(['ГК "Инвестстройкуб"', 'ПИК', 'Самолет Девелопмент']),
                    cashback_amount=cashback_amount,
                    cashback_percent=round(cashback_amount / property_price * 100, 2),
                    status=status,
                    application_date=app_date,
                    approved_date=approved_date,
                    payout_date=payout_date,
                    approved_by_manager_id=managers[0].id if managers and status in ['Одобрена', 'Выплачена'] else None,
                    notes=f'Заявка на получение кешбека за покупку {rooms}-комнатной квартиры',
                    manager_notes='Документы проверены, заявка обработана' if status == 'Одобрена' else None
                )
                db.session.add(application)
                created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} заявок на кешбек")

def create_saved_searches(users):
    """Создание сохраненных поисков"""
    print("🔍 Создаем сохраненные поиски...")
    
    created_count = 0
    search_templates = [
        {
            'name': '1-комнатные до 6 млн',
            'property_type': '1-комн',
            'price_max': 6000000
        },
        {
            'name': '2-3 комнатные в центре',
            'property_type': '2-комн',
            'location': 'Центральный'
        },
        {
            'name': 'Студии до 4 млн',
            'property_type': 'студия',
            'price_max': 4000000
        },
        {
            'name': 'Премиум квартиры',
            'price_min': 12000000,
            'description': 'Элитное жилье премиум-класса'
        },
        {
            'name': 'Семейные квартиры',
            'property_type': '3-комн',
            'size_min': 80.0
        }
    ]
    
    for user in users[:6]:  # Для первых 6 пользователей
        searches_count = random.randint(2, 4)
        user_searches = random.sample(search_templates, min(searches_count, len(search_templates)))
        
        for search_data in user_searches:
            existing = SavedSearch.query.filter_by(
                user_id=user.id, 
                name=search_data['name']
            ).first()
            
            if not existing:
                saved_search = SavedSearch(
                    user_id=user.id,
                    name=search_data['name'],
                    description=search_data.get('description'),
                    property_type=search_data.get('property_type'),
                    location=search_data.get('location'),
                    price_min=search_data.get('price_min'),
                    price_max=search_data.get('price_max'),
                    size_min=search_data.get('size_min'),
                    notify_new_matches=random.choice([True, True, True, False]),  # 75% с уведомлениями
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
                )
                db.session.add(saved_search)
                created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} сохраненных поисков")

def create_user_notifications(users):
    """Создание уведомлений пользователей"""
    print("📢 Создаем уведомления пользователей...")
    
    created_count = 0
    notification_templates = [
        {
            'title': 'Добро пожаловать!',
            'message': 'Добро пожаловать на платформу недвижимости! Здесь вы найдете лучшие предложения.',
            'type': 'welcome'
        },
        {
            'title': 'Заявка на кешбек рассмотрена',
            'message': 'Ваша заявка на получение кешбека была рассмотрена и одобрена.',
            'type': 'cashback'
        },
        {
            'title': 'Новые объекты по вашим критериям',
            'message': 'Появились новые квартиры, соответствующие вашим требованиям к поиску.',
            'type': 'search_match'
        },
        {
            'title': 'Изменение цен в избранных ЖК',
            'message': 'Цены в одном из ваших избранных жилых комплексов изменились.',
            'type': 'price_change'
        },
        {
            'title': 'Новая подборка от менеджера',
            'message': 'Ваш персональный менеджер подготовил для вас новую подборку квартир.',
            'type': 'collection'
        },
        {
            'title': 'Акция: скидка 3%',
            'message': 'Специальная акция от застройщика - дополнительная скидка 3% при покупке.',
            'type': 'promotion'
        }
    ]
    
    for user in users:
        notifications_count = random.randint(3, 8)
        user_notifications = random.sample(notification_templates, min(notifications_count, len(notification_templates)))
        
        for notif_data in user_notifications:
            notification = UserNotification(
                user_id=user.id,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['type'],
                is_read=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(notification)
            created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} уведомлений")

def create_blog_posts(admins):
    """Создание статей блога"""
    print("📝 Создаем статьи блога...")
    
    if not admins:
        print("⚠️ Нет администраторов для создания статей")
        return
    
    blog_posts_data = [
        {
            'title': 'Как выбрать квартиру в новостройке: полное руководство',
            'content': '''При выборе квартиры в новостройке важно учитывать множество факторов. 
            
Основные критерии:
1. Репутация застройщика - изучите его предыдущие проекты
2. Документы на строительство - все должно быть в порядке
3. Расположение - транспортная доступность и инфраструктура
4. Планировка и качество отделки
5. Сроки сдачи и возможные риски

Финансовые аспекты:
- Сравните цены с аналогичными объектами
- Узнайте о возможностях рассрочки и ипотеки
- Рассчитайте дополнительные расходы

Правовые моменты:
- Проверьте все документы на землю и строительство
- Изучите договор долевого участия
- Узнайте о страховании''',
            'excerpt': 'Подробное руководство по выбору квартиры в новостройке с учетом всех важных факторов',
            'category': 'Советы покупателям',
            'status': 'published',
            'tags': '["новостройка", "покупка", "советы"]'
        },
        {
            'title': 'Ипотечные программы 2024: льготы и условия',
            'content': '''Обзор актуальных ипотечных программ 2024 года.

Семейная ипотека:
- Ставка от 5.5% годовых
- Для семей с детьми
- Первоначальный взнос от 20%

IT-ипотека:
- Ставка от 5.0% годовых  
- Для IT-специалистов
- Первоначальный взнос от 15%

Военная ипотека:
- Льготные условия для военнослужащих
- Государственная поддержка
- Особые требования к объектам

Материнский капитал:
- Можно использовать как первоначальный взнос
- Дополнительные льготы
- Упрощенная процедура оформления''',
            'excerpt': 'Подробный обзор ипотечных программ и льгот, доступных в 2024 году',
            'category': 'Ипотека',
            'status': 'published',
            'tags': '["ипотека", "льготы", "2024"]'
        },
        {
            'title': 'Инвестиции в недвижимость Краснодара: аналитика рынка',
            'content': '''Краснодар остается одним из наиболее привлекательных городов для инвестиций в недвижимость.

Ключевые факторы роста:
- Активное развитие инфраструктуры
- Приток населения из других регионов
- Развитие IT-сектора
- Близость к морю и туристическим зонам

Перспективные районы:
1. Центральный - стабильный рост стоимости
2. Карасунский - новые жилые комплексы
3. Прикубанский - развитая инфраструктура

Рекомендации инвесторам:
- Выбирайте объекты в перспективных локациях
- Учитывайте транспортную доступность
- Обращайте внимание на качество застройщика
- Рассматривайте возможности сдачи в аренду''',
            'excerpt': 'Анализ инвестиционной привлекательности недвижимости Краснодара',
            'category': 'Инвестиции',
            'status': 'published',
            'tags': '["инвестиции", "Краснодар", "аналитика"]'
        },
        {
            'title': 'Кешбек при покупке недвижимости: как получить максимум',
            'content': '''Кешбек при покупке недвижимости - отличная возможность сэкономить.

Виды кешбека:
- От застройщика (обычно 1-3% от стоимости)
- От банка при оформлении ипотеки
- От агентства недвижимости
- Специальные акции и программы лояльности

Как увеличить кешбек:
1. Участвуйте в акциях застройщика
2. Выбирайте правильное время покупки
3. Используйте партнерские программы
4. Оформляйте ипотеку в банках-партнерах

Условия получения:
- Соблюдение сроков сделки
- Предоставление всех документов
- Выполнение условий программы

Налоговые аспекты:
- Кешбек может облагаться налогом
- Ведите учет всех выплат
- Консультируйтесь с налоговыми консультантами''',
            'excerpt': 'Как максимально использовать программы кешбека при покупке недвижимости',
            'category': 'Кешбек',
            'status': 'published',
            'tags': '["кешбек", "экономия", "покупка"]'
        },
        {
            'title': 'Тенденции рынка недвижимости в 2024 году',
            'content': '''Рынок недвижимости в 2024 году показывает интересные тенденции.

Основные тренды:
- Рост спроса на комфорт-класс
- Увеличение популярности готового жилья
- Развитие пригородной недвижимости
- Внедрение smart-технологий в ЖК

Региональные особенности:
- Краснодар: стабильный рост цен
- Сочи: высокий инвестиционный потенциал
- Анапа: развитие курортной недвижимости

Прогнозы на год:
- Умеренный рост цен (5-10%)
- Развитие ипотечного кредитования
- Увеличение объемов строительства
- Новые технологии в отрасли

Рекомендации покупателям:
- Не откладывайте покупку надолго
- Изучайте новые проекты
- Следите за изменениями в законодательстве''',
            'excerpt': 'Обзор ключевых тенденций и прогнозов развития рынка недвижимости',
            'category': 'Аналитика',
            'status': 'published',
            'tags': '["тенденции", "прогноз", "рынок"]'
        }
    ]
    
    created_count = 0
    for post_data in blog_posts_data:
        existing = BlogPost.query.filter_by(title=post_data['title']).first()
        if not existing:
            post = BlogPost(
                title=post_data['title'],
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                category=post_data['category'],
                status=post_data['status'],
                tags=post_data.get('tags'),
                author_id=admins[0].id,
                published_at=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                views_count=random.randint(50, 500),
                likes_count=random.randint(5, 50)
            )
            db.session.add(post)
            created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} статей блога")

def create_collections(managers, users):
    """Создание коллекций недвижимости"""
    print("📚 Создаем коллекции недвижимости...")
    
    if not managers or not users:
        print("⚠️ Нет менеджеров или пользователей для создания коллекций")
        return
    
    collections_data = [
        {
            'title': 'Лучшие предложения для молодой семьи',
            'description': 'Подборка 2-3 комнатных квартир в семейных районах с развитой инфраструктурой',
            'tags': '["молодая семья", "2-3 комнаты", "инфраструктура"]'
        },
        {
            'title': 'Инвестиционный портфель: стабильный доход',
            'description': 'Квартиры с высоким потенциалом роста стоимости и возможностью сдачи в аренду',
            'tags': '["инвестиции", "аренда", "рост стоимости"]'
        },
        {
            'title': 'Первое жилье: доступные варианты',
            'description': 'Бюджетные варианты для покупки первой квартиры с возможностью ипотеки',
            'tags': '["первое жилье", "бюджет", "ипотека"]'
        },
        {
            'title': 'Премиум класс: эксклюзивные предложения',
            'description': 'Элитные квартиры в престижных районах с уникальными характеристиками',
            'tags': '["премиум", "элитное жилье", "эксклюзив"]'
        },
        {
            'title': 'Студии и 1-комнатные: компактный комфорт',
            'description': 'Небольшие, но функциональные квартиры для одного человека или пары',
            'tags': '["студия", "1-комнатная", "компакт"]'
        }
    ]
    
    created_count = 0
    for i, collection_data in enumerate(collections_data):
        existing = Collection.query.filter_by(title=collection_data['title']).first()
        if not existing:
            assigned_user = users[i % len(users)] if users else None
            
            collection = Collection(
                title=collection_data['title'],
                description=collection_data['description'],
                tags=collection_data['tags'],
                created_by_manager_id=managers[0].id,
                assigned_to_user_id=assigned_user.id if assigned_user else None,
                status=random.choice(['Отправлена', 'Просмотрена', 'Черновик']),
                is_public=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                sent_at=datetime.utcnow() - timedelta(days=random.randint(1, 15)) if random.choice([True, False]) else None
            )
            db.session.add(collection)
            db.session.flush()  # Чтобы получить ID
            
            # Добавляем свойства в коллекцию
            properties_count = random.randint(3, 8)
            for j in range(properties_count):
                rooms = random.choice(['1', '2', '3', '4'])
                property_price = random.randint(4000000, 18000000)
                
                collection_property = CollectionProperty(
                    collection_id=collection.id,
                    property_id=f'coll_{collection.id}_{j}',
                    property_name=f"{rooms}-комн квартира",
                    property_price=property_price,
                    complex_name=f'ЖК {random.choice(["Солнечный", "Премьер", "Центральный"])}',
                    property_type=rooms,
                    property_size=random.randint(35, 150),
                    manager_note=f'Отличный вариант для {collection_data["title"].lower()}. Рекомендую к рассмотрению.',
                    order_index=j
                )
                db.session.add(collection_property)
            
            created_count += 1
    
    db.session.commit()
    print(f"✓ Создано {created_count} коллекций")

def main():
    """Основная функция"""
    print("🚀 Добавляем недостающие тестовые данные...\n")
    
    with app.app_context():
        # Получаем существующие данные
        users = User.query.all()
        managers = Manager.query.all()
        admins = Admin.query.all()
        
        print(f"Найдено: {len(users)} пользователей, {len(managers)} менеджеров, {len(admins)} администраторов")
        
        # Загружаем данные о недвижимости
        properties_data = load_properties_data()
        
        # Создаем недостающие данные
        create_favorite_properties(users, properties_data)
        create_cashback_applications(users, managers)
        create_saved_searches(users)
        create_user_notifications(users)
        create_blog_posts(admins)
        create_collections(managers, users)
        
        print("\n✅ Добавление данных завершено!")
        print("\n🔍 Для проверки запустите: python check_database.py")

if __name__ == '__main__':
    main()