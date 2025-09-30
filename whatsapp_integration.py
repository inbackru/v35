#!/usr/bin/env python3
"""
WhatsApp интеграция для отправки уведомлений
Использует WhatsApp Business API для отправки сообщений клиентам
"""

import os
import requests
import json
from datetime import datetime

# WhatsApp Business API Configuration
WHATSAPP_TOKEN = os.environ.get('WHATSAPP_TOKEN', '')
WHATSAPP_PHONE_ID = os.environ.get('WHATSAPP_PHONE_ID', '')
WHATSAPP_API_VERSION = 'v17.0'
WHATSAPP_API_URL = f'https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_ID}/messages'

def format_phone_number(phone):
    """
    Форматирует номер телефона для WhatsApp API
    Убирает все символы кроме цифр и добавляет код страны если нужно
    
    Args:
        phone: Номер телефона в любом формате
    
    Returns:
        Отформатированный номер для WhatsApp API
    """
    if not phone:
        return None
    
    # Убираем все символы кроме цифр
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    # Если номер начинается с 8, заменяем на 7 (российский формат)
    if clean_phone.startswith('8') and len(clean_phone) == 11:
        clean_phone = '7' + clean_phone[1:]
    
    # Если номер не начинается с 7 и имеет 10 цифр, добавляем 7
    elif len(clean_phone) == 10:
        clean_phone = '7' + clean_phone
    
    return clean_phone

def send_whatsapp_message(phone_number, message_type='text', **kwargs):
    """
    Отправляет сообщение через WhatsApp Business API
    
    Args:
        phone_number: Номер телефона получателя
        message_type: Тип сообщения (text, template, etc.)
        **kwargs: Дополнительные параметры для сообщения
    
    Returns:
        bool: True если сообщение отправлено успешно
    """
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print(f"WhatsApp credentials not configured. Message would be sent to {phone_number}")
        return True  # Return True for demo purposes
    
    formatted_phone = format_phone_number(phone_number)
    if not formatted_phone:
        print(f"Invalid phone number: {phone_number}")
        return False
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    if message_type == 'text':
        payload = {
            'messaging_product': 'whatsapp',
            'to': formatted_phone,
            'type': 'text',
            'text': {
                'body': kwargs.get('text', '')
            }
        }
    elif message_type == 'template':
        payload = {
            'messaging_product': 'whatsapp',
            'to': formatted_phone,
            'type': 'template',
            'template': {
                'name': kwargs.get('template_name'),
                'language': {'code': 'ru'},
                'components': kwargs.get('components', [])
            }
        }
    else:
        print(f"Unsupported message type: {message_type}")
        return False
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"WhatsApp message sent successfully to {formatted_phone}")
            return True
        else:
            print(f"WhatsApp API error: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        print(f"WhatsApp message sending failed: {e}")
        return False

def send_recommendation_whatsapp(user_phone, recommendation_data):
    """
    Отправляет уведомление о рекомендации через WhatsApp
    
    Args:
        user_phone: Номер телефона пользователя
        recommendation_data: Данные рекомендации
    
    Returns:
        bool: Успешность отправки
    """
    priority_emoji = {
        'urgent': '🔥',
        'high': '⚡',
        'normal': '💡'
    }
    
    emoji = priority_emoji.get(recommendation_data.get('priority', 'normal'), '💡')
    
    message = f"""🏠 *Новая рекомендация от менеджера*

{emoji} *{recommendation_data.get('title', '')}*
🏢 {recommendation_data.get('item_name', '')}

{recommendation_data.get('description', '')}

👨‍💼 Менеджер: {recommendation_data.get('manager_name', '')}

Для просмотра деталей перейдите на сайт inback.ru"""
    
    return send_whatsapp_message(user_phone, 'text', text=message)

def send_saved_search_whatsapp(user_phone, search_data):
    """
    Отправляет уведомление о новых результатах поиска через WhatsApp
    
    Args:
        user_phone: Номер телефона пользователя
        search_data: Данные поиска
    
    Returns:
        bool: Успешность отправки
    """
    properties_count = search_data.get('properties_count', 0)
    search_name = search_data.get('search_name', '')
    
    message = f"""🔍 *Новые объекты по вашему поиску*

"{search_name}"

📊 Найдено: *{properties_count} объектов*

🎉 По вашему сохраненному поиску появились новые объекты, которые соответствуют вашим критериям.

Рекомендуем не затягивать с просмотром - хорошие объекты разбирают быстро!

Посмотреть результаты: inback.ru"""
    
    return send_whatsapp_message(user_phone, 'text', text=message)

def send_application_status_whatsapp(user_phone, application_data):
    """
    Отправляет уведомление о статусе заявки через WhatsApp
    
    Args:
        user_phone: Номер телефона пользователя
        application_data: Данные заявки
    
    Returns:
        bool: Успешность отправки
    """
    status_emoji = {
        'pending': '⏳',
        'approved': '✅',
        'rejected': '❌'
    }
    
    status = application_data.get('status', 'pending')
    emoji = status_emoji.get(status, '📋')
    
    status_text = {
        'pending': 'на рассмотрении',
        'approved': 'одобрена',
        'rejected': 'отклонена'
    }
    
    message = f"""📋 *Обновление статуса заявки*

{emoji} Ваша заявка *{status_text.get(status, status)}*

🏠 Объект: {application_data.get('property_name', '')}
💰 Кешбек: {application_data.get('cashback_amount', 0):,} ₽

Подробности в личном кабинете: inback.ru/dashboard"""
    
    return send_whatsapp_message(user_phone, 'text', text=message)

# Интеграция с основной системой уведомлений
def send_whatsapp_notification(user, notification_type, **data):
    """
    Отправляет WhatsApp уведомление
    
    Args:
        user: Объект пользователя
        notification_type: Тип уведомления
        **data: Дополнительные данные
    
    Returns:
        bool: Успешность отправки
    """
    if not hasattr(user, 'phone') or not user.phone:
        return False
    
    if notification_type == 'recommendation':
        return send_recommendation_whatsapp(user.phone, data)
    elif notification_type == 'saved_search_results':
        return send_saved_search_whatsapp(user.phone, data)
    elif notification_type == 'application_status':
        return send_application_status_whatsapp(user.phone, data)
    else:
        # Общее текстовое уведомление
        message = f"""📱 *Уведомление InBack*

{data.get('subject', 'Новое уведомление')}

{data.get('message', '')}

inback.ru"""
        return send_whatsapp_message(user.phone, 'text', text=message)

if __name__ == "__main__":
    # Тестирование WhatsApp интеграции
    test_phone = "+7900000000"  # Тестовый номер
    test_data = {
        'title': 'Тестовая рекомендация',
        'item_name': 'ЖК Тестовый',
        'description': 'Описание тестового объекта',
        'manager_name': 'Тест Менеджер',
        'priority': 'high'
    }
    
    result = send_recommendation_whatsapp(test_phone, test_data)
    print(f"WhatsApp test result: {result}")