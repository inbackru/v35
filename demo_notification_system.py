#!/usr/bin/env python3
"""
Демонстрация системы уведомлений InBack через веб-интерфейс
Создает тестовых пользователей и показывает возможности системы
"""

from app import app, db
from models import User, Manager, SavedSearch, Recommendation
from email_service import send_recommendation_email, send_saved_search_results_email
from werkzeug.security import generate_password_hash
import json
from datetime import datetime

def create_demo_users():
    """Создать демонстрационных пользователей с разными настройками"""
    with app.app_context():
        print("Создание демонстрационных пользователей...")
        
        # Пользователь с полными настройками уведомлений
        demo_user = User.query.filter_by(email='demo@inback.ru').first()
        if not demo_user:
            demo_user = User(
                email='demo@inback.ru',
                full_name='Демо Пользователь',
                password_hash=generate_password_hash('demo123'),
                phone='+7-918-123-45-67',
                telegram_id='123456789',  # Для демонстрации
                role='buyer',
                email_notifications=True,
                telegram_notifications=True,
                notify_recommendations=True,
                notify_saved_searches=True,
                notify_applications=True,
                notify_cashback=True,
                notify_marketing=False
            )
            db.session.add(demo_user)
            print("✓ Создан демо пользователь с полными настройками")
        
        # Пользователь только с email
        email_user = User.query.filter_by(email='email_only@inback.ru').first()
        if not email_user:
            email_user = User(
                email='email_only@inback.ru',
                full_name='Email Пользователь',
                password_hash=generate_password_hash('email123'),
                role='buyer',
                email_notifications=True,
                telegram_notifications=False,
                notify_recommendations=True,
                notify_saved_searches=False,
                notify_applications=True,
                notify_cashback=True,
                notify_marketing=False
            )
            db.session.add(email_user)
            print("✓ Создан пользователь только с email")
        
        # Пользователь с WhatsApp
        whatsapp_user = User.query.filter_by(email='whatsapp@inback.ru').first()
        if not whatsapp_user:
            whatsapp_user = User(
                email='whatsapp@inback.ru',
                full_name='WhatsApp Пользователь',
                password_hash=generate_password_hash('whatsapp123'),
                phone='+7-918-999-88-77',
                role='buyer',
                email_notifications=False,
                telegram_notifications=False,
                notify_recommendations=True,
                notify_saved_searches=True,
                notify_applications=False,
                notify_cashback=True,
                notify_marketing=True
            )
            db.session.add(whatsapp_user)
            print("✓ Создан пользователь с WhatsApp")
        
        db.session.commit()

def demo_manager_recommendations():
    """Демонстрация отправки рекомендаций через менеджерскую панель"""
    print("\n=== ДЕМОНСТРАЦИЯ РЕКОМЕНДАЦИЙ ОТ МЕНЕДЖЕРА ===")
    
    with app.app_context():
        manager = Manager.query.first()
        users = User.query.filter_by(role='buyer').limit(3).all()
        
        for user in users:
            print(f"\nОтправка рекомендации для: {user.full_name}")
            
            # Создание рекомендации в базе
            recommendation = Recommendation(
                user_id=user.id,
                title=f'Рекомендация для {user.full_name.split()[0]}',
                item_type='property',
                item_name='ЖК "Демонстрационный"',
                description='Отличная квартира с кэшбеком до 300 000 рублей',
                priority='high',
                manager_id=manager.id if manager else None,
                category='urgent'
            )
            db.session.add(recommendation)
            
            # Подготовка данных для email
            recommendation_data = {
                'title': recommendation.title,
                'item_name': recommendation.item_name,
                'description': recommendation.description,
                'manager_name': manager.full_name if manager else 'Менеджер InBack',
                'priority_text': 'Высокий приоритет' if recommendation.priority == 'high' else 'Обычный',
                'cashback_amount': '300 000 ₽',
                'property_url': 'https://inback.ru/properties/demo'
            }
            
            # Отправка email уведомления
            if user.email_notifications and user.notify_recommendations:
                result = send_recommendation_email(user, recommendation_data)
                print(f"   📧 Email: {'✓' if result else '❌'}")
            else:
                print(f"   📧 Email: ⏭️ (отключен пользователем)")
        
        db.session.commit()

