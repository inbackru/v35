#!/usr/bin/env python3
"""
Скрипт для проверки содержимого базы данных
"""
from app import app, db
from models import (
    User, Manager, Admin, BlogPost, Collection, CollectionProperty,
    CashbackApplication, FavoriteProperty, SavedSearch, UserNotification,
    District, Developer, ResidentialComplex, SearchCategory
)

def check_database():
    """Проверка содержимого базы данных"""
    print("📊 Проверяем состояние базы данных...\n")
    
    with app.app_context():
        # Подсчитываем количество записей в каждой таблице
        stats = {
            'Пользователи (Users)': User.query.count(),
            'Менеджеры (Managers)': Manager.query.count(), 
            'Администраторы (Admins)': Admin.query.count(),
            'Районы (Districts)': District.query.count(),
            'Застройщики (Developers)': Developer.query.count(),
            'ЖК (Residential Complexes)': ResidentialComplex.query.count(),
            'Категории поиска (Search Categories)': SearchCategory.query.count(),
            'Избранное (Favorite Properties)': FavoriteProperty.query.count(),
            'Заявки на кешбек (Cashback Applications)': CashbackApplication.query.count(),
            'Сохраненные поиски (Saved Searches)': SavedSearch.query.count(),
            'Уведомления (User Notifications)': UserNotification.query.count(),
            'Коллекции (Collections)': Collection.query.count(),
            'Статьи блога (Blog Posts)': BlogPost.query.count()
        }
        
        print("📈 Статистика по таблицам:")
        print("=" * 50)
        total_records = 0
        for table_name, count in stats.items():
            print(f"{table_name:<40} {count:>8} записей")
            total_records += count
        
        print("=" * 50)
        print(f"{'ВСЕГО ЗАПИСЕЙ':<40} {total_records:>8}")
        
        # Проверяем тестовые аккаунты
        print("\n🔐 Тестовые аккаунты:")
        print("=" * 50)
        
        demo_user = User.query.filter_by(email='demo@inback.ru').first()
        if demo_user:
            print(f"✅ Пользователь: demo@inback.ru (ID: {demo_user.id})")
        else:
            print("❌ Пользователь demo@inback.ru не найден")
        
        demo_manager = Manager.query.filter_by(email='manager@inback.ru').first()
        if demo_manager:
            print(f"✅ Менеджер: manager@inback.ru (ID: {demo_manager.id})")
        else:
            print("❌ Менеджер manager@inback.ru не найден")
        
        demo_admin = Admin.query.filter_by(email='admin@inback.ru').first()
        if demo_admin:
            print(f"✅ Администратор: admin@inback.ru (ID: {demo_admin.id})")
        else:
            print("❌ Администратор admin@inback.ru не найден")
        
        # Показываем примеры данных
        print("\n📝 Примеры данных:")
        print("=" * 50)
        
        # Показываем несколько пользователей
        users = User.query.limit(3).all()
        print(f"Пользователи ({len(users)} из {User.query.count()}):")
        for user in users:
            print(f"  - {user.full_name} ({user.email}) - {user.client_status}")
        
        # Показываем несколько районов
        districts = District.query.limit(5).all()
        print(f"\nРайоны ({len(districts)} из {District.query.count()}):")
        for district in districts:
            print(f"  - {district.name} (slug: {district.slug})")
        
        # Показываем застройщиков
        developers = Developer.query.limit(5).all()
        print(f"\nЗастройщики ({len(developers)} из {Developer.query.count()}):")
        for developer in developers:
            print(f"  - {developer.name} (slug: {developer.slug})")
        
        # Показываем ЖК
        complexes = ResidentialComplex.query.limit(5).all()
        print(f"\nЖилые комплексы ({len(complexes)} из {ResidentialComplex.query.count()}):")
        for complex_obj in complexes:
            district_name = complex_obj.district.name if complex_obj.district else "Не указан"
            developer_name = complex_obj.developer.name if complex_obj.developer else "Не указан"
            print(f"  - {complex_obj.name} ({district_name}, {developer_name})")
        
        print("\n✅ Проверка завершена!")

if __name__ == '__main__':
    check_database()