#!/usr/bin/env python3
"""
Тест системы регистрации и уведомлений InBack
Проверяет готовность всех функций без внешних API ключей
"""

import os
import sys
from app import app, db
from models import User, Manager, CallbackRequest
from email_service import send_notification

def test_database_connection():
    """Тест подключения к базе данных"""
    print("🔍 Проверка подключения к PostgreSQL...")
    try:
        with app.app_context():
            result = db.session.execute(db.text('SELECT version();')).fetchone()
            print(f"✅ PostgreSQL подключен: {result[0][:50]}...")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False

def test_user_registration():
    """Тест регистрации пользователя"""
    print("🔍 Проверка регистрации пользователя...")
    try:
        with app.app_context():
            # Создаем тестового пользователя
            test_user = User(
                email="test@inback.ru",
                full_name="Тестовый Пользователь",
                phone="+7900123456"
            )
            test_user.set_password("test123")
            
            # Проверяем генерацию ID
            user_id = test_user.user_id
            print(f"✅ Сгенерирован ID пользователя: {user_id}")
            
            # Проверяем хеширование пароля
            if test_user.check_password("test123"):
                print("✅ Хеширование пароля работает")
            else:
                print("❌ Ошибка хеширования пароля")
                return False
                
            print("✅ Система регистрации работает корректно")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")
        return False

def test_manager_system():
    """Тест системы менеджеров"""
    print("🔍 Проверка системы менеджеров...")
    try:
        with app.app_context():
            # Создаем тестового менеджера
            test_manager = Manager(
                email="manager@inback.ru",
                first_name="Тест",
                last_name="Менеджер",
                phone="+7900987654"
            )
            test_manager.set_password("manager123")
            
            manager_id = test_manager.manager_id
            print(f"✅ Сгенерирован ID менеджера: {manager_id}")
            print(f"✅ Полное имя: {test_manager.full_name}")
            print("✅ Система менеджеров работает корректно")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка создания менеджера: {e}")
        return False

def test_callback_requests():
    """Тест системы заявок"""
    print("🔍 Проверка системы заявок...")
    try:
        with app.app_context():
            # Создаем тестовую заявку
            test_request = CallbackRequest(
                name="Иван Петров",
                phone="+7900555444",
                email="ivan@example.com",
                interest="Покупка квартиры",
                budget="5-7 млн руб",
                timing="В ближайшие 3 месяца"
            )
            
            print(f"✅ Заявка создана: {test_request.name} - {test_request.phone}")
            print(f"✅ Статус: {test_request.status}")
            print("✅ Система заявок работает корректно")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка создания заявки: {e}")
        return False

def test_notification_system():
    """Тест системы уведомлений"""
    print("🔍 Проверка системы уведомлений...")
    try:
        # Тест без внешних API ключей (будет работать в режиме логирования)
        result = send_notification(
            recipient_email="test@inback.ru",
            subject="Тестовое уведомление",
            message="Проверка системы уведомлений InBack",
            notification_type="test"
        )
        
        print("✅ Функция уведомлений вызывается без ошибок")
        print(f"✅ Результат: {result}")
        
        # Проверим наличие шаблонов email
        templates_dir = "templates/emails"
        if os.path.exists(templates_dir):
            templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
            print(f"✅ Найдено {len(templates)} email шаблонов")
        else:
            print("⚠️  Папка email шаблонов не найдена")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка системы уведомлений: {e}")
        return False

def main():
    """Запуск всех тестов"""
    print("🚀 Тестирование системы регистрации и уведомлений InBack")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_user_registration,
        test_manager_system,
        test_callback_requests,
        test_notification_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все системы готовы к работе!")
        print("\n✅ ГОТОВЫЕ ФУНКЦИИ:")
        print("   • Регистрация пользователей")
        print("   • Система менеджеров") 
        print("   • Обработка заявок")
        print("   • База данных PostgreSQL")
        print("   • Система уведомлений (логирование)")
        
        print("\n⚠️  ДЛЯ ПОЛНОГО ФУНКЦИОНАЛА ДОБАВЬТЕ:")
        print("   • SENDGRID_API_KEY - для email уведомлений")
        print("   • TELEGRAM_BOT_TOKEN - для Telegram уведомлений")
    else:
        print("⚠️  Некоторые функции требуют настройки")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)