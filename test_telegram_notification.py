#!/usr/bin/env python3
"""
Тестирование Telegram уведомлений
"""

import asyncio
from email_service import send_notification

async def test_telegram_notification():
    """Тест отправки уведомления через Telegram"""
    
    # Тестовые данные для клиента Станислава
    test_data = {
        'title': 'Тестовая рекомендация недвижимости',
        'item_name': 'ЖК "Тестовый комплекс"',
        'description': 'Отличная квартира в новом жилом комплексе с развитой инфраструктурой',
        'manager_name': 'Демо Менеджер',
        'priority_text': 'Высокий'
    }
    
    print("🚀 Тестируем отправку Telegram уведомления...")
    
    # Отправляем уведомление
    result = send_notification(
        recipient_email='bithome@mail.ru',
        subject='Тестовое уведомление',
        message='Тест системы уведомлений InBack',
        notification_type='recommendation',
        user_id=14,  # ID клиента Станислава
        **test_data
    )
    
    print(f"📊 Результат отправки: {result}")
    
    if result.get('telegram'):
        print("✅ Telegram уведомление отправлено успешно!")
    else:
        print("❌ Не удалось отправить Telegram уведомление")
    
    if result.get('email'):
        print("✅ Email уведомление отправлено успешно!")
    else:
        print("❌ Не удалось отправить Email уведомление")

if __name__ == "__main__":
    asyncio.run(test_telegram_notification())