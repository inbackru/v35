#!/usr/bin/env python3
"""
Скрипт для получения Telegram chat_id пользователей
Запустите этот скрипт и попросите пользователя написать боту любое сообщение
"""

import os
import asyncio
from telegram import Bot

async def get_chat_ids():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("TELEGRAM_BOT_TOKEN не найден")
        return
    
    bot = Bot(token=token)
    
    try:
        me = await bot.get_me()
        print(f"✓ Подключен к боту: @{me.username}")
        print()
        
        # Получаем обновления
        updates = await bot.get_updates()
        
        if not updates:
            print("❌ Нет сообщений в истории бота")
            print()
            print("📱 Инструкция:")
            print("1. Найдите @inbackbot в Telegram")
            print("2. Отправьте любое сообщение (например: 'привет')")
            print("3. Запустите этот скрипт снова")
            return
        
        print(f"📨 Найдено {len(updates)} сообщений:")
        print()
        
        # Собираем уникальных пользователей
        users = {}
        for update in updates:
            if update.message and update.message.from_user:
                user = update.message.from_user
                chat_id = update.message.chat.id
                
                if chat_id not in users:
                    users[chat_id] = {
                        'chat_id': chat_id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name or '',
                        'last_message': update.message.text or '[Медиа]'
                    }
        
        # Выводим информацию о пользователях
        for chat_id, user_info in users.items():
            username = f"@{user_info['username']}" if user_info['username'] else "Нет username"
            full_name = f"{user_info['first_name']} {user_info['last_name']}".strip()
            
            print(f"👤 {full_name}")
            print(f"   Chat ID: {chat_id}")
            print(f"   Username: {username}")
            print(f"   Последнее сообщение: {user_info['last_message']}")
            print()
            
            # Если это @Ultimaten, покажем SQL команду для обновления
            if user_info['username'] == 'Ultimaten':
                print("🔧 SQL команда для обновления Станислава:")
                print(f"UPDATE users SET telegram_id = '{chat_id}' WHERE email = 'bithome@mail.ru';")
                print()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(get_chat_ids())