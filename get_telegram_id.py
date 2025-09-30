#!/usr/bin/env python3
"""
Простой способ получить ваш Telegram ID
"""

import asyncio
from telegram import Bot

async def test_telegram_bot():
    """Тест Telegram бота и получение информации"""
    
    bot_token = '7210651587:AAEx05tkpKveOIqPpDtwXOY8UGkhwYeCxmE'
    bot = Bot(token=bot_token)
    
    try:
        # Получаем информацию о боте
        me = await bot.get_me()
        print(f"🤖 Bot активен: @{me.username} ({me.first_name})")
        print(f"Bot ID: {me.id}")
        
        # Отправляем тестовое сообщение на ваш ID (если известен)
        # Замените на ваш реальный Telegram ID
        test_chat_id = 123456789  # Заменить на реальный ID
        
        test_message = """
🔥 <b>Тест уведомлений InBack</b>

Станислав, это тестовое уведомление от системы InBack!

📋 <b>Рекомендую: Объект 2</b>
🏢 ЖК «Аврора»

Отличная студия в центре города с развитой инфраструктурой.

💡 <i>Приоритет:</i> Высокий

<a href="https://inback.ru/properties">Посмотреть объект</a>
        """
        
        result = await bot.send_message(
            chat_id=test_chat_id,
            text=test_message.strip(),
            parse_mode='HTML'
        )
        
        print(f"✅ Сообщение отправлено! Message ID: {result.message_id}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        
        if "chat not found" in str(e).lower():
            print("\n📋 Для получения уведомлений:")
            print("1. Напишите боту @YourBotUsername (замените на имя бота)")
            print("2. Отправьте команду /start")
            print("3. Ваш Telegram ID появится в логах бота")

if __name__ == "__main__":
    asyncio.run(test_telegram_bot())