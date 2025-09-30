#!/usr/bin/env python3
"""
Диагностика проблем с Telegram Bot
"""

import os
import asyncio
import requests

def check_bot_token():
    """Проверка токена через HTTP API"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден")
        return False
    
    print(f"🔑 Токен: {token[:15]}...")
    
    # Проверка через HTTP API
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Бот активен: @{bot_info['username']}")
            print(f"   Имя: {bot_info['first_name']}")
            print(f"   ID: {bot_info['id']}")
            return True
        else:
            print(f"❌ Ошибка API: {data.get('description', 'Неизвестная ошибка')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Сетевая ошибка: {e}")
        return False

async def test_telegram_library():
    """Тест через python-telegram-bot"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    try:
        from telegram import Bot
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Библиотека работает: @{me.username}")
        return True
    except Exception as e:
        print(f"❌ Ошибка библиотеки: {e}")
        return False

def main():
    print("🔍 Диагностика Telegram Bot")
    print("=" * 40)
    
    # Проверка токена
    if check_bot_token():
        print("\n🔍 Тестирование библиотеки...")
        asyncio.run(test_telegram_library())
    
    print("\n📝 Рекомендации:")
    print("1. Если токен не работает - получите новый через @BotFather")
    print("2. Убедитесь что бот @inbackbot активен")
    print("3. Для получения chat_id - пользователь должен написать боту")

if __name__ == "__main__":
    main()