#!/usr/bin/env python3
"""
Простой тест Telegram уведомлений
"""

import asyncio
import os
from telegram import Bot

async def test_telegram_simple():
    """Простой тест отправки Telegram сообщения"""
    
    # Telegram Bot Token
    token = "7210651587:AAHp6T0JGwOAq6rjIqOkZ2p5MjOKZFHStYA"
    
    if not token:
        print("❌ Telegram Bot Token не найден")
        return
    
    bot = Bot(token=token)
    
    # Сообщение для тестирования
    message = """🏠 Тест уведомления InBack

Привет! Это тестовое уведомление от бота @inbackbot.

Если вы получили это сообщение, то система уведомлений работает корректно! 🎉

---
InBack.ru - ваш помощник в покупке недвижимости"""
    
    try:
        # Попробуем отправить сообщение по username
        username = '@Ultimaten'
        print(f"🚀 Отправляем тестовое сообщение пользователю {username}...")
        
        # Попробуем найти пользователя через chat_id или username
        # Для начала попробуем отправить прямо по username
        await bot.send_message(chat_id=username, text=message)
        
        print("✅ Сообщение отправлено успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
        
        # Попробуем получить информацию о боте
        try:
            bot_info = await bot.get_me()
            print(f"ℹ️ Информация о боте: @{bot_info.username}")
        except Exception as bot_error:
            print(f"❌ Ошибка получения информации о боте: {bot_error}")

if __name__ == "__main__":
    asyncio.run(test_telegram_simple())