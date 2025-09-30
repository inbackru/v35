#!/usr/bin/env python3
"""
Скрипт для тестирования системы многоканальных уведомлений InBack
Демонстрирует работу Email, Telegram и WhatsApp уведомлений
"""

from app import app, db
from models import User, Manager
from email_service import send_notification, send_recommendation_email, send_saved_search_results_email
from whatsapp_integration import send_whatsapp_notification
import json

def test_email_notifications():
    """Тестирование email уведомлений"""
    print("=== ТЕСТИРОВАНИЕ EMAIL УВЕДОМЛЕНИЙ ===")
    
    with app.app_context():
        # Найти тестового пользователя
        user = User.query.filter_by(email='admin@inback.ru').first()
        if not user:
            print("❌ Тестовый пользователь не найден")
            return
        
        print(f"✓ Тестируем для пользователя: {user.full_name} ({user.email})")
        
        # 1. Тест приветственного письма
        print("\n1. Приветственное письмо...")
        try:
            from email_service import send_welcome_email
            result = send_welcome_email(user, base_url='https://inback.ru')
            print(f"   {'✓' if result else '❌'} Приветственное письмо")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        # 2. Тест рекомендации
        print("\n2. Рекомендация от менеджера...")
        try:
            recommendation_data = {
                'title': 'Отличная квартира в новом ЖК',
                'item_name': 'ЖК "Солнечный"',
                'description': 'Прекрасная 2-комнатная квартира с видом на парк. Отделка от застройщика, развитая инфраструктура.',
                'manager_name': 'Демо Менеджер',
                'priority_text': 'Высокий приоритет'
            }
            result = send_recommendation_email(user, recommendation_data)
            print(f"   {'✓' if result else '❌'} Рекомендация отправлена")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
        
        # 3. Тест результатов поиска
        print("\n3. Результаты сохраненного поиска...")
        try:
            search_data = {
                'search_name': 'Квартиры до 5 млн в центре',
                'properties_list': [
                    {'name': 'ЖК "Центральный"', 'price': '4 500 000 ₽'},
                    {'name': 'ЖК "Городской"', 'price': '4 800 000 ₽'}
                ],
                'properties_count': 2,
                'search_url': 'https://inback.ru/properties?price_max=5000000'
            }
            result = send_saved_search_results_email(user, search_data)
            print(f"   {'✓' if result else '❌'} Результаты поиска отправлены")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def test_telegram_notifications():
    """Тестирование Telegram уведомлений"""
    print("\n=== ТЕСТИРОВАНИЕ TELEGRAM УВЕДОМЛЕНИЙ ===")
    
    with app.app_context():
        # Найти пользователя с Telegram ID
        user = User.query.filter(User.telegram_id.isnot(None)).first()
        if not user:
            print("❌ Пользователи с Telegram ID не найдены")
            print("   Для тестирования нужно связать аккаунт с Telegram ботом")
            return
        
        print(f"✓ Тестируем для пользователя: {user.full_name} (Telegram: {user.telegram_id})")
        
        try:
            from email_service import send_telegram_notification
            
            # Тест приветственного сообщения
            result = send_telegram_notification(user, 'welcome', base_url='https://inback.ru')
            print(f"   {'✓' if result else '❌'} Telegram приветствие")
            
            # Тест рекомендации
            recommendation_data = {
                'title': 'Новая рекомендация',
                'item_name': 'ЖК "Telegram Test"',
                'manager_name': 'Демо Менеджер'
            }
            result = send_telegram_notification(user, 'recommendation', **recommendation_data)
            print(f"   {'✓' if result else '❌'} Telegram рекомендация")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def test_whatsapp_notifications():
    """Тестирование WhatsApp уведомлений"""
    print("\n=== ТЕСТИРОВАНИЕ WHATSAPP УВЕДОМЛЕНИЙ ===")
    
    with app.app_context():
        # Найти пользователя с номером телефона
        user = User.query.filter(User.phone.isnot(None)).first()
        if not user:
            print("❌ Пользователи с номерами телефонов не найдены")
            return
        
        print(f"✓ Тестируем для пользователя: {user.full_name} (Телефон: {user.phone})")
        
        try:
            # Тест приветственного сообщения
            message = f"""
🏠 *Добро пожаловать в InBack!*

Привет, {user.full_name.split()[0] if user.full_name else 'Клиент'}!

Теперь вы можете получать уведомления о новых объектах прямо в WhatsApp.

💰 Отслеживайте кэшбек
🏘️ Получайте новые предложения  
📞 Связывайтесь с менеджером

*InBack.ru - ваш кэшбек-сервис*
            """
            
            result = send_whatsapp_notification(user.phone, message)
            print(f"   {'✓' if result else '❌'} WhatsApp приветствие")
            
            # Тест рекомендации
            recommendation_message = f"""
🏠 *Новая рекомендация от менеджера*

{user.full_name.split()[0] if user.full_name else 'Клиент'}, ваш менеджер рекомендует:

📋 *Отличная квартира в центре*
🏢 ЖК "WhatsApp Test"
💰 Кэшбек до 200 000 ₽

Свяжитесь с менеджером для подробностей!

*InBack.ru*
            """
            
            result = send_whatsapp_notification(user.phone, recommendation_message)
            print(f"   {'✓' if result else '❌'} WhatsApp рекомендация")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def test_unified_notifications():
    """Тестирование единой системы уведомлений"""
    print("\n=== ТЕСТИРОВАНИЕ ЕДИНОЙ СИСТЕМЫ УВЕДОМЛЕНИЙ ===")
    
    with app.app_context():
        user = User.query.filter_by(email='admin@inback.ru').first()
        if not user:
            print("❌ Тестовый пользователь не найден")
            return
        
        print(f"✓ Тестируем единую систему для: {user.full_name}")
        
        try:
            # Тест универсального уведомления
            result = send_notification(
                recipient_email=user.email,
                subject="Тест единой системы уведомлений",
                message="Это тестовое уведомление для проверки работы системы",
                notification_type='general',
                user_id=user.id,
                base_url='https://inback.ru'
            )
            print(f"   {'✓' if result else '❌'} Универсальное уведомление")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