def demo_saved_search_notifications():
    """Демонстрация уведомлений о результатах сохраненного поиска"""
    print("\n=== ДЕМОНСТРАЦИЯ УВЕДОМЛЕНИЙ О ПОИСКЕ ===")
    
    with app.app_context():
        users = User.query.filter_by(role='buyer').limit(2).all()
        
        for user in users:
            print(f"\nСоздание уведомления о поиске для: {user.full_name}")
            
            # Создание сохраненного поиска
            saved_search = SavedSearch(
                user_id=user.id,
                name=f'Поиск {user.full_name.split()[0]}',
                search_params=json.dumps({
                    'price_min': 3000000,
                    'price_max': 6000000,
                    'room_count': 2,
                    'district': 'Центральный'
                })
            )
            db.session.add(saved_search)
            
            # Подготовка данных о найденных объектах
            search_data = {
                'search_name': saved_search.name,
                'properties_list': [
                    {'name': 'ЖК "Центральный Парк"', 'price': '4 200 000 ₽', 'cashback': '210 000 ₽'},
                    {'name': 'ЖК "Солнечный Город"', 'price': '5 800 000 ₽', 'cashback': '290 000 ₽'},
                    {'name': 'ЖК "Зеленая Роща"', 'price': '3 900 000 ₽', 'cashback': '195 000 ₽'}
                ],
                'properties_count': 3,
                'search_url': 'https://inback.ru/properties?search_id=' + str(saved_search.id if hasattr(saved_search, 'id') else 'demo')
            }
            
            # Отправка уведомления
            if user.email_notifications and user.notify_saved_searches:
                result = send_saved_search_results_email(user, search_data)
                print(f"   📧 Результаты поиска: {'✓' if result else '❌'}")
            else:
                print(f"   📧 Результаты поиска: ⏭️ (отключен пользователем)")
        
        db.session.commit()

def show_web_interface_guide():
    """Показать инструкцию по тестированию через веб-интерфейс"""
    print("\n=== ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ ЧЕРЕЗ ВЕБ-ИНТЕРФЕЙС ===")
    print("""
🌐 ТЕСТИРОВАНИЕ ЧЕРЕЗ БРАУЗЕР:

1. МЕНЕДЖЕРСКАЯ ПАНЕЛЬ:
   - Перейти: /manager/login
   - Логин: manager@inback.ru  
   - Пароль: manager123
   - Использовать функции отправки рекомендаций

2. ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС:
   - Регистрация: /register
   - Настройки уведомлений: /profile
   - Управление подписками

3. НАСТРОЙКИ УВЕДОМЛЕНИЙ:
   - Email уведомления (включить/отключить)
   - Типы уведомлений (рекомендации, поиск, кэшбек)
   - Telegram интеграция
   - WhatsApp настройки

4. ОТПРАВКА РЕКОМЕНДАЦИЙ:
   - Создание персональных рекомендаций
   - Массовая рассылка
   - Категоризация клиентов
   
🔑 API ENDPOINTS ДЛЯ ТЕСТИРОВАНИЯ:
   - POST /api/send-recommendation
   - POST /api/send-search-results  
   - GET /api/notification-settings
   - PUT /api/notification-settings
""")

def show_configuration_guide():
    """Показать настройки для продакшена"""
    print("\n=== НАСТРОЙКИ ДЛЯ ПРОДАКШЕНА ===")
    print("""
🔧 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ:

1. EMAIL НАСТРОЙКИ:
   EMAIL_PASSWORD=your_email_password
   EMAIL_HOST=smtp.your-hosting.com
   EMAIL_PORT=587

2. TELEGRAM BOT:
   TELEGRAM_BOT_TOKEN=your_bot_token
   # Получить у @BotFather в Telegram

3. WHATSAPP BUSINESS API:
   WHATSAPP_TOKEN=your_whatsapp_token
   WHATSAPP_PHONE_ID=your_phone_number_id
   # Настроить в Facebook Business

4. ОСНОВНЫЕ:
   DATABASE_URL=already_configured
   SESSION_SECRET=already_configured
   
💡 РЕКОМЕНДАЦИИ:
   - Используйте реальные API ключи для тестирования
   - Настройте webhooks для Telegram бота
   - Проверьте лимиты WhatsApp API
   - Настройте мониторинг доставки писем
""")

if __name__ == '__main__':
    print("🔔 ДЕМОНСТРАЦИЯ СИСТЕМЫ УВЕДОМЛЕНИЙ INBACK")
    print("=" * 60)
    
    # Создать демо пользователей
    create_demo_users()
    
    # Демонстрация функций
    demo_manager_recommendations()
    demo_saved_search_notifications()
    
    # Инструкции
    show_web_interface_guide()
    show_configuration_guide()
    
    print("\n" + "=" * 60)
    print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("\nТеперь вы можете:")
    print("• Войти в менеджерскую панель и отправить реальные рекомендации")
    print("• Настроить API ключи для полнофункционального тестирования")
    print("• Протестировать все каналы уведомлений с реальными пользователями")