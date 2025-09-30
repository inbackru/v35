"""
SMS service integration for client notifications
"""
import os
import requests
from typing import Optional

def send_sms(phone: str, message: str) -> bool:
    """
    Send SMS using various SMS providers
    Currently supports logging SMS content for development
    In production, integrate with services like:
    - Twilio
    - SMS.ru
    - UniSender
    - SMSC.ru
    """
    
    # For development - just log the SMS
    print(f"📱 SMS to {phone}: {message}")
    
    # Example integration with SMS.ru (commented out)
    # Uncomment and configure for production use
    """
    try:
        sms_ru_api_key = os.environ.get('SMS_RU_API_KEY')
        if sms_ru_api_key:
            url = 'https://sms.ru/sms/send'
            params = {
                'api_id': sms_ru_api_key,
                'to': phone.replace('+', '').replace('-', '').replace(' ', ''),
                'msg': message,
                'json': 1
            }
            
            response = requests.post(url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'OK':
                    print(f"SMS sent successfully to {phone}")
                    return True
                else:
                    print(f"SMS failed: {result.get('status_text', 'Unknown error')}")
                    return False
            else:
                print(f"SMS service error: HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"SMS sending error: {e}")
        return False
    """
    
    # Example integration with Twilio (commented out)
    """
    try:
        from twilio.rest import Client
        
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if account_sid and auth_token and from_phone:
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message,
                from_=from_phone,
                to=phone
            )
            
            print(f"SMS sent via Twilio: {message.sid}")
            return True
    except Exception as e:
        print(f"Twilio SMS error: {e}")
        return False
    """
    
    return True  # Return True for development (SMS logged)

def format_phone_for_sms(phone: str) -> str:
    """
    Format phone number for SMS sending
    Convert +7-918-123-45-67 to +79181234567
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters except +
    clean_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
    
    # Ensure proper format
    if clean_phone.startswith('+7'):
        return clean_phone
    elif clean_phone.startswith('7') and len(clean_phone) == 11:
        return '+' + clean_phone
    elif clean_phone.startswith('8') and len(clean_phone) == 11:
        return '+7' + clean_phone[1:]
    
    return clean_phone

def send_login_credentials_sms(phone: str, email: str, password: str, manager_name: str = "", login_url: str = "") -> bool:
    """
    Send login credentials via SMS
    """
    formatted_phone = format_phone_for_sms(phone)
    
    message = f"""InBack.ru - Данные для входа:
Email: {email}
Пароль: {password}
{login_url if login_url else 'Войти на сайте InBack.ru'}
{f'Менеджер: {manager_name}' if manager_name else ''}"""
    
    return send_sms(formatted_phone, message)

def send_welcome_sms(phone: str, client_name: str, manager_name: str = "") -> bool:
    """
    Send welcome SMS to new client
    """
    formatted_phone = format_phone_for_sms(phone)
    
    message = f"""Добро пожаловать в InBack.ru, {client_name}! 
Ваш аккаунт создан. Данные для входа отправлены на email.
{f'Ваш менеджер: {manager_name}' if manager_name else ''}
Тел: +7(918)123-45-67"""
    
    return send_sms(formatted_phone, message)