def show_notification_settings():
    """Показать настройки уведомлений пользователей"""
    print("\n=== НАСТРОЙКИ УВЕДОМЛЕНИЙ ПОЛЬЗОВАТЕЛЕЙ ===")
    
    with app.app_context():
        users = User.query.limit(5).all()
        
        for user in users:
            print(f"\n👤 {user.full_name} ({user.email})")
            print(f"   📧 Email: {'✓' if getattr(user, 'email_notifications', True) else '❌'}")
            print(f"   📱 Telegram: {'✓' if user.telegram_id else '❌'} ({user.telegram_id or 'не привязан'})")
            print(f"   📞 WhatsApp: {'✓' if user.phone else '❌'} ({user.phone or 'не указан'})")
            print(f"   🔔 Предпочтения:")
            print(f"      - Рекомендации: {'✓' if getattr(user, 'notify_recommendations', True) else '❌'}")
            print(f"      - Поиск: {'✓' if getattr(user, 'notify_saved_searches', True) else '❌'}")
            print(f"      - Заявки: {'✓' if getattr(user, 'notify_applications', True) else '❌'}")
            print(f"      - Кэшбек: {'✓' if getattr(user, 'notify_cashback', True) else '❌'}")

if __name__ == '__main__':
    print("🔔 ТЕСТИРОВАНИЕ СИСТЕМЫ УВЕДОМЛЕНИЙ INBACK")
    print("=" * 50)
    
    # Показать текущие настройки
    show_notification_settings()
    
    # Тестировать все типы уведомлений
    test_email_notifications()
    test_telegram_notifications()
    test_whatsapp_notifications()
    test_unified_notifications()
    
    print("\n" + "=" * 50)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("\nДля полного тестирования:")
    print("1. Настройте EMAIL_PASSWORD в переменных окружения для реальной отправки писем")
    print("2. Настройте TELEGRAM_BOT_TOKEN для Telegram уведомлений")
    print("3. Настройте WHATSAPP_TOKEN для WhatsApp уведомлений")
    print("4. Привяжите аккаунты пользователей к Telegram боту")
    print("5. Убедитесь что у пользователей указаны номера телефонов")